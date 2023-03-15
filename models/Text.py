import pygame
from src.const import Const
from src.Timer import Timer

class TextInfo():
    def __init__(self, text, thing):
        font = pygame.font.Font('res/Zabdilus.ttf', 20)
        self.text_settings = font.render(text, True, Const.BLACK, Const.WHITE)
        self.textRect = self.text_settings.get_rect()
        self.textRect.center = (thing.rect.center[0], thing.rect.center[1] - 27)
        self.text_timer = Timer(200)
    
    def draw(self, ds):
        ds.blit(self.text_settings, self.textRect)

    def update(self):
        self.text_timer.update()

    def should_remove(self):
        if not self.text_timer.is_on():
            return True
        return False