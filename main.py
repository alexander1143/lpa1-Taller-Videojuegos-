import pygame as pg
import sys
from settings import *
from map import *
from player import *
from raycasting import *
from object_renderer import *
from sprite_object import *
from object_handler import *
from weapon import *
from sound import *
from pathfinding import *
from inventory import *  # Se importa el inventario externo

class Game:
    def __init__(self):
        pg.init()
        pg.mouse.set_visible(False)
        self.screen = pg.display.set_mode(RES)
        pg.event.set_grab(True)
        self.clock = pg.time.Clock()
        self.delta_time = 1
        self.global_trigger = False
        self.global_event = pg.USEREVENT + 0
        pg.time.set_timer(self.global_event, 40)

        self.start_screen()
        self.new_game()

    def start_screen(self):
        input_active = True
        font = pg.font.Font(None, 50)
        screen_width = self.screen.get_width()
        screen_height = self.screen.get_height()

        input_box = pg.Rect(screen_width // 2 - 150, screen_height // 2, 300, 50)
        color_inactive = pg.Color('gray15')
        color_active = pg.Color('dodgerblue2')
        active = True
        color = color_active
        player_name = ''

        while input_active:
            self.screen.fill(pg.Color('black'))

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                elif event.type == pg.MOUSEBUTTONDOWN:
                    if input_box.collidepoint(event.pos):
                        active = True
                    else:
                        active = False
                    color = color_active if active else color_inactive
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        pg.quit()
                        sys.exit()
                    if active:
                        if event.key == pg.K_RETURN and player_name.strip() != "":
                            input_active = False
                        elif event.key == pg.K_BACKSPACE:
                            player_name = player_name[:-1]
                        else:
                            player_name += event.unicode

            title_surface = font.render("Ingrese su nombre:", True, pg.Color("white"))
            name_surface = font.render(player_name, True, color)
            width = max(300, name_surface.get_width() + 10)
            input_box.w = width

            self.screen.blit(title_surface, (screen_width // 2 - title_surface.get_width() // 2, screen_height // 2 - 80))
            self.screen.blit(name_surface, (input_box.x + 5, input_box.y + 10))
            pg.draw.rect(self.screen, color, input_box, 2)

            pg.display.flip()
            self.clock.tick(30)

        self.player_name = player_name
        print(f"Nombre del jugador: {self.player_name}")

    def new_game(self):
        self.map = Map(self)
        self.player = Player(self)
        self.object_renderer = ObjectRenderer(self)
        self.raycasting = RayCasting(self)
        self.object_handler = ObjectHandler(self)
        self.weapon = Weapon(self)
        self.sound = Sound(self)
        self.pathfinding = PathFinding(self)
        pg.mixer.music.play(-1)
        self.font = pg.font.Font(None, 36)

        # Inventario
        self.inventario = Inventario(self)
        self.inventario.cargar_imagen_balas('resources/sprites/weapon/inventario/0.png')
        self.inventario_abierto = False

        # Cargar íconos de vida
        def load_heart(name):
            img = pg.image.load(f'resources/sprites/weapon/{name}.png').convert_alpha()
            return pg.transform.scale(img, (32, 32))

        self.heart_full  = load_heart('heart_full')
        self.heart_half  = load_heart('heart_half')
        self.heart_empty = load_heart('heart_empty')

    def update(self):
        self.player.update()
        self.raycasting.update()
        self.object_handler.update()
        self.weapon.update()
        # ¡Quitamos el flip de aquí!
        self.delta_time = self.clock.tick(FPS)
        pg.display.set_caption(f'{self.clock.get_fps() :.1f}')

    def draw(self):
        # Si tu object_renderer no limpia la pantalla, descomenta la siguiente línea:
        # self.screen.fill('black')

        self.object_renderer.draw()
        self.weapon.draw()

        # Mostrar la barra de vida
        self.mostrar_barra_vida()

        # Mostrar inventario si está abierto
        if self.inventario_abierto:
            self.inventario.dibujar()

        # **Aquí sí hacemos el flip**, después de dibujar TODO
        pg.display.flip()

    def mostrar_barra_vida(self):
        # Definir la posición y tamaño de la barra de vida
        x = self.screen.get_width() - 220
        y = 20
        ancho = 180
        alto = 30
        border_color = (255, 255, 255)
        fondo_color = (60, 60, 60)
        vida_color = (200, 20, 20)

        vida_actual = self.player.health
        vida_maxima = PLAYER_MAX_HEALTH
        ratio = vida_actual / vida_maxima
        vida_ancho = int(ancho * ratio)

        # Dibujar fondo y borde de la barra
        pg.draw.rect(self.screen, fondo_color, (x, y, ancho, alto), border_radius=8)
        pg.draw.rect(self.screen, border_color, (x, y, ancho, alto), 2, border_radius=8)

        # Dibujar la barra de vida (basada en la salud actual)
        pg.draw.rect(self.screen, vida_color, (x, y, vida_ancho, alto), border_radius=8)

    def check_events(self):
        self.global_trigger = False
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()
            elif event.type == self.global_event:
                self.global_trigger = True

            self.player.single_fire_event(event)

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_r:
                    self.inventario.agregar_item(5)
                elif event.key == pg.K_SPACE:
                    if self.inventario.usar_municion(1):
                        print("¡Disparo!")
                    else:
                        print("Sin munición")
                elif event.key == pg.K_t:
                    self.inventario_abierto = not self.inventario_abierto

    def run(self):
        while True:
            self.check_events()
            self.update()
            self.draw()

if __name__ == '__main__':
    game = Game()
    game.run()
