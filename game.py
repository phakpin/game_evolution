import pygame
import random
from pygame.locals import *
import sys
from models.TheThing import Age
from src.const import Const
from models.Egg import EggStage,EggType
from src.Factory import Factory
from models.Lair import Lair
from conf import Conf
from src.Stats import Stats
from src.Utils import Utils
from src.Timer import Timer
from src.Natural_interaction import Interaction

# Assign FPS a value
FPS = 60
FramePerSec = pygame.time.Clock()

pygame.init()
DISPLAYSURF = pygame.display.set_mode((Const.SCREEN_SIZE, Const.SCREEN_SIZE))
DISPLAYSURF.fill(Const.WHITE)
pygame.display.set_caption(Const.GAME_NAME)

class Game():
  def __init__(self):
    self.factory = Factory()
    self.stats = Stats()
    self.utils = Utils()
    self.renew_berries_timer = Timer(Conf.TIMER_RENEW_BERRIES)
    self.initail_renew_berries = Conf.INITIAL_RENEW_BERRIES

    self.BerryCollection = []
    self.CleanBerryCollection = []

    self.TreeCollection = []
    self.CleanTreeCollection = []

    self.MeatCollection = []
    self.CleanMeatCollection = []

    self.BearCollection = []
    self.CleanBearCollection = []

    self.PredatorCollection = []
    self.CleanPredatorCollection = []

    self.EggCollection = []
    self.CleanEggCollection = []

    self.TextCollection = []
    self.CleanTextCollection = []

    self.Lairs = []

  def create_game_objects(self):
    self.Lairs.append(Lair(0.25 * Const.SCREEN_SIZE, 0.5 * Const.SCREEN_SIZE))
    self.Lairs.append(Lair(0.75 * Const.SCREEN_SIZE, 0.5 * Const.SCREEN_SIZE))
    self.PredatorCollection.extend(self.factory.GetPredators(Conf.NUMBER_OF_PREDATORS))
    for predator in self.PredatorCollection:
      rand = random.randint(0,1)
      predator.lair = self.Lairs[rand]
    self.BearCollection.extend(self.factory.GetBears(Conf.NUMBER_OF_BEARS))
    self.BerryCollection.extend(self.factory.GetBerries(Conf.NUMBER_OF_BERRIES))

  def bear_colision_detection(self):
    for bear in self.BearCollection:

      if bear.is_dead:
        continue

      #bear - predator
      for enemy in self.PredatorCollection:
        bear.Sense_predator(enemy)
        enemy.sense_victim(bear)
        if self.utils.IsCollision(bear, enemy):
          if bear.can_fight() and enemy.can_fight():
            inter = Interaction()
            inter.Force_Fight(bear, enemy)
            enemy.make_fight()
            bear.make_fight()
            self.TextCollection.append(self.factory.GetText("{:.2f}".format(inter.predator_force), enemy))
            self.TextCollection.append(self.factory.GetText("{:.2f}".format(inter.bear_force), bear))
            if inter.winner is enemy:
              if enemy.can_kill():
                enemy.got_meat()
                bear.make_dead()
              else:
                bear.make_injury()
            if inter.winner is bear:
              if bear.can_kill():
                enemy.make_dead()
              else:
                enemy.make_injury()

      #bear - berry
      for berry in self.BerryCollection:
        if berry.gone:
          continue
        bear.Sense_food(berry)

        if self.utils.IsCollision(bear, berry):
          berry.gone = True
          bear.got_berry()

      #bear - bear
      for second_bear in self.BearCollection:
        if bear is second_bear:
          continue
        bear.Sense_copule(second_bear)
        second_bear.Sense_copule(bear)

        if self.utils.IsCollision(bear, second_bear):
          if bear.can_copule() and second_bear.can_copule():
            bear.make_copule()
            second_bear.make_copule()
            self.EggCollection.append(self.factory.GetEggBear(bear, second_bear))
        
      #bear - tree
      for tree in self.TreeCollection:
        if tree.gone:
          continue
        bear.Sense_tree(tree)
      
      #bear - lair
      for lair in self.Lairs:
        bear.Sense_Lair(lair)


  def predator_colision_detection(self):
    for predator in self.PredatorCollection:
      if predator.is_dead:
        continue
      
      for lair in self.Lairs:
        if self.utils.IsCollision(predator, lair):
          predator.lair = lair
      
      # predator to predator
      for predaror_second in self.PredatorCollection:
        if predator is predaror_second:
          continue
        if self.utils.IsCollision(predator, predaror_second):
            if predator.can_copule() and predaror_second.can_copule():
              predator.make_copule()
              predaror_second.make_copule()
              self.EggCollection.append(self.factory.GetEggPredator(predator, predaror_second))

      # carrion to predator
      for carrion in self.MeatCollection:
        if not predator.age == Age.ADULT:
          predator.sense_carrion(carrion)
          if self.utils.IsCollision(predator, carrion):
            predator.eat_carrion()
            carrion.gone = True
      
      # egg to predator 
      for egg in self.EggCollection:
        if egg.egg_type == EggType.PREDATOR:
          continue
        predator.sense_egg(egg)
        if self.utils.IsCollision(predator, egg):
          predator.eat_egg()
          egg.destroy()

  def cleanup(self):

    for berry in self.CleanBerryCollection:
      self.BerryCollection.remove(berry)
    self.CleanBerryCollection = []

    for meat in self.CleanMeatCollection:
      self.MeatCollection.remove(meat)
    self.CleanMeatCollection = []

    for bear in self.CleanBearCollection:
      self.BearCollection.remove(bear)
    self.CleanBearCollection = []

    for egg in self.CleanEggCollection:
      self.EggCollection.remove(egg)
    self.CleanEggCollection = []

    for predator in self.CleanPredatorCollection:
      self.PredatorCollection.remove(predator)
    self.CleanPredatorCollection = []

    for text in self.CleanTextCollection:
      self.TextCollection.remove(text)
    self.CleanTextCollection = []

    for tree in self.CleanTreeCollection:
      self.TreeCollection.remove(tree)
    self.CleanTreeCollection = []

  def update_all(self):
    for bear in self.BearCollection:
      bear.update()
      if bear.is_dead and not bear.dead_body_exist_timer.is_on():
        self.CleanBearCollection.append(bear)
        self.MeatCollection.append(self.factory.GetMeat(bear.rect.center))

    for predator in self.PredatorCollection:
      if predator.is_dead and not predator.dead_body_exist_timer.is_on():
        self.CleanPredatorCollection.append(predator)
      predator.update()
  
    for egg in self.EggCollection:
      egg.update()
    
    for berry in self.BerryCollection:
      berry.update()
      if berry.gone:
        self.CleanBerryCollection.append(berry)
        if not berry.exist_timer.is_on():
          self.TreeCollection.append(self.factory.GetTree(berry.rect.center))

    for meat in self.MeatCollection:
      meat.update()
      if meat.gone:
        self.CleanMeatCollection.append(meat)
    
    for text in self.TextCollection:
      text.update()
      if text.should_remove():
        self.CleanTextCollection.append(text)
    
    for tree in self.TreeCollection:
      tree.update_tree()
      if tree.renew_berry():
        self.BerryCollection.extend(self.factory.GetBerriesFromTree(random.randint(0, 2), tree))
      if tree.gone:
        self.CleanTreeCollection.append(tree)

  def draw_all(self, ds):
    for lair in self.Lairs:
      lair.draw(ds)
    for tree in self.TreeCollection:
      tree.draw(ds)
    for bear in self.BearCollection:
      bear.draw(ds)
    for predator in self.PredatorCollection:
      predator.draw(ds)
    for berry in self.BerryCollection:
      berry.draw(ds)
    for meat in self.MeatCollection:
      meat.draw(ds)
    for egg in self.EggCollection:
      egg.draw(ds)
    for text in self.TextCollection:
      text.draw(ds)

  def general_state_updater(self):
    self.renew_berry()
    self.eggs_handle()

  def renew_berry(self):
    if self.initail_renew_berries <= 0:
      return
    self.renew_berries_timer.update()
    if not self.renew_berries_timer.is_on():
      self.initail_renew_berries -= 1
      self.renew_berries_timer.set_timer(Conf.TIMER_RENEW_BERRIES)
      self.BerryCollection.extend(self.factory.GetBerries(Conf.NUMBER_OF_BERRIES))
  
  def eggs_handle(self):
    for egg in self.EggCollection:
      if egg.egg_stage == EggStage.DESTROY:
        self.CleanEggCollection.append(egg)
      if egg.egg_stage == EggStage.TO_HATCH:
        if egg.egg_type == EggType.BEAR:
          self.BearCollection.append(self.factory.GetBear(egg))
        if egg.egg_type == EggType.PREDATOR:
          self.PredatorCollection.append(self.factory.GetPredator(egg))
        self.CleanEggCollection.append(egg)

  def print_stats(self):
    print("\n\n####################################################")
    self.stats.print_bear_stats(self.BearCollection)
    self.stats.print_predator_stats(self.PredatorCollection)
    self.stats.print_fruit_stats(self.BerryCollection)

  def display_info_from_object(self, point):
    for bear in self.BearCollection:
      dist = self.utils.GetDistPoints(point, bear.rect.center)
      if dist < 30:
        bear.get_details()

def main():
  MainGame = Game()
  MainGame.create_game_objects()
  Pause = False

  #Game loop begins
  while True:
      pygame.display.update()
      for event in pygame.event.get():
          if event.type == QUIT:
              pygame.quit()
              sys.exit()
          if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
              MainGame.print_stats()
            if event.key == pygame.K_p:
              Pause = not Pause
          if event.type == pygame.MOUSEBUTTONUP:
            MainGame.display_info_from_object(pygame.mouse.get_pos())

      if(Pause):
        continue

      MainGame.update_all()
      DISPLAYSURF.fill(Const.WHITE)
      MainGame.draw_all(DISPLAYSURF)
      MainGame.bear_colision_detection()
      MainGame.predator_colision_detection()
      MainGame.cleanup()
      MainGame.general_state_updater()
      FramePerSec.tick(FPS)

if __name__ == "__main__":
  main()