import pygame.sprite

class Images:
   __instance = None

   @staticmethod 
   def getInstance():
      if Images.__instance == None:
         Images()
      return Images.__instance

   def __init__(self):
      if Images.__instance != None:
         raise Exception("This class is a singleton!")
      else:
         Images.__instance = self
         self.Thing_good_YOUNG = pygame.image.load("res/Thing_good_YOUNG.png")
         self.Thing_good_ADULT = pygame.image.load("res/Thing_good_ADULT.png")
         self.Thing_good_OLD = pygame.image.load("res/Thing_good_OLD.png")

         self.Thing_predator_YOUNG = pygame.image.load("res/Thing_predator_YOUNG.png")
         self.Thing_predator_ADULT = pygame.image.load("res/Thing_predator_ADULT.png")
         self.Thing_predator_OLD = pygame.image.load("res/Thing_predator_OLD.png")

         self.Thing_dead = pygame.image.load("res/Thing_dead.png")
         self.Egg = pygame.image.load("res/Egg.png")
         self.Egg_predator = pygame.image.load("res/Egg_predator.png")
         self.Egg_for_predator = pygame.image.load("res/Egg_For_Predator.png")
         self.Berry = pygame.image.load("res/Berry.png")
         self.Meat = pygame.image.load("res/Meat.png")
         self.Bush = pygame.image.load("res/Bush.png")
         self.Injury = pygame.image.load("res/Injury.png")
         self.lair = pygame.image.load("res/lair.png")
         self.Starve = pygame.image.load("res/Starve.png")
         self.Thing_dead = pygame.image.load("res/Thing_dead.png")
