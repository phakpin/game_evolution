from conf import Conf
import pygame.sprite
from enum import Enum
import numpy
from src.Images import Images
from src.Timer import Timer
from src.Utils import Utils
class EggStage(Enum):
  COPULE = 1
  EGG = 2
  TO_HATCH = 3
  DESTROY = 4

class EggType(Enum):
  BEAR = 1
  PREDATOR = 2

class Egg(pygame.sprite.Sprite):
    
    def __init__(self, thing_one=None, thing_two=None):
        super().__init__()
        self.initial = False
        if thing_one == None and thing_two == None:
            #initial egg
            self.initial = True
            return
        
        self.size = 20
        self.thing_one = thing_one
        self.thing_two = thing_two
        self.egg_timer = Timer(Conf.EGG_TIME)
        self.egg_stage = EggStage.COPULE
        self.rect = self.image.get_rect()
        self.Location_X = (thing_one.rect.center[0] + thing_two.rect.center[0])/2
        self.Location_Y = (thing_one.rect.center[1] + thing_two.rect.center[1])/2
        self.rect.center=(self.Location_X,self.Location_Y)
        self.utils = Utils()

    def destroy(self):
        self.egg_stage = EggStage.DESTROY

    def update(self):
        if self.egg_stage == EggStage.COPULE:
            self.copule_timer.update()
            if not self.copule_timer.is_on():
                if self.thing_one.is_dead or self.thing_two.is_dead or not self.utils.IsCollision(self.thing_one, self.thing_two):
                   self.egg_stage = EggStage.DESTROY
                else:
                    self.egg_stage = EggStage.EGG

        if self.egg_stage == EggStage.EGG:
            self.egg_timer.update()
            if not self.egg_timer.is_on():
                self.egg_stage = EggStage.TO_HATCH

    def draw(self, surface):
        if self.egg_stage == EggStage.EGG:
            surface.blit(self.image, self.rect)
    
    def normalize_size(self, size):
        if size < (0.5*Conf.DEFAULT_SIZE):
            return (0.5*Conf.DEFAULT_SIZE)
        if size > (2*Conf.DEFAULT_SIZE):
            return (2*Conf.DEFAULT_SIZE)
        return size
    
    def normalize_speed(self, speed):
        if speed < (0.5*Conf.INITIAL_SPEED):
            return (0.5*Conf.INITIAL_SPEED)
        if speed > (2*Conf.INITIAL_SPEED):
            return (2*Conf.INITIAL_SPEED)
        return speed

class Egg_Bear(Egg):
    def __init__(self, thing_one=None, thing_two=None):
        self.image = Images.getInstance().Egg
        self.copule_timer = Timer(Conf.COPULE_TIME_BEAR)
        super().__init__(thing_one, thing_two)  
        self.DNA_size = numpy.random.normal((thing_one.size + thing_two.size)/2, 1, 1)[0]
        self.DNA_size = self.normalize_size(self.DNA_size)
        self.DNA_speed = numpy.random.normal((thing_one.speed + thing_two.speed)/2, 0.3, 1)[0]
        self.DNA_speed = self.normalize_speed(self.DNA_speed)
        self.DNA_bear_sense = numpy.random.normal((thing_one.sense_fear + thing_two.sense_fear)/2, 6, 1)[0]
        self.DNA_berry_sense = numpy.random.normal((thing_one.sense_food + thing_two.sense_food)/2, 6, 1)[0]
        self.DNA_copule_sense = numpy.random.normal((thing_one.sense_copule + thing_two.sense_copule)/2, 6, 1)[0]
        self.egg_type = EggType.BEAR 
        self.DNA_force = numpy.random.normal((thing_one.force + thing_two.force)/2, 0.05, 1)[0]


class Egg_Predator(Egg):
    def __init__(self, thing_one=None, thing_two=None):
        self.image = Images.getInstance().Egg_predator
        self.copule_timer = Timer(Conf.COPULE_TIME_PREDATOR)
        super().__init__(thing_one, thing_two)
        self.egg_type = EggType.PREDATOR
        self.DNA_size = numpy.random.normal((thing_one.size + thing_two.size)/2, 1, 1)[0]
        self.DNA_size = self.normalize_size(self.DNA_size)
        self.DNA_speed = numpy.random.normal((thing_one.speed + thing_two.speed)/2, 0.3, 1)[0]
        self.DNA_speed = self.normalize_speed(self.DNA_speed)
        self.DNA_predator_sense = numpy.random.normal((thing_one.sense_predator + thing_two.sense_predator)/2, 5, 1)[0]
        self.DNA_carrion_sense = numpy.random.normal((thing_one.sense_carrion_value + thing_two.sense_carrion_value)/2, 5, 1)[0]
        self.DNA_force = numpy.random.normal((thing_one.force + thing_two.force)/2, 0.05, 1)[0]
        self.DNA_egg_sense = numpy.random.normal((thing_one.sense_egg_value + thing_two.sense_egg_value)/2, 5, 1)[0]