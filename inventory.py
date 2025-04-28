import pygame as pg

class Inventario:
    def __init__(self, game):
        self.game = game
        self.items = []  # Cada ítem será un diccionario: {"imagen": ..., "cantidad": ...}
        self.width = 600
        self.height = 400
        self.bg_color = (30, 30, 30)
        self.font = pg.font.Font(None, 28)
        self.visible = False
        self.image_balas = None

    def agregar_item(self, cantidad):
        if self.items:
            self.items[0]["cantidad"] += cantidad  # Solo actualiza cantidad
        else:
            self.items.append({"imagen": self.image_balas, "cantidad": cantidad})

    def usar_municion(self, cantidad):
        if self.items and self.items[0]["cantidad"] >= cantidad:
            self.items[0]["cantidad"] -= cantidad
            return True
        return False

    def cargar_imagen_balas(self, path):
        try:
            self.image_balas = pg.image.load(path).convert_alpha()
            self.image_balas = pg.transform.scale(self.image_balas, (64, 64))
        except Exception as e:
            print(f"[ERROR] No se pudo cargar la imagen: {e}")

    def dibujar(self):
        # Fondo con bordes redondeados
        rect = pg.Rect(50, 50, self.width, self.height)
        pg.draw.rect(self.game.screen, self.bg_color, rect, border_radius=12)
        pg.draw.rect(self.game.screen, (200, 200, 200), rect, 2, border_radius=12)

        # Título
        titulo = self.font.render("Inventario", True, (255, 255, 255))
        self.game.screen.blit(titulo, (rect.centerx - titulo.get_width() // 2, 60))

        if not self.items:
            vacio = self.font.render("No hay objetos", True, (255, 100, 100))
            self.game.screen.blit(vacio, (rect.centerx - vacio.get_width() // 2, rect.centery))
            return

        padding = 20
        item_size = 64
        cols = 5
        for i, item in enumerate(self.items):
            col = i % cols
            row = i // cols
            x = 80 + col * (item_size + padding)
            y = 120 + row * (item_size + padding)

            if item["imagen"]:
                self.game.screen.blit(item["imagen"], (x, y))

            texto = self.font.render(f'x{item["cantidad"]}', True, (255, 255, 255))
            self.game.screen.blit(texto, (x, y + item_size + 5))
