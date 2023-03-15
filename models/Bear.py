import random
from core.Brain import Brain_Bear
from models.TheThing import TheThing,Age
from conf import Conf
from src.const import Const
from src.Images import Images
from src.Timer import Timer
from models.Food import Berry

class Bear(TheThing):
  def __init__(self, egg):
    super().__init__(egg)
    self.brain = Brain_Bear(self)
    self.brain.get_new_random_target()
    if egg.initial:
      self.age = Age.ADULT
    self.berry_string = ""
    self.current_live.set_timer(Conf.LIVE_WITHOUT_BERRY)
    self.image = Images.getInstance().Thing_good_YOUNG
    self.rect = self.image.get_rect()
    self.sense_fear = egg.DNA_bear_sense
    self.sense_food = egg.DNA_berry_sense
    self.sense_copule = egg.DNA_copule_sense
    self.berry_visibility = Timer()
    self.fear = False
    if egg.initial:
      self.rect.center=(random.randint(Const.THING_MARGIN, Const.SCREEN_SIZE-Const.THING_MARGIN),Const.SCREEN_SIZE-Const.THING_MARGIN)
    else:
      self.rect.center=(egg.Location_X, egg.Location_Y)
    self.berries = 0
    self.berry_image = Berry()

  def get_details(self):
    print(f'Name: {self.name} | Eggs: {self.eggs} | Berries: {self.berries} | Speed: {self.speed} | Power: {self.force} | Age: {self.age.name} | Sense_fear: {self.sense_fear}\
  | Sense_food: {self.sense_food} | sense_copule: {self.sense_copule}')

  def got_berry(self):
    self.current_live.eat(Conf.LIVE_FROM_BERRY)
    self.berry_visibility.set_timer(Conf.LIVE_FROM_BERRY)
    self.berries = self.berries + 1

  def update(self):
    super().update()
    self.current_live.update(self.consumption())
    self.berry_visibility.update()
    self.copule_timer.update()
    self.cant_copule_timer.update()
    if not self.current_live.is_on():
      self.make_dead()
    self.update_image()
    self.brain.make_decision()

  def make_copule(self, partner):
    if not self.can_copule() or not partner.can_copule():
      return False
    super().make_copule()
    self.copule_timer.set_timer(Conf.COPULE_TIME_BEAR)
    self.cant_copule_timer.set_timer(Conf.COPULE_TIME_BEAR*2)
    return True
  
  def make_dead(self):
    super().make_dead()
    self.berry_visibility.disable_timer()

  def update_image(self):
    if self.is_dead:
      self.image = Images.getInstance().Thing_dead
      return
    if self.age == Age.YOUNG:
      self.image = Images.getInstance().Thing_good_YOUNG
    elif self.age == Age.ADULT:
      self.image = Images.getInstance().Thing_good_ADULT
    elif self.age == Age.OLD:
      self.image = Images.getInstance().Thing_good_OLD
    super().scale()

  def draw(self, ds):
    super().draw(ds)
    if self.berry_visibility.is_on():
      center = (self.rect.center[0] - 0.3 * self.size, self.rect.center[1] + 0.3 * self.size)
      self.berry_image.draw(ds, center)

# SENSES
  def Sense_predator(self, predator):
    dist = self.utils.GetDist(self, predator)
    if dist < self.sense_fear:
      self.brain.append_enemies(predator, dist)

  def Sense_food(self, berry):
    dist = self.utils.GetDist(self, berry)
    if dist < self.sense_food:
      self.brain.append_berry(berry, dist)

  def Sense_copule(self, bear):
    dist = self.utils.GetDist(self, bear)
    if dist < self.sense_copule:
      self.brain.append_bear(bear, dist)
  
  def Sense_tree(self, tree):
    dist = self.utils.GetDist(self, tree)
    if dist < Conf.SIGHT_RANGE:
      self.brain.append_tree(tree, dist)
  
  def Sense_Lair(self, lair):
    dist = self.utils.GetDist(self, lair)
    if dist < Conf.SIGHT_RANGE:
      self.brain.append_lair(lair, dist)