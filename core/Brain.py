from django import conf
from src.const import Const
import random
from lib.vec2d import Vec2d
from src.Utils import Utils
from core.InfoObj import InfoObj

class Brain():
    def __init__(self, the_thing):

        self.move_target = self.get_new_random_target()

        self.utils = Utils()
        self.this_thing = the_thing

        self.see_enemies = []
        self.see_berries = []
        self.see_trees = []
        self.see_bears = []
        self.see_lairs = []
        self.see_eggs = []
        self.see_meats = []

        self.know_trees = []
        self.know_places_to_copule = []
        self.know_lairs = []

        self.is_hungry = 0.5
        self.want_copule = 0
        self.fear = 0
    
    def append_bear(self, bear, dist):
        self.see_bears.append(InfoObj(bear, dist))
    
    def append_berry(self, berry, dist):
        self.see_berries.append(InfoObj(berry, dist))

    def append_enemies(self, enemy, dist):
        self.see_enemies.append(InfoObj(enemy, dist))
    
    def append_tree(self, tree, dist):
        self.see_trees.append(InfoObj(tree, dist))

    def append_lair(self, lair, dist):
        self.see_lairs.append(InfoObj(lair, dist))

    def append_egg(self, egg, dist):
        self.see_eggs.append(InfoObj(egg, dist))

    def append_meat(self, meat, dist):
        self.see_meats.append(InfoObj(meat, dist))

    def return_dsit(self, e):
        return e.dist
    
    def sort_all(self):
        self.see_enemies.sort(key=self.return_dsit)
        self.see_berries.sort(key=self.return_dsit)
        self.see_trees.sort(key=self.return_dsit)
        self.see_bears.sort(key=self.return_dsit)
        self.see_lairs.sort(key=self.return_dsit)
        self.see_eggs.sort(key=self.return_dsit)
        self.see_meats.sort(key=self.return_dsit) 

    def clean_visibility(self):
        self.see_enemies = []
        self.see_berries = []
        self.see_trees = []
        self.see_bears = []
        self.see_lairs = []
        self.see_eggs = []
        self.see_meats = [] 

    # movements
    def do_not_move(self):
        self.move_target = self.this_thing.rect.center

    def get_new_random_target(self):
        self.move_target = Vec2d(random.randint(Const.THING_MARGIN, Const.SCREEN_SIZE-Const.THING_MARGIN), random.randint(Const.THING_MARGIN, Const.SCREEN_SIZE-Const.THING_MARGIN))

    def fallow(self, thing):
        self.move_target = thing.rect.center

    def runaway(self, thing): 
        self.move_target = self.utils.KeepPointInRange(self.utils.GetReversePoint(self.this_thing, thing))

class Brain_Bear(Brain):
    def __init__(self, the_thing):
        super().__init__(the_thing)
        # main process

    def make_decision(self):
        self.sort_all()
        self.should_stop()
        self.should_go_for_eat()
        self.should_run()
        self.clean_visibility()
    
    def should_stop(self):
        if self.this_thing.fight_timer.is_on() or self.this_thing.copule_timer.is_on():
            self.do_not_move()

    def should_run(self):
        for predator in self.see_enemies:
            if predator.obj.can_attack():
                self.runaway(predator.obj)
                return        

    def should_go_for_eat(self):
        for berry in self.see_berries:
            self.fallow(berry.obj)
            return

    def should_copule(self):
        for bear in self.see_bears:
            if self.this_thing.can_copule() and bear.obj.can_copule():
                self.fallow(bear.obj)
                return

class Brain_Predator(Brain):
    def __init__(self, the_thing):
        super().__init__(the_thing)

    def make_decision(self):
        self.sort_all()
        self.should_go_for_carrion()
        self.should_go_for_egg()
        self.attack_victim()
        self.go_to_lair()
        self.stop_on_lair()
        self.clean_visibility()
    
    def stop_on_lair(self):
        if self.this_thing.meat_timer.is_on()\
             and self.utils.GetDist(self.this_thing, self.this_thing.lair) < self.this_thing.lair_distance:
            self.do_not_move()
    
    def go_to_lair(self):
        if not self.this_thing.lair == None\
             and not self.this_thing.rect.center == self.this_thing.lair.rect.center\
             and self.this_thing.meat_timer.is_on():
            self.fallow(self.this_thing.lair)
    
    def attack_victim(self):
        for victim in self.see_bears:
            if self.this_thing.can_attack():
                self.fallow(victim.obj)

    def should_go_for_carrion(self):
        for carrion in self.see_meats:
            self.fallow(carrion.obj)
            return

    def should_go_for_egg(self):
        for egg in self.see_eggs:
            self.fallow(egg.obj)
            return

