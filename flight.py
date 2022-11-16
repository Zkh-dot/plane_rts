from math import sqrt, sin, cos, pi

def pif(a = 0, b = 0, c = 0):
    return sqrt(a ** 2 + b ** 2 + c ** 2)


def crashReport(text='ну тут и сказать нечего'):
    print('booom!')
    print(text)

class Plain:
    def __init__(self, properties = {'wingsCapacity': 10}, location = {'x': 0, 'y': 0, 'z': 0}, speed = {'x': 0, 'y': 0, 'z': 0}, acs = {'x': 0, 'y': 0, 'z': 0}):
        self.properties = properties
        self.angleup = 0
        self.anglehor = 0
        self.speed = speed
        self.acs = acs
        self.location = location

    def turn(self, g = 2):
        for i in self.speed.keys():
            try:
                self.speed[i] += self.acs[i] - (abs(self.speed[i]) // self.speed[i]) * g // 2
            except:
                self.speed[i] += self.acs[i]
        
        self.speed['z'] -=  g 
        

        self.location['x'] += self.speed['x']
        self.location['y'] += self.speed['y']
        windLiftMoment = (sqrt((sqrt(2) / 2 * self.speed['x']) ** 2 + (sqrt(2) / 2 * self.speed['y']) ** 2)) // self.properties['wingsCapacity']
        self.location['z'] += self.speed['z'] + windLiftMoment

    
    def calculate(self, angleUp, angleHorisontal, speed):
        angleUp *= pi
        angleHorisontal *= pi
        self.angleup += angleUp
        self.anglehor += angleHorisontal
        self.angleup %= 2 * pi
        self.anglehor %= 2 * pi
        self.acs['x'] = round(speed * cos(self.anglehor) * cos(self.angleup))
        self.acs['y'] = round(speed * sin(self.anglehor) * cos(self.angleup))
        self.acs['z'] = round(speed * sin(self.angleup))

    def isOk(self):
        if self.location['z'] < -3:
            crashReport('Скорость сближения... а, уже не важно')
            
        elif self.location['z'] <= 0:
            if pif(self.speed['x'], self.speed['y'], self.speed['z']) > 5:
                crashReport('Куда торопился то так?')
                return False
            elif self.angleup < 0 or self.angleup > 0.25 * pi:
                crashReport('Нос по ветру, брат...')
                return False
            print('landed')
            self.speed = {'x': 0, 'y': 0, 'z': 0}
            self.location['z'] = 0
        return True


def testLaunch():
    plaineOne = Plain()

    while(True):
        up = float(input())
        if up != -1:
            hor = float(input())
            speed = int(input())
        else:
            hor = 0
            speed = 0
            up = 0
        plaineOne.calculate(up, hor, speed)
        plaineOne.turn()
        if(plaineOne.isOk()):
            print(plaineOne.location)
            print('speed =', pif(plaineOne.speed['x'], plaineOne.speed['y'], plaineOne.speed['z']))
            print('vector =', plaineOne.angleup / pi, plaineOne.anglehor / pi)
        else:
            break


if __name__ == "__main__":
    testLaunch()
    
        

