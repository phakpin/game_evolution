class Conf():
    DEFAULT_SIZE = 30

    NUMBER_OF_BEARS = 14
    NUMBER_OF_PREDATORS = 7

    INITIAL_RENEW_BERRIES = 15
    NUMBER_OF_BERRIES = 4

    # PREEDATOR_INITIAL_SPEED = 2.3 #3 is good value
    INITIAL_SPEED = 2

    TIMER_RENEW_BERRIES = 500
    TIMER_RENEW_BERRIES_TREE = 1000

    THING_LIVE_TIME = 3600*3 #3600 is a one minute
    OLD_AGE = THING_LIVE_TIME  - (3 * THING_LIVE_TIME / 4)
    ADULT_AGE = THING_LIVE_TIME  - (1 * THING_LIVE_TIME / 4)
    
    LIVE_WITHOUT_BERRY = 2600
    LIVE_FROM_BERRY = 2500
    LIVE_FROM_CORRION = 2000
    LIVE_FROM_EGG = 600

    LIVE_WITHOUT_MEAT = 2400
    LIVE_FROM_MEAT = 3500

    BERRY_EXIST = 2000
    MEAT_EXITS = 2000

    DEAD_BODY_EXIST = 1000

    COPULE_TIME_BEAR = 200
    COPULE_TIME_PREDATOR = 700

    EGG_TIME = 1000

    BEAR_SENSE_FEAR = 80
    BEAR_SENSE_FOOD = 60
    BEAR_SENSE_COPULE = 60
    
    SIGHT_RANGE = 120

    SENSE_PREDATOR = 52
    SENSE_CARRION = 60
    SENSE_EGG = 60

    FORCE_PREDATOR = 0.5
    FORCE_BEAR = 0.2

    TREE_GROWING = 3000
    TREE_EXIST = 10000

