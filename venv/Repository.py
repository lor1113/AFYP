import math
import json
import copy

def reader(target):
    json_data = open(target).read()
    return json.loads(json_data)

def find(code, dict):
    keys = code.split('.')
    rv = dict
    for key in keys:
        try:
            rv = rv[key]
        except:
            rv = rv[int(key)]
    return rv

GunDB = reader('Guns.json')
ShipDB = reader('Ships.json')

buff_matrix = {}
research_sequence = [0,0.18,0.31,0.475,0.695,1]
skill_sequence = [0,1,2,3,4,5,6,7,8,9,10]
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
        'Lasers': [[1.8, 1.8, 1.8], [3, 3, 3], [4,4,4]],
        'LasersAdv': [[10, 2, 3], [17.5, 3.5, 5], [22.5, 4.5, 7]],
        'Railguns': [[1.8, 1.8, 1.8], [3, 3, 3], [4,4,4]],
        'RailgunsAdv': [[10, 2, 3], [17.5, 3.5, 5], [22.5, 4.5, 7]],
        'Missiles': [[1.8, 1.8, 1.8], [3, 3, 3], [4,4,4]],
        'MissilesAdv': [[10, 2, 3], [17.5, 3.5, 5], [22.5, 4.5, 7]],
        'General': [[10, 2, 2], [17.5, 3.5, 3.5], [22.5, 4.5, 4.5]],
        'Artillery': [[10, 2, 2], [17.5, 3.5, 5.25], [22.5, 4.5, 6.75]]
    },
    'Engineering': {
        'Ship Core': [[6, 5, 5], [10.5, 8.75, 8.75], [13.5, 11.25, 11.25]],
        'Energy Basics': [[3, 3, 6], [5.25, 5.25, 10.5], [6.75, 6.75, 13.5]],
        'Energy Adv': [[3, 2, 6], [5.25, 3.5, 10.5], [6.75, 4.5, 13.5]],
        'Shield Basics': [[8, 4, 4], [14, 7, 7], [18, 9, 9]],
        'Shield Adv': [[3, 2, 6], [5.25, 3.5, 10.5], [6.75, 4.5, 13.5]],
        'Resistance Basics': [[6, 6, 6], [10.5, 10.5, 10.5], [13.5, 13.5, 13.5]],
        'Resistance Adv': [[3, 3, 3], [5.25, 5.25, 5.25], [6.75, 6.75, 6.75]],
        'Tactical Shield': [[4, 4, 2], [7, 7, 3.5], [9, 9, 4.5]],
        'Propulsion Basics': [[4, 2, 5], [7, 3.5, 8.75], [9, 4.5, 11.25]],
        'Propulsion Adv': [[3, 3, 4], [5.25, 5.25, 7], [6.25, 6.25, 9]],
        'Jump Engine': [[0, 0, 4], [0, 0, 7], [0, 0, 9]]
    },
    'Electronics': {
        'Weapon Reinforcement': [[3, 3, 3, 3], [5.25, 5.25, 5.25, 5.25], [6.75, 6.75, 6.75, 6.75]],
        'Fire-Control Reinforcement': [[3, 3, 3, 3], [5.25, 5.25, 5.25, 5.25], [6.75, 6.75, 6.75, 6.75]],
        'Core Suppression': [[3, 3, 3, 3], [5.25, 5.25, 5.25, 5.25], [6.75, 6.75, 6.75, 6.75]],
        'Weapon Suppression': [[3, 3, 3, 3], [5.25, 5.25, 5.25, 5.25], [6.75, 6.75, 6.75, 6.75]],
        'Fire-Control Suppression': [[3, 3, 3, 3], [5.25, 5.25, 5.25, 5.25], [6.75, 6.75, 6.75, 6.75]],
        'Propulsion Suppression': [[3, 3, 3, 3], [5.25, 5.25, 5.25, 5.25], [6.75, 6.75, 6.75, 6.75]],
        'Directional Scanning': [[13.2, 13.2, 13.2], [23.05, 23.05, 23.05], [29.75, 29.75, 29.75]]
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
        'Blasters': [[731, 721, 711], [731, 721, 711], [731, 721, 711]],
        'BlastersAdv': [[74, 73, 72], [74, 73, 72], [74, 73, 72]],
        'Lasers': [[631, 621, 611], [631, 621, 611], [631, 621, 611]],
        'LasersAdv': [[64, 63, 62], [64, 63, 62], [64, 63, 62]],
        'Railguns': [[931, 921, 911], [931, 921, 911], [931, 921, 911]],
        'RailgunsAdv': [[94, 93, 92], [94, 93, 92], [94, 93, 92]],
        'Missiles': [[831, 821, 811], [831, 821, 811], [831, 821, 811]],
        'MissilesAdv': [[84, 83, 82], [84, 83, 82], [84, 83, 82]],
        'General': [[55, 56, 54], [55, 56, 54], [55, 56, 54]],
        'Artillery': [[104, 103, 102], [104, 103, 102], [104, 103, 102]]
    },
    'Engineering': {
        'Ship Core': [[1, 4, 5], [1, 4, 5], [1, 4, 5]],
        'Energy Basics': [[[5201,6201], 10, 9], [[5201,6201], 10, 9], [[5201,6201], 10, 9]],
        'Energy Adv': [[[4202,5202,6202], [4203,5203,6203], [4201,5201,6201]], [[4202,5202,6202], [4203,5203,6203], [4201,5201,6201]], [[4202,5202,6202], [4203,5203,6203], [4201,5201,6201]]],
        'Shield Basics': [[[5101,6101], 13, 2], [[5101,6101], 13, 2], [[5101,6101], 13, 2]],
        'Shield Adv': [[[4102,5102,6102], [4103,5103,6103], [4101,5101,6101]], [[4102,5102,6102], [4103,5103,6103], [4101,5101,6101]], [[4102,5102,6102], [4103,5103,6103], [4101,5101,6101]]],
        'Resistance Basics': [[33, 32, 31], [33, 32, 31], [33, 32, 31]],
        'Resistance Adv': [[[2114,2124,2134,3114,3124,3134], [1313,1323,1333,1403,2113,2123,2133,2203,3113,3123,3133,3203], [1314,1324,1334,1404,2114,2124,2134,2204,3114,3124,3134,3204]], [[2114,2124,2134,3114,3124,3134], [1313,1323,1333,1403,2113,2123,2133,2203,3113,3123,3133,3203], [1314,1324,1334,1404,2114,2124,2134,2204,3114,3124,3134,3204]], [[2114,2124,2134,3114,3124,3134], [1313,1323,1333,1403,2113,2123,2133,2203,3113,3123,3133,3203], [1314,1324,1334,1404,2114,2124,2134,2204,3114,3124,3134,3204]]],
        'Tactical Shield': [[7202, 7302, 12], [7202, 7302, 12], [7202, 7302, 12]],
        'Propulsion Basics': [[11, 8, 7], [11, 8, 7], [11, 8, 7]],
        'Propulsion Adv': [[[2302,3302], [2303,3303], [15,1101]], [[2302,3302], [2303,3303], [15,1101]], [[2302,3302], [2303,3303], [15,1101]]],
        'Jump Engine': [[0, 0, [7111,7112,7113]], [0, 0, [7111,7112,7113]], [0, 0, [7111,7112,7113]]]
    },
    'Electronics': {
        'Weapon Reinforcement': [[[1532,2432],[1533,2433],[1512,2412],[1513,2413]], [[1532,2432],[1533,2433],[1512,2412],[1513,2413]], [[1532,2432],[1533,2433],[1512,2412],[1513,2413]]],
        'Fire-Control Reinforcement': [[[1522,2422],[1523,2423],[1542,2442],[1543,2443]], [[1522,2422],[1523,2423],[1542,2442],[1543,2443]], [[1522,2422],[1523,2423],[1542,2442],[1543,2443]]],
        'Core Suppression': [[[8104,8114,8124,8134,9104,9114,9124,9134],[8103,8113,8123,8133,9103,9113,9123,9133],[8904,9904],[8903,9903]], [[8104,8114,8124,8134,9104,9114,9124,9134],[8103,8113,8123,8133,9103,9113,9123,9133],[8904,9904],[8903,9903]], [[8104,8114,8124,8134,9104,9114,9124,9134],[8103,8113,8123,8133,9103,9113,9123,9133],[8904,9904],[8903,9903]]],
        'Weapon Suppression': [[[8804,9804], [8803,9903], [8504,9504], [8503,9503]], [[8804,9804], [8803,9903], [8504,9504], [8503,9503]], [[8804,9804], [8803,9903], [8504,9504], [8503,9503]]],
        'Fire-Control Suppression': [[[8604,9604], [8603,9603], [8704,9704], [8703,9703]], [[8604,9604], [8603,9603], [8704,9704], [8703,9703]], [[8604,9604], [8603,9603], [8704,9704], [8703,9703]]],
        'Propulsion Suppression': [[[8404,9404], [8403,9403], [8304,9304], [8303,9303]], [[8404,9404], [8403,9403], [8304,9304], [8303,9303]], [[8404,9404], [8403,9403], [8304,9304], [8303,9303]]],
        'Directional Scanning': [[7411, 7421, 7431], [7411, 7421, 7431], [7411, 7421, 7431]]
    }
}

