from math import sqrt, sin, cos, pi
from numpy import cross

def pif(a = 0, b = 0, c = 0):
    return sqrt(a ** 2 + b ** 2 + c ** 2)


def crashReport(text='ну тут и сказать нечего'):
    print('booom!')
    print(text)

class Plain:
    def __init__(self, 
            properties = {'wingsCapacity': 10, 'overloadSpeed': 10}, 
            location = {'x': 0, 'y': 0, 'z': 0}, 
            speed = {'x': 0, 'y': 0, 'z': 0}, 
            acs = {'x': 0, 'y': 0, 'z': 0}, 
            name = 'somePlane'):
        self.name = name
        self.properties = properties
        self.angleup = 0
        self.anglehor = 0
        self.speed = speed
        self.acs = acs
        self.location = location
        self.noseDir = {'x': 0, 'y': 0, 'z': 0}

    def move(self, g = 2):
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

    def isOk(self, isShot = False):
        if isShot:
            crashReport('9 граммов свинца кажутся хорошей участью по сравнению с твоей, брат...')
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
        #   x0 = obj[x]     
        #   кринж ли это? да, конечно, но шо поделать
        #   upd: текущая версия не кринж, текущая версия заебок
        #print(self.acs)
        a = [self.noseDir['x'] * range, self.noseDir['y'] * range, self.noseDir['z'] * range]
        aLength = pif(a[0], a[1], a[2])
        m3m1 = [obj['x'] - self.location['x'], obj['y'] - self.location['y'], obj['z'] - self.location['z']]
        #print(a, m3m1, cross(a, m3m1))
        ans = cross(a, m3m1)
        axm3m1 = pif(ans[0], ans[1], ans[2])
        try:
            return axm3m1 / aLength
        except Exception():
            print('Кажется, вы забыли сделать calculate перед выстрелом. Ну или просто что-то ебнулось')
            return 10000000
        
    def shoot(self, aim, range = 100, accur = 3):
        self.calculate(0, 0, 0)     #   приводим нос в актуальное положение
        if self.lookForvared(range, aim.location) <= accur:
            print(aim.name, 'уничтожен! Пау-пау-пау!')
            aim.isOk(True)
        else:
            return False

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
        if not plaineOne.move(): 
            return False
        print('расстояние =', plaineOne.lookForvared())
        if(plaineOne.isOk()):
            print(plaineOne.location)
            print('range =', plaineOne.lookForvared())
            print('speed =', pif(plaineOne.speed['x'], plaineOne.speed['y'], plaineOne.speed['z']))
            print('vector =', plaineOne.angleup / pi, plaineOne.anglehor / pi)
            print('vectorV2:', end=" ")
            for i in plaineOne.noseDir.keys():
                print(i, '=', plaineOne.noseDir[i], end=', ')
        else:
            break



if __name__ == "__main__":
    pass
    testLaunch()
    #pln = Plain()
    #pln.calculate(0, 0, 0)
    #print(pln.lookForvared(int(input()), {'x': int(input()), 'y': int(input()), 'z': int(input())}))