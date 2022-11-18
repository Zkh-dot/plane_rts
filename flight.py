from math import sqrt, sin, cos, pi

def pif(a = 0, b = 0, c = 0):
    return sqrt(a ** 2 + b ** 2 + c ** 2)


def crashReport(text='ну тут и сказать нечего'):
    print('booom!')
    print(text)

class Plain:
    def __init__(self, properties = {'wingsCapacity': 10, 'overloadSpeed': 10}, location = {'x': 0, 'y': 0, 'z': 0}, speed = {'x': 0, 'y': 0, 'z': 0}, acs = {'x': 0, 'y': 0, 'z': 0}):
        self.properties = properties
        self.angleup = 0
        self.anglehor = 0
        self.speed = speed
        self.acs = acs
        self.location = location
        self.noseDir = {'x': 0, 'y': 0, 'z': 0}

    def turn(self, g = 2):
        speedLambda = 0
        for i in self.speed.keys():
            try:
                self.speed[i] += self.acs[i] - (abs(self.speed[i]) // self.speed[i]) * g // 2
                speedLambda += (self.acs[i] - (abs(self.speed[i]) // self.speed[i]) * g // 2) ** 2
            except:
                speedLambda += self.acs[i]
                self.speed[i] += self.acs[i]
        try:
            if sqrt(speedLambda) > self.properties['overloadSpeed']:
                crashReport('Чет ты себя перегрузил, брат...')
                return False
        except Exception as e:
            print('Что-то случилось, мы не уверены что')
            print(e)
        
        self.speed['z'] -=  g 
        
        self.location['x'] += self.speed['x']
        self.location['y'] += self.speed['y']
        windLiftMoment = (sqrt((sqrt(2) / 2 * self.speed['x']) ** 2 + (sqrt(2) / 2 * self.speed['y']) ** 2)) // self.properties['wingsCapacity']
        self.location['z'] += self.speed['z'] + windLiftMoment

        return True

    
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
        self.noseDir['x'] = round(cos(self.anglehor) * cos(self.angleup)) 
        self.noseDir['y'] = round(sin(self.anglehor) * cos(self.angleup)) 
        self.noseDir['z'] = round(sin(self.angleup))

    def isOk(self):
        if self.location['z'] < -3:
            crashReport('Скорость сближения... а, уже не важно')
            return False
            
        elif self.location['z'] <= 0:
            if pif(self.speed['x'], self.speed['y'], self.speed['z']) > 5:
                crashReport('Куда торопился то так?')
                return False
            elif self.angleup < 0 or self.angleup > 0.25 * pi:
                crashReport('Нос по ветру, брат...')
                return False
            print('landed')
            self.angleup = 0
            self.speed = {'x': 0, 'y': 0, 'z': 0}
            self.location['z'] = 0
        return True

    def lookForvared(self, range = 100, obj = {'x': 0, 'y': 0, 'z': 0}):
        #   self.acs - это направление носа, сторону которого ведется стрельба
        #   сперва происходит calculate, потом lookForvared
        #   можно конечно сперва двгать нос, потом менять скорость, потом стрелять
        #   но я бы наверное сделал опциональный вызов выстрела и там и там, например
        #   x0 = obj[x]     xa = self.location['x']     xb = (self.location['x'] + self.noseDir['x']) * range
        #   кринж ли это? да, конечно, но шо поделать
        #print(self.acs)
        tUpPart = 0
        tDownPart = 0
        for i in obj.keys():
            tUpPart += (obj[i] - self.location[i]) * ((self.location[i] + self.noseDir[i]) * range)
            tDownPart += (((self.location[i] + self.noseDir[i]) * range) - self.location[i]) ** 2
        tFull = tUpPart / tDownPart
        disInPowerTwo = 0
        for i in obj.keys():
            disInPowerTwo += ((self.location[i] - obj[i] + (((self.location[i] + self.noseDir[i]) * range) - self.location[i])) * tFull) ** 2
        distance = sqrt(disInPowerTwo)
        return distance

def testLaunch():
    plaineOne = Plain()

    while(True):
        up = input()
        if up == 'q':
            up = pUp
        elif up != 'p':
            up = float(up)
            pUp = up
            hor = float(input())
            speed = int(input())
        else:
            hor = 0
            speed = 0
            up = 0
        plaineOne.calculate(up, hor, speed)
        if not plaineOne.turn(): 
            return False
        print('расстояние =', plaineOne.lookForvared())
        if(plaineOne.isOk()):
            print(plaineOne.location)
            print('speed =', pif(plaineOne.speed['x'], plaineOne.speed['y'], plaineOne.speed['z']))
            print('vector =', plaineOne.angleup / pi, plaineOne.anglehor / pi)
        else:
            break


if __name__ == "__main__":
    testLaunch()