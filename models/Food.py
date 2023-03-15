import pygame.sprite
import random
from src.const import Const
from src.Images import Images
from src.Timer import Timer
from conf import Conf
from enum import Enum

class Food(pygame.sprite.Sprite):
      def __init__(self):
        super().__init__()
        self.gone = False
        self.exist_timer = Timer()
 
      def draw(self, surface, center = None):
        if center != None:
          self.rect.center=center
        surface.blit(self.image, self.rect)

      def update(self):
        self.exist_timer.update()
        if not self.exist_timer.is_on():
          self.gone = True

class Berry(Food):
      def __init__(self, tree = None):
        super().__init__()
        self.size = 10
        self.dist = 70
        self.exist_timer = Timer(Conf.BERRY_EXIST)
        self.image = Images.getInstance().Berry
        self.rect = self.image.get_rect()
        if tree == None:
          self.rect.center=(random.randint(Const.BERRY_MARGIN, Const.SCREEN_SIZE-Const.BERRY_MARGIN),random.randint(Const.BERRY_MARGIN, Const.SCREEN_SIZE-Const.BERRY_MARGIN))
        else:
          self.rect.center=(self.normalize_location(random.randint(tree.rect.center[0] - self.dist, tree.rect.center[0] + self.dist)), \
            self.normalize_location(random.randint(tree.rect.center[1] - self.dist, tree.rect.center[1] + self.dist)))
        
      def normalize_location(self, value):
        if value > (Const.SCREEN_SIZE - 15):
          return Const.SCREEN_SIZE - 15
        if value < 15:
          return 15
        return value

class Meat(Food):
      def __init__(self, location):
        super().__init__()
        self.size = 15
        self.exist_timer = Timer(Conf.MEAT_EXITS)
        self.image = Images.getInstance().Meat
        self.rect = self.image.get_rect()
        self.rect.center=location

class Egg_Food(Food):
      def __init__(self, location):
        super().__init__()
        self.size = 20
        self.exist = Conf.MEAT_EXITS
        self.image = Images.getInstance().Egg_for_predator 
        self.rect = self.image.get_rect()
        self.rect.center=location

class Age(Enum):
  GROWING = 1
  ADULT = 2

class Tree(Food):
  def __init__(self, location):
        super().__init__()
        self.tree_size = 1
        self.exist_timer = Timer(Conf.TREE_EXIST)
        self.growing_timer = Timer(Conf.TREE_GROWING)
        self.age = Age.GROWING
        self.image = Images.getInstance().Bush
        self.rect = self.image.get_rect()
        self.rect.center = location
        self.location = location
        self.renew_berry_timer = Timer(Conf.TIMER_RENEW_BERRIES_TREE)

  def update_tree(self):
    if self.age == Age.GROWING:
      self.growing_timer.update()
    if self.age == Age.ADULT:
      self.exist_timer.update()

    if not self.growing_timer.is_on() and self.age == Age.GROWING:
      self.age = Age.ADULT
    if not self.exist_timer.is_on():
      self.gone = True
    
    if self.age == Age.GROWING:
      self.tree_size = int((60 * (Conf.TREE_GROWING - self.growing_timer.get_time()))/Conf.TREE_GROWING) + 1

  def draw(self, surface):
    self.scale()
    super().draw(surface)

  def renew_berry(self):
    if self.age == Age.GROWING:
      return False
    self.renew_berry_timer.update()
    if not self.renew_berry_timer.is_on():
      self.renew_berry_timer.set_timer(Conf.TIMER_RENEW_BERRIES_TREE)
      return bool(random.randint(0, 1))
    return False

  def scale(self):
    self.image = Images.getInstance().Bush
    self.image = pygame.transform.scale(self.image, (self.tree_size, self.tree_size))
    self.rect = self.image.get_rect()
    self.rect.center = (self.location[0], self.location[1] - 0.5 * self.tree_size)
       



