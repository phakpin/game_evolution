import math
from src.const import Const

class Utils():

    def GetDist(self,bear,predator):
        return math.sqrt(pow(bear.rect.center[0] - predator.rect.center[0], 2) + pow(bear.rect.center[1] - predator.rect.center[1], 2))

    def IsCollision(self, a, b):
        dist = self.GetDist(a,b)
        contact = (a.size/2) + (b.size/2)
        if dist < contact:
            return True
        else:
            return False

    def GetReversePoint(self,bear,predator):
        A = predator.rect.center[0] - bear.rect.center[0]
        B = predator.rect.center[1] - bear.rect.center[1]

        return [bear.rect.center[0] + (A*(-1)), bear.rect.center[1] + (B*(-1))]

    def KeepPointInRange(self,point):
        point[0] = self.ValueInRange(point[0])
        point[1] = self.ValueInRange(point[1])
        return point

    def ValueInRange(self, value):
        if(value < 0):
            value = 0 + 10
        if(value > Const.SCREEN_SIZE):
            value = Const.SCREEN_SIZE - 10
        return value

    def GetDistPoints(self, point1, point2):
        return math.sqrt(pow(point1[0] - point2[0], 2) + pow(point1[1] - point2[1], 2))