import pygame.sprite
from src.Images import Images

class Starve(pygame.sprite.Sprite):
      def __init__(self):
        super().__init__()
        self.size = 100
        self.image = Images.getInstance().Starve
        self.rect = self.image.get_rect()

      def draw(self, surface, center):
        self.rect.center=center
        surface.blit(self.image, self.rect)