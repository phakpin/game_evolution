from models.Predator import Predator
from models.Bear import Bear
from models.Food import Berry,Meat,Tree
from models.Egg import Egg,Egg_Bear,Egg_Predator
from models.Text import TextInfo
from conf import Conf

class Factory():
    def GetBears(self, count, egg=None):
        if egg == None:
            egg = Egg()
            egg.DNA_size = Conf.DEFAULT_SIZE
            egg.DNA_speed = Conf.INITIAL_SPEED
            egg.DNA_bear_sense = Conf.BEAR_SENSE_FEAR
            egg.DNA_berry_sense = Conf.BEAR_SENSE_FOOD
            egg.DNA_copule_sense = Conf.BEAR_SENSE_COPULE
            egg.DNA_force = Conf.FORCE_BEAR
        collection = []
        for _ in range(count):
            collection.append(Bear(egg))
        return collection

    def GetBear(self, egg):
        return Bear(egg)

    def GetPredators(self, count, egg=None):
        if egg == None:
            egg = Egg()
            egg.DNA_size = Conf.DEFAULT_SIZE
            egg.DNA_speed = Conf.INITIAL_SPEED
            egg.DNA_predator_sense = Conf.SENSE_PREDATOR
            egg.DNA_carrion_sense = Conf.SENSE_CARRION
            egg.DNA_egg_sense = Conf.SENSE_EGG
            egg.DNA_force = Conf.FORCE_PREDATOR
        collection = []
        for _ in range(count):
            collection.append(Predator(egg))
        return collection

    def GetPredator(self, egg=None):
        return Predator(egg)
    
    def GetBerries(self, count):
        collection = []
        for _ in range(count):
            collection.append(Berry())
        return collection
    
    def GetBerriesFromTree(self, count, tree):
        collection = []
        for _ in range(count):
            collection.append(Berry(tree))
        return collection

    def GetEggs(self, count, thing_one, thing_two):
        collection = []
        for _ in range(count):
            collection.append(Egg(thing_one, thing_two))
        return collection

    def GetEggBear(self,thing_one, thing_two):
        return Egg_Bear(thing_one, thing_two)
    
    def GetEggPredator(self,thing_one, thing_two):
        return Egg_Predator(thing_one, thing_two)

    def GetMeat(self, location):
        return Meat(location)

    def GetTree(self, location):
        return Tree(location)

    def GetText(self, text, loc):
        return TextInfo(text, loc)