skill_multipliers = {
    "Weapon": {
        "Railgun": [[0.34, 0.34, 0.34], [0.45, 0.45, 0.45], [0.8, 0.8, 0.8]],
        "Launcher": [[0.34, 0.34, 0.34], [0.45, 0.45, 0.45], [0.8, 0.8, 0.8]],
        "Laser": [[0.34, 0.34, 0.34], [0.45, 0.45, 0.45], [0.8, 0.8, 0.8]],
        "Blaster": [[0.34, 0.34, 0.34], [0.45, 0.45, 0.45], [0.8, 0.8, 0.8]]
    },
    "Defense": {
        "Resistance": [[0.68, 0.68, 0.68], [1.2, 1.2, 1.2], [2.12, 2.12, 2.12]],
        "Recharge": [[0.765, 0.255], [1.35, 0.45], [2.39, 0.8]]
    },
    "Electronics": {
        "Recharge": [[0.765, 0.255, 0.765], [1.35, 0.45, 1.35], [2.39, 0.8, 2.39]],
        "Energy": [[0.255, 0.51], [0.45, 0.9], [0.8, 1.59]]
    },
    "Ship Piloting": {
        "Propulsion": [[0.51, 0.34, 0.51], [0.9, 0.6, 0.9], [1.59, 1.06, 1.59]]
    }
}

