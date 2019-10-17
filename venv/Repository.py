import math
import json
import copy
from pathlib import Path

research_sequence = {}
skill_sequence = {}
research_multipliers = {}
research_effects = {}
skill_multipliers = {}
skill_effects = {}

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

def loader(path):
    global research_sequence
    global skill_sequence
    global research_multipliers
    global research_effects
    global skill_multipliers
    global skill_effects
    folder = Path(path)
    GunDB = reader(folder / 'Guns.json')
    ShipDB = reader(folder / 'Ships.json')
    ComponentDB = reader(folder / 'Components.json')
    DeviceDB = reader(folder / 'Devices.json')
    data = reader(folder / 'Data.json')
    research_sequence = data['research_sequence']
    skill_sequence = data['skill_sequence']
    research_multipliers = data['research_multipliers']
    research_effects = data["research_effects"]
    skill_multipliers = data["skill_multipliers"]
    skill_effects = data["skill_effects"]


class Ship():
    def __init__(self,db,char):
        self.db = db
        self.char = char
        self.affects = char.affects
        self.components = []
        self.gunNames = []
        self.componentNames = []
        self.deviceNames = []
        self.devices = []
        self.guns = []
        self.applySkills()
        self.addGun(self.db['artillery'],self.affects)
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
        self.devCap = 2
        self.attributes = [0,self.armor,self.shield,self.resistances,self.processor,self.power,self.warpStab,self.warpSpeed,self.speed,self.energy,self.recovery,self.agility,self.volume,self.shieldRecovery,self.cargo]
    def applySkills(self):
        self.reset()
        if self.char.licenses()[self.race][self.tech][self.type] == 0:
            pass
        elif self.char.licenses()[self.race][self.tech][self.type] > 3:
            self.devCap = 3
            if self.char.licenses()[self.race][self.tech][self.type] > 5:
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
        if 22 in self.affects:
            if isinstance(self.affects[22],list):
                for each in self.affects[22]:
                    self.attributes[2] = self.attributes[2] + each
            else:
                self.attributes[2] = self.attributes[2] + self.affects[22]
        if 29 in self.affects:
            if isinstance(self.affects[29],list):
                for each in self.affects[29]:
                    self.attributes[9] = self.attributes[9] + each
            else:
                self.attributes[9] = self.attributes[9] + self.affects[29]
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
    def recompile(self,char):
        char.applySkills()
        self.affects = char.affects
        for each in self.components:
            toAppend = each.matrixReturn()
            for each in toAppend.keys():
                if each in self.affects:
                    if isinstance(self.affects[each],list):
                        self.affects[each].append(toAppend[each])
                    else:
                        self.affects[each] = [self.affects[each]]
                        self.affects[each].append(toAppend[each])
                else:
                    self.affects[each] = toAppend[each]
        for each in self.devices:
            each.applySkills(self.affects)
            toAppend = each.matrixReturn()
            for each in toAppend.keys():
                if each in self.affects:
                    if isinstance(self.affects[each],list):
                        self.affects[each].append(toAppend[each])
                    else:
                        self.affects[each] = [self.affects[each]]
                        self.affects[each].append(toAppend[each])
                else:
                    self.affects[each] = toAppend[each]
        for each in self.guns:
            each.applySkills(self.affects)
        self.applySkills()
    def addGun(self,gundb,affects):
        gun = Gun(gundb,affects)
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
            self.recompile(self.char)
    def addDevice(self,devdb):
        device = Device(devdb,self.affects)
        fitting = device.fitting()
        processr = self.processor - fitting[0]
        powr = self.power - fitting[1]
        if powr < 0:
            print('Not enough Power')
            return null
        if processr < 0:
            print('Not enough Processor')
            return null
        if (len(self.devices) < self.devCap):
            self.power = powr
            self.processor = processr
            self.devices.append(device)
            self.deviceNames.append(device.namer())
            self.recompile(self.char)
    def addComponent(self,compdb):
        component = Component(compdb,self.affects)
        fitting = component.fitting()
        processr = self.processor - fitting[0]
        powr = self.power - fitting[1]
        if powr < 0:
            print('Not enough Power')
            return null
        if processr < 0:
            print('Not enough Processor')
            return null
        if (len(self.components) < self.comCap):
            self.power = powr
            self.processor = processr
            self.components.append(component)
            self.componentNames.append(component.namer())
            self.recompile(self.char)
    def dps(self):
        return sum([gun.dps() for gun in self.guns])
    def dpsResist(self,resist):
        return(sum([gun.dpsResist(resist) for gun in self.guns]))
    def ammoTime(self):
        times = [gun.ammoTime() for gun in self.guns]
        return min(times)
    def update(self,char):
        self.affects = char.affects
        self.recompile(char)

