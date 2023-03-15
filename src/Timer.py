class Timer():
    def __init__(self, value = 0):
        self.Time = value

    def set_timer(self, value):
        self.Time = value
    
    def update(self):
        if self.Time > 0:
            self.Time -= 1

    def is_on(self):
        if self.Time > 0:
            return True
        return False

    def disable_timer(self):
        self.Time = 0

    def get_time(self):
        return self.Time

class Timer_Live(Timer):
    def __init__(self):
        super().__init__()

    def update(self, value):
        if self.Time > 0:
            self.Time -= value

    def eat(self, value):
        self.Time += value

    def is_starve(self):
        if self.Time < 1000:
            return True
        else:
            return False

class Timer_Whole_Live(Timer):

    def get_current_live_time(self):
        return self.Time



