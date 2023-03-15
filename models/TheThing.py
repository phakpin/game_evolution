import pygame.sprite
import random
from models.Injury import Injury
from models.Starve import Starve
from core.Brain import Brain
from lib.vec2d import Vec2d
from src.Images import Images
from conf import Conf
from enum import Enum
import string
from src.Utils import Utils
from src.Timer import Timer_Live, Timer, Timer_Whole_Live

class Age(Enum):
  YOUNG = 1
  ADULT = 2
  OLD = 3

class TheThing(pygame.sprite.Sprite):
  def __init__(self, egg):
    super().__init__()
    self.brain = None
    
    self.size = egg.DNA_size
    self.speed = egg.DNA_speed
    self.force = egg.DNA_force
    self.is_dead = False
    self.utils = Utils()
    self.live_time_timer = Timer_Whole_Live(Conf.THING_LIVE_TIME)
    self.age = Age.YOUNG
    self.name = ''.join(random.choice(string.ascii_lowercase) for i in range(10))
    self.current_live = Timer_Live()
    self.dead_body_exist_timer = Timer()
    self.cant_copule_timer = Timer()
    self.copule_timer = Timer()
    self.fight_timer = Timer()
    self.injury_timer = Timer()
    self.injury_image = Injury()
    self.starve_image = Starve()
    self.eggs = 0

  def scale(self):
    self.image = pygame.transform.scale(self.image, (self.size, self.size))

  def get_size_factor(self):
    return self.size / Conf.DEFAULT_SIZE

  def get_speed_factor(self):
    return self.speed / Conf.INITIAL_SPEED

  def consumption(self):
    return 1 * self.get_speed_factor() * self.get_size_factor()

  def get_injury_factor(self):
    if self.injury_timer.is_on():
      return 0.5
    else:
      return 1

  def get_speed(self):
    return (self.get_injury_factor() * self.speed) * (2 - self.get_size_factor())
  
  def get_force(self):
    return self.force * self.get_size_factor()

  def make_injury(self):
    self.injury_timer.set_timer(700)

  def can_fight(self):
    if not self.is_dead and not self.fight_timer.is_on() and not self.injury_timer.is_on():
      return True
    return False

  def make_fight(self):
    self.fight_timer.set_timer(200)

  def update(self):
    if not self.is_dead:
      self.live_time_timer.update()
      self.move()
    if not self.live_time_timer.is_on():
      self.make_dead()
    self.dead_body_exist_timer.update()
    self.fight_timer.update()
    self.injury_timer.update()
    self.age_control()

  def make_dead(self):
    if not self.is_dead:
      self.dead_body_exist_timer.set_timer(Conf.DEAD_BODY_EXIST)
      self.image = Images.getInstance().Thing_dead
      self.injury_timer.disable_timer()
      self.is_dead = True

  def make_copule(self):
    self.eggs += 1
  
  def can_kill(self):
    if self.age == Age.ADULT:
      return True
    return False

  def age_control(self):
    if self.live_time_timer.get_current_live_time() < Conf.ADULT_AGE and self.live_time_timer.get_current_live_time() > Conf.OLD_AGE:
      self.age = Age.ADULT
    if self.live_time_timer.get_current_live_time() < Conf.OLD_AGE:
      self.age = Age.OLD

  def can_copule(self):
    if self.is_dead or self.injury_timer.is_on():
      return False
    if not self.cant_copule_timer.is_on() and self.age == Age.ADULT:
      return True
    else:
      return False
 
  def move(self):
    self.pos = Vec2d(self.rect.center)
    self.target = self.brain.move_target
    move = self.target - self.pos
    if move.length >= self.get_speed():
      move.length = self.get_speed()
      self.pos += move
      self.rect.move_ip(move.x, move.y)
    else:
      self.brain.get_new_random_target()
 
  def draw(self, surface):
    surface.blit(self.image, self.rect)
    if self.injury_timer.is_on():
      center = (self.rect.center[0] + 0.2 * self.size, self.rect.center[1] - 0.2 * self.size)
      self.injury_image.draw(surface,center)
    if self.current_live.is_starve() and not self.is_dead:
      center = (self.rect.center[0] - 0.5 * self.size, self.rect.center[1] + 0.5 * self.size)
      self.starve_image.draw(surface, center)
