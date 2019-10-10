import math

def reader(target):
    json_data = open(target).read()
    return json.loads(json_data)

GunDB = reader('Guns.json')
ShipDB = reader('Ships.json')

sequence = [0.18,0.31,0.475,0.695,1]

research_multipliers = {
    "Ships": {
        "OE": [[6, 6, 6, 6, 6], [10.5, 10.5, 10.5, 10.5, 10.5], [13.5, 13.5, 13.5, 13.5, 13.5]],
        "NEF": [[6, 6, 6, 6, 6], [10.5, 10.5, 10.5, 10.5, 10.5], [13.5, 13.5, 13.5, 13.5, 13.5]],
        "ECD": [[6, 6, 6, 6, 6], [10.5, 10.5, 10.5, 10.5, 10.5], [13.5, 13.5, 13.5, 13.5, 13.5]],
        "RS": [[6, 6, 6, 6, 6], [10.5, 10.5, 10.5, 10.5, 10.5], [13.5, 13.5, 13.5, 13.5, 13.5]]
    },
    "Weapons": {
        'Blasters': [[1.8, 1.8, 1.8], [3, 3, 3], [4,4,4]],
        'BlastersAdv': [[10, 2, 3], [17.5, 3.5, 5], [22.5, 4.5, 7]],
        'Lasers': [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
        'LasersAdv': [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
        'Railguns': [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
        'RailgunsAdv': [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
        'Missiles': [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
        'MissilesAdv': [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
        'General': [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
        'Artillery': [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    },
    'Engineering': {
        'Ship Core': [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
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

research_effects = {
    "Ships": {
        "OE": [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]],
        "NEF": [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]],
        "ECD": [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]],
        "RS": [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]
    },
    "Weapons": {
        'Blasters': [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
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
    'Engineering': {
        'Ship Core': [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
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

class Ship():
    def __init__(self,db,char):
        self.db = db
        self.char = char
        self.applySkills(self.char)
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
        self.cargo = self.db['cargo']
        self.artillery = self.db['artillery']
        self.dps = 0
        self.devices = []
        self.guns = []
        self.devCap = 2
        self.components = []
        self.gunNames = []
        self.addGun(self.artillery)
        self.attributes = [self.armor,self.shield,self.processor,self.power,self.resistances,self.warpStab,self.warpSpeed,self.speed,self.energy,self.recovery,self.agility,self.volume,self.shieldRecovery,self.cargo]
    def applySkills(self,char):
        self.reset()
        if char.researches()['Ships'][self.race][0][self.type] > 3:
            self.devCap = 3
            if char.researches()['Ships'][self.race][0][self.type] > 5:
                self.comCap = self.comCap + 1
    def addGun(self,gundb):
        gun = Gun(gundb,self.char)
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
    def dps(self):
        return(sum([gun.dps() for gun in self.guns]))
    def dpsResist(self,resist):
        return(sum([gun.dpsResist(resist) for gun in self.guns]))
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
    def ammoTime(self):
        times = [gun.ammoTime() for gun in self.guns]
        return min(times)


TestShipDB = {
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
            "tech" : 0,
            "rank" : 0,
            "damage" : 18,
            "damages" : [6,6,6],
            "cooldown" : 1,
            "range" : 9,
            'precision' : 0,
            "tracking" : 0,
            "critChance" : 0,
            "critDmg" : 0,
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
TestGunDB = {
    "artillery": {
        "damage": 18,
        "damages": [6,6,6,],
        "cooldown": 1,
        "range": 9,
        'precision': 0,
        "tech": 0,
        "rank": 0,
        "tracking": 0,
        "critChance": 0,
        "critDmg": 0,
        "activation": 0,
        "ammo": 0,
        "ammoUsage": 1,
        "processor": 0,
        "power": 0,
        "type": 0,
        "name": "Frigate Std Artillery"
    },
    "S-Combat Railgun I 1": {
        "damage": 124,
        "damages": [31,93,0],
        "cooldown": 4,
        "range": 12.5,
        "critChance": 10.0,
        "critDmg" : 2,
        "precision": 71.4,
        "tracking": 700,
        "activation": 41,
        "ammo": 450,
        "ammoUsage": 1,
        "processor": 42,
        "power": 23,
        "tech": 1,
        "type": 1,
        "rank": 1,
        "name": "S-Combat Railgun I 1"
    }
}

class Character:
    def __init__(self):
        self.research = {
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
        self.skill = {
            "Weapon":{
                "Railgun":[[0,0,0],[0,0,0],[0,0,0]],
                "Launcher":[[0,0,0],[0,0,0],[0,0,0]],
                "Laser":[[0,0,0],[0,0,0],[0,0,0]],
                "Blaster":[[0,0,0],[0,0,0],[0,0,0]]
                },
            "Defense":{
                "Resistance": [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
                "Recharge": [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
            },
            "Electronics": {
                "Energy": [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
                "Recharge": [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
            },
            "Ship Piloting":{
                "Propulsion": [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
            }
        }
    def skills(self):
        return self.skill
    def researches(self):
        return self.research

clean = Character()

class Gun():
    def __init__(self,db,char):
        self.db = db
        self.applySkills(char)
    def applySkills(self,char):
        self.reset()
    def reset(self):
        self.damage =  self.db['damage']
        self.damages = self.db['damages']
        self.cooldown =  self.db['cooldown']
        self.range =  self.db['range']
        self.precision =  self.db['precision']
        self.tracking =  self.db['tracking']
        self.activation =  self.db['activation']
        self.ammo =  self.db['ammo']
        self.tech = self.db['tech']
        self.rank = self.db['rank']
        self.ammoUsage =  self.db['ammoUsage']
        self.processor =  self.db['processor']
        self.power =  self.db['power']
        self.type =  self.db['type']
        self.critChance = self.db['critChance']/10
        self.critDmg = self.db['critDmg']
        self.name = self.db['name']
    def namer(self):
        return(self.name)
    def fitting(self):
        return([self.processor,self.power])
    def dps(self):
        if self.damages:
            return(((sum(self.damages)/self.cooldown)*(1-self.critChance)) + ((sum(self.damages)/self.cooldown)*(self.critChance*self.critDmg)))
        else:
            return (((self.damage / self.cooldown) * (1 - self.critChance)) + ((self.damage / self.cooldown) * (self.critChance * self.critDmg)))
    def dpsResist(self,resist):
        if self.damages:
            one = (((self.damages[0]/self.cooldown)*(1-self.critChance)) + ((self.damages[0]/self.cooldown)*(self.critChance*self.critDmg)))*(1-resist[0])
            two = (((self.damages[1]/self.cooldown)*(1-self.critChance)) + ((self.damages[1]/self.cooldown)*(self.critChance*self.critDmg)))*(1-resist[1])
            three = (((self.damages[2]/self.cooldown)*(1-self.critChance)) + ((self.damages[2]/self.cooldown)*(self.critChance*self.critDmg)))*(1-resist[2])
            return(one+two+three)
        else:
            return (((self.damage / self.cooldown) * (1 - self.critChance)) + ((self.damage / self.cooldown) * (self.critChance * self.critDmg)))
    def drain(self):
        return(self.activation/self.cooldown)
    def ammoTime(self):
        if self.ammo == 0:
            return math.inf
        else:
            return((self.ammo/self.ammoUsage)*self.cooldown)

class Device():
    def __init__(self,db,char):
        self.db = db
        self.applySkills(char)
    def applySkills(self):
        self.reset()
    def reset(self):
        self.processor = self.db['processor']
        self.power = self.db['power']
        self.tech = self.db['tech']
        self.rank = self.db['rank']
        self.type = self.db['type']
        self.effect = self.db['effect']
        self.activation = self.db['activation']
        self.cooldown = self.db['cooldown']
        self.effectTime = self.db['effectTime']

class Component():
    def __init__(self,db,char):
        self.db = db
        self.applySkills(char)
    def applySkills(self):
        self.reset()
    def reset(self):
        self.processor = self.db['processor']
        self.power = self.db['power']
        self.tech = self.db['tech']
        self.rank = self.db['rank']
        self.type = self.db['type']
        self.effect = self.db['effect']

myship = Ship(TestShipDB['Covert'],clean)
myship.addGun(TestGunDB['S-Combat Railgun I 1'])
myship.addGun(TestGunDB['S-Combat Railgun I 1'])
myship.addGun(TestGunDB['S-Combat Railgun I 1'])
print(myship.dpsResist([0.5,0.5,0.5]))
print(myship.dps)