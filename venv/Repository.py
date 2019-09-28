class Ship():
    def __init__(self,db,char):
        self.db = db
        self.applySkills(char)
    def reset(self):
        self.type = self.db['type']
        self.race = self.db['race']
        self.tech = self.db['tech']
        self.armor = self.db['armor']
        self.shield =  self.db['shield']
        self.processor =  self.db['processor']
        self.power =  self.db['power']
        self.comCap = self.db['comCap']
        self.resistances =  self.db['resistances']
        self.warpStab =  self.db['warpStab']
        self.warpSpeed =  self.db['warpSpeed']
        self.speed =  self.db['speed']
        self.energy = self.db['energy']
        self.recovery =  self.db['energyRecovery']
        self.agility =  self.db['agility']
        self.volume =  self.db['volume']
        self.shieldRecovery =  self.db['shieldRecovery']
        self.artillery = Gun(self.db['artillery'])
        self.dps = 0
        self.devices = []
        self.guns = []
        self.devCap = 2
        self.components = []
        self.gunNames = []
        self.addGun(self.artillery)
    def applySkills(self,char):
        self.reset()
        if char.skills()['Ships'][self.race][0][self.type] > 3:
            self.devCap = 3
            if char.skills()['Ships'][self.race][0][self.type] > 5:
                self.comCap = self.comCap + 1
    def addGun(self,gun):
        fitting = gun.fitting()
        processr = self.processor - fitting[0]
        powr = self.power - fitting[1]
        if powr < 0:
            print('Not enough Power')
            return null
        if processr < 0:
            print('Not enough Processor')
            return null
        if (len(self.guns) < 4):
            self.power = powr
            self.processor = processr
            self.guns.append(gun)
            self.gunNames.append(gun.namer())
            self.dps = self.dps + gun.dps()
    def addDevice(self,device):
        fitting = device.fitting()
        processr = processor - fitting[0]
        powr = power - fitting[1]
        if powr < 0:
            print('Not enough Power')
            return null
        if processr < 0:
            print('Not enough Processor')
            return null
        if len((devices) < self.devCap):
            power = powr
            processor = processr
            devices.append(device)
        else:
            print("Not enough device slots")


ShipDB = {
    "Covert": {
        "type" : 0,
        'tech' : 0,
        "race" : "OE",
        "armor" : 1760,
        "shield" : 1876,
        "processor" : 243,
        "power" : 107,
        "comCap" : 1,
        "resistances" : [0.3,0.1,0.5], #EM,KINETIC,THERMAL
        "warpStab" : 2,
        "warpSpeed" : 10.58,
        "speed" : 688,
        "energy" : 1241,
        "energyRecovery" : 12,
        "agility" : 693,
        "volume" : 140,
        "shieldRecovery": 1,
        "artillery" : {
            "damage" : 18,
            "damages" : False,
            "cooldown" : 1,
            "range" : 9,
            'precision' : 0,
            "tracking" : 0,
            "activation" : 0,
            "ammo" : 0,
            "ammoUsage" : 1,
            "processor" : 0,
            "power" : 0,
            "type" : 0,
            "name" : "Frigate Std Artillery"
        }

    }
}
GunDB = {

}

class Character:
    def __init__(self):
        self.skill = {
            "Ships": {
                "OE" : [[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]],
                "NEF" : [[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]],
                "ECD" : [[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]],
                "RS" :[[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]]
            },
            "Weapons":{
                'Blasters' : [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
                'BlastersAdv': [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
                'Lasers': [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
                'LasersAdv': [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
                'Railguns': [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
                'RailgunsAdv': [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
                'Missiles': [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
                'MissilesAdv': [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
                'General': [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
                'Artillery': [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
            },
            'Engineering':{
                'Ship Core' : [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
                'Energy Basics': [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
                'Energy Adv': [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
                'Shield Basics': [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
                'Shield Adv': [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
                'Resistance Basics': [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
                'Resistance Adv': [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
                'Tactical Shield': [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
                'Propulsion Basics': [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
                'Propulsion Adv': [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
            }
        }
    def skills(self):
        return self.skill

clean = Character()

class Gun():
    def __init__(self, db):
        self.damage =  db['damage']
        self.damages = db['damages']
        self.cooldown =  db['cooldown']
        self.range =  db['range']
        self.precision =  db['precision']
        self.tracking =  db['tracking']
        self.activation =  db['activation']
        self.ammo =  db['ammo']
        self.ammoUsage =  db['ammoUsage']
        self.processor =  db['processor']
        self.power =  db['power']
        self.type =  db['type']
        self.name = db['name']
    def namer(self):
        return(self.name)
    def fitting(self):
        return([self.processor,self.power])
    def dps(self):
        if self.damages:
            return(sum(self.damages)/self.cooldown)
        else:
            return(self.damage/self.cooldown)
    def dpsResist(self,resist):
        alpha = (self.damage[0]*(1-resist[0]) + self.damage[1]*(1-resist[1]) + self.damage[2]*(1-resist[3]))
        return(alpha/self.cooldown)
    def drain(self):
        return(self.activation/self.cooldown)
    def ammoTime(self):
        if self.ammo == 0:
            return 0
        else:
            return((self.ammo/self.ammoUsage)*self.cooldown)

class Device():
    def __init__(self, db):
        effects =  db['effects']
        processor =  db['processor']
        power =  db['power']
        limits =  db['limits']
    def fitting(self):
        return([processor,power])

myship = Ship(ShipDB['Covert'],clean)
print (myship.dps)
print(myship.gunNames)