import random
from core.Brain import Brain_Predator
from models.TheThing import TheThing,Age
from conf import Conf
from src.const import Const
from src.Images import Images
from src.Timer import Timer
from models.Food import Meat, Egg_Food

class Predator(TheThing):
  def __init__(self, egg):
    super().__init__(egg)
    self.brain = Brain_Predator(self)
    self.brain.get_new_random_target()
    if egg.initial:
      self.age = Age.ADULT
    self.image = Images.getInstance().Thing_predator_YOUNG
    self.rect = self.image.get_rect()
    self.current_live.set_timer(Conf.LIVE_WITHOUT_MEAT)
    self.lair_distance = 15
    self.lair = None
    self.has_egg_timer = Timer()
    self.meat_timer = Timer()
    self.sense_predator = egg.DNA_predator_sense
    self.sense_carrion_value = egg.DNA_carrion_sense
    self.sense_egg_value = egg.DNA_egg_sense
    self.meat_image = Meat((0,0))
    self.egg_image = Egg_Food((0,0))

    if egg.initial:
      self.rect.center=(random.randint(Const.THING_MARGIN, Const.SCREEN_SIZE-Const.THING_MARGIN),Const.THING_MARGIN)
    else:
      self.rect.center=(egg.Location_X, egg.Location_Y)

  def got_meat(self):
    if self.injury_timer.is_on():
      return
    self.meat_timer.set_timer(2000)
    self.current_live.eat(Conf.LIVE_FROM_MEAT)

  def eat_carrion(self):
    self.meat_timer.set_timer(1000)
    self.current_live.eat(Conf.LIVE_FROM_CORRION)

  def eat_egg(self):
    self.has_egg_timer.set_timer(500)
    self.current_live.eat(Conf.LIVE_FROM_EGG)

  def update(self):
    super().update()
    self.current_live.update(self.consumption())
    self.meat_timer.update()
    self.has_egg_timer.update()
    self.copule_timer.update()
    self.cant_copule_timer.update()
    
    if not self.current_live.is_on():
      self.make_dead()

    self.update_image()
    self.brain.make_decision()

  def make_copule(self, partner):
    if not self.can_copule_predator() or not partner.can_copule_predator():
      return False
    super().make_copule()
    self.copule_timer.set_timer(Conf.COPULE_TIME_PREDATOR)
    self.cant_copule_timer.set_timer(Conf.COPULE_TIME_PREDATOR * 2)
    return True

  def update_image(self):
    if self.is_dead:
      self.image = Images.getInstance().Thing_dead
      return
    if self.age == Age.YOUNG:
      self.image = Images.getInstance().Thing_predator_YOUNG
    elif self.age == Age.ADULT:
      self.image = Images.getInstance().Thing_predator_ADULT
    elif self.age == Age.OLD:
      self.image = Images.getInstance().Thing_predator_OLD
    super().scale()

  def draw(self, ds):
    super().draw(ds)
    if self.meat_timer.is_on():
      center = (self.rect.center[0] - 0.3 * self.size, self.rect.center[1] + 0.3 * self.size)
      self.meat_image.draw(ds, center)
    if self.has_egg_timer.is_on():
      center = (self.rect.center[0] + 0.3 * self.size, self.rect.center[1] + 0.3 * self.size)
      self.egg_image.draw(ds, center)

  def can_copule_predator(self):
    if not self.is_dead \
      and not self.cant_copule_timer.is_on() \
      and not self.lair == None \
      and not self.injury_timer.is_on() \
      and self.utils.GetDist(self, self.lair) < self.lair_distance \
      and self.age == Age.ADULT:
      return True
    return False

  def can_fight(self):
    basic_value = super().can_fight()
    if basic_value and not self.meat_timer.is_on():
      return True
    else:
      return False
  
  def make_dead(self):
    super().make_dead()
    self.has_egg_timer.disable_timer()
    self.meat_timer.disable_timer()

  def can_attack(self):
    return self.age == Age.ADULT and not self.meat_timer.is_on() and not self.is_dead

  def sense_victim(self, bear):
    dist = self.utils.GetDist(self, bear)
    if dist < self.sense_predator:
      self.brain.append_bear(bear, dist)

  def sense_carrion(self, carrion):
    dist = self.utils.GetDist(self, carrion)
    if dist < self.sense_carrion_value:
      self.brain.append_meat(carrion, dist)

  def sense_egg(self, egg):
    dist = self.utils.GetDist(self, egg)
    if dist < self.sense_egg_value:
      self.brain.append_egg(egg, dist)