TestComponentDB = {
    "Artillery Damage Amplifier III 2": {
        "name": "Artillery Damage Amplifier III 2",
        "id": 1502,
        "effects": 102,
        "effects2": 0,
        "tech": 3.0,
        "rank": 2.0,
        "processor": 184.0,
        "power": 14.0,
        "effect": 56.8,
        "effect2": 0
    }
}

TestDeviceDB = {
    "Adaptive Screen 1": {
        "name": "Adaptive Screen 1",
        "id": 140, "tech": 1.0,
        "rank": 1.0,
        "activation": 17.3,
        "range":0,
        "cooldown": 24.0,
        "effect2":0,
        "effects2":0,
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
            "id":10,
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
        "id":100,
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
        "id": 91,
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
    def __init__(self,db,matrix):
        self.db = db
        self.affects = matrix
        self.applySkills(self.affects)
    def applySkills(self,matrix):
        self.reset()
        for i in range(len(self.attributes)):
            j = (self.id*10) + i
            if j in matrix.keys():
                if isinstance(matrix[j],list):
                    value = 1
                    for each in matrix[j]:
                        value = value * (1+each/100)
                else:
                    value = 1 + matrix[j]/100
                self.attributes[i] = self.attributes[i] * value
            if not self.id == 10:
                j = 50 + i
                if j in matrix.keys():
                    if isinstance(matrix[j],list):
                        value = 1
                        for each in matrix[j]:
                            value = value * (1+each/100)
                    else:
                        value = 1 + matrix[j]/100
                    self.attributes[i] = self.attributes[i] * value
                j = (round(self.id,-1) * 10) + i
                if j in matrix.keys():
                    if isinstance(matrix[j],list):
                        value = 1
                        for each in matrix[j]:
                            value = value * (1+each/100)
                    else:
                        value = 1 + matrix[j]/100
                    self.attributes[i] = self.attributes[i] * value
        self.cooldown = self.attributes[1]
        self.damage = self.attributes[2]
        self.range = self.attributes[3]
        self.tracking = self.attributes[4]
        self.critDmg = self.attributes[5]
        self.critChance = self.attributes[6]
        self.activation = self.attributes[7]
        for i in range(len(self.damages)):
            self.damages[i] = self.damages[i] * (self.damage/self.db['damage'])
    def reset(self):
        self.damage =  self.db['damage']
        self.damages = self.db['damages']
        self.cooldown =  self.db['cooldown']
        self.range =  self.db['range']
        self.id = self.db['id']
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
        self.attributes = [0,self.cooldown,self.damage,self.range, self.tracking,self.critDmg,self.critChance,self.activation]
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
        self.applySkills(self.affects)
    def applySkills(self,matrix):
        self.reset()
        for i in range(len(self.attributes)):
            j = self.id * 10 + i
            if j in matrix.keys():
                if isinstance(matrix[j],list):
                    value = 1
                    for each in matrix[j]:
                        value = value * (1+each/100)
                else:
                    value = 1 + matrix[j]/100
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
        self.effect2 = self.db['effect2']
        self.effects2 = self.db['effects2']
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
            return {31:self.effect,32:self.effect,33:self.effect,self.effects2:self.effects2}
        else:
            return {self.effects:self.effect,self.effects2:self.effect2}
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
        self.name = self.db['name']
        self.rank = self.db['rank']
        self.id = self.db['id']
        self.effect = self.db['effect']
        self.effect2 = self.db['effect2']
        self.effects = self.db['effects']
        self.effects2 = self.db['effects2']
    def matrixReturn(self):
        return {self.effects: self.effect, self.effects2: self.effect2}
    def fitting(self):
        return([self.processor,self.power])
    def namer(self):
        return(self.name)

loader("DB/1.0/")
char = Character()
char.applySkills()
rifter = Ship(TestShipDB['Covert'],char)
print(rifter.resistances)
char.allV()
char.applySkills()
rifter.update(char)
print(rifter.resistances)
rifter.addDevice(TestDeviceDB['Adaptive Screen 1'])
print(rifter.resistances)
print(rifter.dps())
rifter.addComponent(TestComponentDB['Artillery Damage Amplifier III 2'])
print(rifter.dps())
print(rifter.components)