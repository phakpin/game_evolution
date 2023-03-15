import random
from models.TheThing import Age

class Interaction():
    def Force_Fight(self, bear, predator):
        
        bear_rand_factor = random.randint(1, 5)
        bear_reductor = 0
        if not bear.age == Age.ADULT:
            bear_reductor = 0.1
        self.bear_force = (bear.get_force() - bear_reductor) * bear_rand_factor

        predator_rand_factor = random.randint(1, 5)
        predator_reductor = 0
        if not predator.age == Age.ADULT:
            predator_reductor = 0.1
        
        self.predator_force = (predator.get_force() - predator_reductor) * predator_rand_factor

        if self.predator_force > self.bear_force:
            self.winner = predator
            self.looser = bear
        else:
            self.winner = bear
            self.looser = predator
            