skill_effects = {
    "Weapon": {
        "Railgun": [[92, 96, 93], [92, 96, 93], [92, 96, 93]],
        "Launcher": [[82, 86, 83], [82, 86, 83], [82, 86, 83]],
        "Laser": [[62, 66, 63], [62, 66, 63], [62, 66, 63]],
        "Blaster": [[72, 76, 73], [72, 76, 73], [72, 76, 73]]
    },
    "Defense": {
        "Resistance": [[31, 32, 33], [31, 32, 33], [31, 32, 33]],
        "Recharge": [[4101, 4102], [4101, 4102], [4101, 4102]]
    },
    "Electronics": {
        "Recharge": [[4201, 4202, 10], [4201, 4202, 10], [4201, 4202, 10]],
        "Energy": [[57, 4103], [57, 4103], [57, 4103]]
    },
    "Ship Piloting": {
        "Propulsion": [[[1101,1201,15], 7, 12], [[1101,1201,15], 7, 12], [[1101,1201,15], 7, 12]]
    }
}

class Ship():
    def __init__(self,db,char):
        self.db = db
        self.char = char
        self.affects = char.affects
        self.applySkills()
    def reset(self):
        self.type = self.db['type']
        self.race = self.db['race']
        self.tech = self.db['tech']
        self.armor = self.db['armor']
        self.shield =  self.db['shield']
        self.processor =  self.db['processor']
        self.power =  self.db['power']
        self.comCap = self.db['comCap']
        self.resistances =  copy.copy(self.db['resistances'])
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
        self.deviceNames = []
        self.addGun(self.artillery)
        self.attributes = [0,self.armor,self.shield,self.resistances,self.processor,self.power,self.warpStab,self.warpSpeed,self.speed,self.energy,self.recovery,self.agility,self.volume,self.shieldRecovery,self.cargo]
    def applySkills(self):
        self.reset()
        if char.licenses()[self.race][self.tech][self.type] == 0:
            print("no license")
        elif char.licenses()[self.race][self.tech][self.type] > 3:
            self.devCap = 3
            if char.licenses()[self.race][self.tech][self.type] > 5:
                self.comCap = self.comCap + 1
        for i in range(len(self.attributes)):
            if i in self.affects.keys():
                if isinstance(self.affects[i],list):
                    value = 1
                    for each in self.affects[i]:
                        value = value * (1+each/100)
                else:
                    value = 1 + self.affects[i]/100
                self.attributes[i] = self.attributes[i] * value
        for i in range(31,34):
            if i in self.affects.keys():
                if isinstance(self.affects[i],list):
                    for each in self.affects[i]:
                        self.attributes[3][i-31] = 1 - ((1-self.attributes[3][i-31]) * (1-(each/100)))
                else:
                    self.attributes[3][i-31] = 1 - ((1-self.attributes[3][i-31]) * (1-(self.affects[i]/100)))
        self.armor = self.attributes[1]
        self.shield = self.attributes[2]
        self.resistances = self.attributes[3]
        self.processor = self.attributes[4]
        self.power = self.attributes[5]
        self.warpStab = self.attributes[6]
        self.warpSpeed = self.attributes[7]
        self.speed = self.attributes[8]
        self.energy = self.attributes[9]
        self.recovery = self.attributes[10]
        self.agility = self.attributes[11]
        self.volume = self.attributes[12]
        self.shieldRecovery = self.attributes[13]
        self.cargo = self.attributes[14]
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
    def addDevice(self,devdb,affects):
        device = Device(devdb,affects)
        fitting = device.fitting()
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
            self.devices.append(device)
            self.deviceNames.append(device.namer())
            toAppend = device.matrixReturn()
            for each in toAppend.keys():
                if each in self.affects:
                    self.affects[each].append(toAppend[each])
                else:
                    self.affects[each].append(toAppend[each])
            self.applySkills()
    def dps(self):
        return(sum([gun.dps() for gun in self.guns]))
    def dpsResist(self,resist):
        return(sum([gun.dpsResist(resist) for gun in self.guns]))
    def ammoTime(self):
        times = [gun.ammoTime() for gun in self.guns]
        return min(times)

