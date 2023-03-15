import pygame.sprite
from src.Images import Images

class Lair(pygame.sprite.Sprite):

      def __init__(self,X,Y):
        super().__init__()
        self.size = 100
        self.image = Images.getInstance().lair
        self.rect = self.image.get_rect()
        self.rect.center=(X,Y)

      def draw(self, surface):
        surface.blit(self.image, self.rect)