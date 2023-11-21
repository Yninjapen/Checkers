from pygame.font import *
white = (255, 255, 255)
class Text:

    def __init__(self, text: str, font: Font, center: tuple[int, int], color: tuple[int, int, int] = white, antialias: bool = True, background: tuple[int, int, int] = None):
        self.text = text
        self.font = font
        self.center = center
        self.color = color
        self.antialias = antialias
        self.background = background
        self.render()

    def render(self):
        self.text_obj = self.font.render(self.text, self.antialias, self.color, self.background)
        self.rect = self.text_obj.get_rect()
        self.rect.center = self.center

    def draw(self, screen):
        screen.blit(self.text_obj, self.rect)

    def set_center(self, center: tuple[int, int]):
        self.center = center
        self.render()

    def set_color(self, color: tuple[int, int, int]):
        self.color = color
        self.render()

    def set_font(self, font: Font):
        self.font = font
        self.render()

    def set_text(self, text):
        self.text = text
        self.render()