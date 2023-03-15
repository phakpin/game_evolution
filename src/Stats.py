class Stats():

    def print_bear_stats(self, collection):
        print("\nSTATISTICS FOR " + str(len(collection)) + " BEARS")
        for thing in collection:
            print("Name: " + str(thing.name) + " Speed: " + str(thing.speed) + " Sense_fear: " + str(thing.sense_fear) + " Is_dead: " + str(thing.is_dead ) + " Age: " + thing.age.name)
    
    def print_predator_stats(self, collection):
        print("\nSTATISTICS FOR " + str(len(collection)) + " PREDATORS")
        for thing in collection:
            print("Name: " + str(thing.name) + " Speed: " + str(thing.speed) + " Is_dead: " + str(thing.is_dead) + " Age: " + thing.age.name)
    
    def print_fruit_stats(self, collection):
        print("\nSTATISTICS FOR " + str(len(collection)) + " FRUITS")
        # for thing in collection:
        #     print("Name: " + str(thing.name) + " Speed: " + str(thing.speed))