TestDeviceDB = {
    "Adaptive Screen 1": {
        "name": "Adaptive Screen 1",
        "id": 140, "tech": 1.0,
        "rank": 1.0,
        "activation": 17.3,
        "range":0,
        "cooldown": 24.0,
        "processor": 26.0,
        "power": 11.0,
        "effect": 28.0,
        "effectTime": 18.0,
        "effects": 3
    }
}

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
        "cargo" : 100,
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
                'Propulsion Adv': [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
                'Jump Engine': [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
            },
            'Electronics': {
                'Weapon Reinforcement': [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
                'Fire-Control Reinforcement': [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
                'Core Suppression': [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
                'Weapon Suppression': [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
                'Fire-Control Suppression': [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
                'Propulsion Suppression': [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
                'Directional Scanning': [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
            }
        }
        self.license = {
            "OE": [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]],
            "NEF": [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]],
            "ECD": [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]],
            "RS": [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]
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
                "Recharge": [[0, 0], [0, 0], [0, 0]]
            },
            "Electronics": {
                "Energy": [[0, 0], [0, 0], [0, 0]],
                "Recharge": [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
            },
            "Ship Piloting":{
                "Propulsion": [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
            }
        }
        self.affects = {}
    def combo(self,source,input,multipliers,effects,sequence):
        for one in input.keys():
            for two in input[one].keys():
                for i in range(len(input[one][two])):
                    for j in range(len(input[one][two][i])):
                        key = ".".join([one,two,str(i),str(j)])
                        val = find(key,multipliers) * sequence[input[one][two][i][j]]
                        if val != 0:
                            entry = find(key,effects)
                            if isinstance(entry,list):
                                for each in entry:
                                    if each in source:
                                        source[each].append(val)
                                    else:
                                        source[each] = [val]
                            else:
                                if entry in source:
                                    source[entry].append(val)
                                else:
                                    source[entry] = [val]
        if 0 in source:
            source[0] = 0
        return source
    def applySkills(self):
        step1 = self.combo({}, self.research, research_multipliers, research_effects, research_sequence)
        self.affects = self.combo(step1, self.skill,skill_multipliers,skill_effects,skill_sequence)
    def allV(self):
        for one in self.research.keys():
            for two in self.research[one].keys():
                for i in range(len(self.research[one][two])):
                    for j in range(len(self.research[one][two][i])):
                        self.research[one][two][i][j] = 5
        for one in self.skill.keys():
            for two in self.skill[one].keys():
                for i in range(len(self.skill[one][two])):
                    for j in range(len(self.skill[one][two][i])):
                        self.skill[one][two][i][j] = 5
    def skills(self):
        return self.skill
    def researches(self):
        return self.research
    def licenses(self):
        return self.license

clean = Character()

class Gun():
    def __init__(self,db,effects):
        self.db = db
        self.applySkills()
    def applySkills(self):
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
    def __init__(self,db,matrix):
        self.db = db
        self.affects = matrix
        self.applySkills()
    def applySkills(self):
        self.reset()
        for i in range(len(self.attributes)):
            j = self.id * 10 + i
            if j in self.affects.keys():
                if isinstance(self.affects[j],list):
                    value = 1
                    for each in self.affects[j]:
                        value = value * (1+each/100)
                else:
                    value = 1 + self.affects[j]/100
                self.attributes[i] = self.attributes[i] * value
        self.effect = self.attributes[1]
        self.cooldown = self.attributes[2]
        self.activation = self.attributes[3]
        self.range = self.attributes[4]
    def reset(self):
        self.id = self.db['id']
        self.name = self.db['name']
        self.effects = self.db['effects']
        self.processor = self.db['processor']
        self.power = self.db['power']
        self.tech = self.db['tech']
        self.range = self.db['range']
        self.rank = self.db['rank']
        self.effect = self.db['effect']
        self.activation = self.db['activation']
        self.cooldown = self.db['cooldown']
        self.effectTime = self.db['effectTime']
        self.attributes = [0,self.effect,self.cooldown,self.activation,self.range]
    def matrixReturn(self):
        if self.effects == 3:
            return {31:self.effect,32:self.effect,33:self.effect}
        else:
            return {self.effects:self.effect}
    def drain(self):
        return(self.activation/self.cooldown)
    def namer(self):
        return(self.name)
    def fitting(self):
        return([self.processor,self.power])

class Component():
    def __init__(self,db,effects):
        self.db = db
        self.applySkills()
    def applySkills(self):
        self.reset()
    def reset(self):
        self.processor = self.db['processor']
        self.power = self.db['power']
        self.tech = self.db['tech']
        self.rank = self.db['rank']
        self.type = self.db['type']
        self.effect = self.db['effect']

char = Character()
char.allV()
char.applySkills()
rifter = Ship(TestShipDB["Covert"],char)
rifter.addDevice(TestDeviceDB['Adaptive Screen 1'],rifter.affects)
