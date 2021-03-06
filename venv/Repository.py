import copy
import json
import math
from pathlib import Path

options = ["DB/1.0/"]
default = "DB/1.0/"


def reader(target):
    json_data = open(target).read()
    return json.loads(json_data)


def find(code, rv):
    keys = code.split('.')
    for key in keys:
        try:
            rv = rv[key]
        except:
            rv = rv[int(key)]
    return rv


def loader(path=""):
    global research_sequence
    global skill_sequence
    global research_multipliers
    global research_effects
    global skill_multipliers
    global skill_effects
    global gunDB
    global shipDB
    global componentDB
    global deviceDB
    global implantDB
    if path:
        folder = Path(path)
    else:
        folder = Path(default)
    gunDB = reader(folder / 'Guns.json')
    shipDB = reader(folder / 'Ships.json')
    componentDB = reader(folder / 'Components.json')
    deviceDB = reader(folder / 'Devices.json')
    data = reader(folder / 'Data.json')
    implantDB = reader(folder / "Implants.json")
    research_sequence = data['research_sequence']
    skill_sequence = data['skill_sequence']
    research_multipliers = data['research_multipliers']
    research_effects = data["research_effects"]
    skill_multipliers = data["skill_multipliers"]
    skill_effects = data["skill_effects"]


def compiler(j, matrix):
    value = 1
    if j in matrix.keys():
        if isinstance(matrix[j], list):
            for each in matrix[j]:
                value = value * (1 + each / 100)
        else:
            value = 1 + matrix[j] / 100
    return value


def invertedCompiler(j, matrix):
    value = 1
    if j in matrix.keys():
        if isinstance(matrix[j], list):
            for each in matrix[j]:
                value = value * (1 - each / 100)
        else:
            value = 1 - matrix[j] / 100
    return value


def combo(source, info, multipliers, effects, sequence):
    for one in info.keys():
        for two in info[one].keys():
            for i in range(len(info[one][two])):
                for j in range(len(info[one][two][i])):
                    key = ".".join([one, two, str(i), str(j)])
                    val = find(key, multipliers) * sequence[info[one][two][i][j]]
                    if val != 0:
                        entry = find(key, effects)
                        if isinstance(entry, list):
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


def collate(dict1, dict2):
    for key, item in dict2.items():
        if isinstance(item, list):
            if key in dict1.keys():
                if isinstance(dict1[key], list):
                    dict1[key] = dict1[key].extend(item)
                else:
                    dict1[key] = [dict1[key]].extend(item)
            else:
                dict1[key] = item
        else:
            if key in dict1.keys():
                if isinstance(dict1[key], list):
                    dict1[key].append(item)
                else:
                    dict1[key] = [dict1[key], item]
            else:
                dict1[key] = item
    return dict1


class Ship:
    def __init__(self, db, char):
        self.db = db
        self.char = char
        self.affects = char.affects
        self.extendedAffects = {}
        self.aoeAffects = {}
        self.base = char.affects
        self.components = []
        self.gunNames = []
        self.aoeShips = []
        self.extendedShips = []
        self.componentNames = []
        self.deviceNames = []
        self.devices = []
        self.updateShips = []
        self.guns = []
        self.inverted = [12]
        self.hullBonuses = self.db['hullBonuses']
        self.licenseBonuses = self.db['licenseBonuses']
        self.applySkills()
        self.addGun(self.db['artillery'], self.affects)
        self.addDevice(self.db['thruster'])
        self.addDevice(self.db['shield'])
        char.ships.append(self)

    def reset(self):
        self.type = self.db['type']
        self.race = self.db['race']
        self.tech = self.db['tech']
        self.armor = self.db['armor']
        self.shield = self.db['shield']
        self.processor = self.db['processor']
        self.power = self.db['power']
        self.comCap = self.db['comCap']
        self.resistances = copy.copy(self.db['resistances'])
        self.warpStab = self.db['warpStab']
        self.warpSpeed = self.db['warpSpeed']
        self.speed = self.db['speed']
        self.energy = self.db['energy']
        self.recovery = self.db['energyRecovery']
        self.agility = self.db['agility']
        self.volume = self.db['volume']
        self.shieldRecovery = self.db['shieldRecovery']
        self.cargo = self.db['cargo']
        self.artillery = self.db['artillery']
        self.devCap = 4
        self.license = self.char.licenses()[self.race][self.tech][self.type]
        self.attributes = [0, self.armor, self.shield, self.resistances, self.processor, self.power, self.warpStab,
                           self.warpSpeed, self.speed, self.energy, self.recovery, self.agility, self.volume,
                           self.shieldRecovery, self.cargo]

    def applySkills(self):
        self.reset()
        if self.license == 0:
            print("Lacks License")
        elif self.license > 3:
            self.devCap = self.devCap + 1
            if self.license > 5:
                self.comCap = self.comCap + 1
        for key, val in self.hullBonuses.items():
            if key in self.affects.keys():
                self.affects[key].append(val)
            else:
                self.affects[key] = [val]
        for key, val in self.licenseBonuses.items():
            val = val * self.license
            if key in self.affects.keys():
                self.affects[key].append(val)
            else:
                self.affects[key] = [val]
        for i in range(len(self.attributes)):
            if i in self.inverted:
                if i in self.affects.keys():
                    value = invertedCompiler(i, self.affects)
                    self.attributes[i] = self.attributes[i] * value
            else:
                if i in self.affects.keys():
                    value = compiler(i, self.affects)
                    self.attributes[i] = self.attributes[i] * value
        for i in range(31, 34):
            if i in self.affects.keys():
                if isinstance(self.affects[i], list):
                    for each in self.affects[i]:
                        self.attributes[3][i - 31] = 1 - ((1 - self.attributes[3][i - 31]) * (1 - (each / 100)))
                else:
                    self.attributes[3][i - 31] = 1 - ((1 - self.attributes[3][i - 31]) * (1 - (self.affects[i] / 100)))
        if 22 in self.affects:
            if isinstance(self.affects[22], list):
                for each in self.affects[22]:
                    self.attributes[2] = self.attributes[2] + each
            else:
                self.attributes[2] = self.attributes[2] + self.affects[22]
        if 23 in self.affects:
            if isinstance(self.affects[23], list):
                for each in self.affects[23]:
                    self.attributes[13] = self.attributes[13] + each
            else:
                self.attributes[13] = self.attributes[13] + self.affects[23]
        if 29 in self.affects:
            if isinstance(self.affects[29], list):
                for each in self.affects[29]:
                    self.attributes[9] = self.attributes[9] + each
            else:
                self.attributes[9] = self.attributes[9] + self.affects[29]
        if 26 in self.affects:
            if isinstance(self.affects[26], list):
                for each in self.affects[26]:
                    self.attributes[6] = self.attributes[6] + each
            else:
                self.attributes[6] = self.attributes[6] + self.affects[26]
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

    def compileExtended(self):
        self.extendedAffects = {}
        for each in self.devices:
            response = each.extendedReturn()
            for each2 in response.keys():
                if each2 in self.extendedAffects:
                    if isinstance(self.extendedAffects[each2], list):
                        self.extendedAffects[each2].append(response[each2])
                    else:
                        self.extendedAffects[each2] = [self.extendedAffects[each2], response[each2]]
                else:
                    self.extendedAffects[each2] = response[each2]
        return self.extendedAffects

    def compileAoe(self):
        self.aoeAffects = {}
        for each in self.devices:
            response = each.aoeReturn()
            for each2 in response.keys():
                if each2 in self.aoeAffects:
                    if isinstance(self.aoeAffects[each2], list):
                        self.aoeAffects[each2].append(response[each2])
                    else:
                        self.aoeAffects[each2] = [self.aoeAffects[each2], response[each2]]
                else:
                    self.aoeAffects[each2] = response[each2]
        return self.aoeAffects

    def recompile(self, matrix, stage):
        self.affects = matrix
        if stage < 3:
            for each in self.aoeShips:
                each[0].recompile(each.base,3)
                toAppend = each[0].aoeAffects
                for each2 in toAppend.keys():
                    if each[1]:
                        if each2 > 8000:
                            if each2 in self.affects:
                                if isinstance(self.affects[each2], list):
                                    self.affects[each2].append(toAppend[each2])
                                else:
                                    self.affects[each2] = [self.affects[each2]]
                                    self.affects[each2].append(toAppend[each2])
                            else:
                                self.affects[each2] = toAppend[each2]
                    else:
                        if each2 < 8000:
                            if each2 in self.affects:
                                if isinstance(self.affects[each2], list):
                                    self.affects[each2].append(toAppend[each2])
                                else:
                                    self.affects[each2] = [self.affects[each2]]
                                    self.affects[each2].append(toAppend[each2])
                            else:
                                self.affects[each2] = toAppend[each2]
            for each in self.extendedShips:
                each[0].recompile(each.base,3)
                toAppend = each[0].extendedAffects
                for each2 in toAppend.keys():
                    if each[1]:
                        if each2 > 8000:
                            if each2 in self.affects:
                                if isinstance(self.affects[each2], list):
                                    self.affects[each2].append(toAppend[each2])
                                else:
                                    self.affects[each2] = [self.affects[each2]]
                                    self.affects[each2].append(toAppend[each2])
                            else:
                                self.affects[each2] = toAppend[each2]
                    else:
                        if each2 < 8000:
                            if each2 in self.affects:
                                if isinstance(self.affects[each2], list):
                                    self.affects[each2].append(toAppend[each2])
                                else:
                                    self.affects[each2] = [self.affects[each2]]
                                    self.affects[each2].append(toAppend[each2])
                            else:
                                self.affects[each2] = toAppend[each2]
        if stage < 2:
            for each in self.components:
                toAppend = each.matrixReturn()
                for each2 in toAppend.keys():
                    if each2 in self.affects:
                        if isinstance(self.affects[each2], list):
                            self.affects[each2].append(toAppend[each2])
                        else:
                            self.affects[each2] = [self.affects[each2]]
                            self.affects[each2].append(toAppend[each2])
                    else:
                        self.affects[each2] = toAppend[each2]
        if stage < 3:
            for each in self.devices:
                each.applySkills(self.affects)
                toAppend = each.matrixReturn()
                for each2 in toAppend.keys():
                    if each2 in self.affects:
                        if isinstance(self.affects[each2], list):
                            self.affects[each2].append(toAppend[each2])
                        else:
                            self.affects[each2] = [self.affects[each2]]
                            self.affects[each2].append(toAppend[each2])
                    else:
                        self.affects[each2] = toAppend[each2]
        if stage < 5:
            for each in self.guns:
                each.applySkills(self.affects)
        self.applySkills()
        self.compileAoe()
        self.compileExtended()
        self.affects[0] = 0
        for each in self.updateShips:
            each.recompile(each.base,3)

    def getAttr(self, id):
        return self.attributes[id]

    def removeGun(self, gun):
        self.guns.remove(gun)
        self.gunNames.remove(gun.naming())
        self.recompile(self.base,4)

    def removeDevice(self, device):
        self.devices.remove(device)
        self.deviceNames.remove(device.naming())
        self.recompile(self.base,2)

    def removeComponent(self, component):
        self.components.remove(component)
        self.componentNames.remove(component.naming())
        self.recompile(self.base,1)

    def addGun(self, gunDatabase, affects):
        gun = Gun(gunDatabase, affects)
        fitting = gun.fitting()
        processor = self.processor - fitting[0]
        power = self.power - fitting[1]
        if power < 0:
            print('Not enough Power')
        if processor < 0:
            print('Not enough Processor')
        if len(self.guns) < 4:
            self.power = power
            self.processor = processor
            self.guns.append(gun)
            self.gunNames.append(gun.naming())

    def addDevice(self, deviceDatabase):
        device = Device(deviceDatabase, self.affects)
        fitting = device.fitting()
        processor = self.processor - fitting[0]
        power = self.power - fitting[1]
        if power < 0:
            print('Not enough Power')
        if processor < 0:
            print('Not enough Processor')
        if len(self.devices) < self.devCap:
            self.power = power
            self.processor = processor
            self.devices.append(device)
            self.deviceNames.append(device.naming())
            self.recompile(self.base,2)

    def addComponent(self, componentDatabase):
        component = Component(componentDatabase)
        fitting = component.fitting()
        processor = self.processor - fitting[0]
        power = self.power - fitting[1]
        if power < 0:
            print('Not enough Power')
        if processor < 0:
            print('Not enough Processor')
        if len(self.components) < self.comCap:
            self.power = power
            self.processor = processor
            self.components.append(component)
            self.componentNames.append(component.naming())
            self.recompile(self.base,1)

    def addAoe(self, ship, enemy):
        self.aoeShips.append([ship, enemy])
        self.updateShips.append(ship)

    def addExtended(self, ship, enemy):
        self.extendedShips.append([ship, enemy])
        self.updateShips.append(ship)

    def removeAoe(self, ship, enemy):
        self.aoeShips.remove([ship, enemy])
        self.updateShips.remove(ship)

    def removeExtended(self, ship, enemy):
        self.extendedShips.remove([ship, enemy])
        self.updateShips.remove(ship)

    def dps(self):
        return sum([gun.dps() for gun in self.guns])

    def dpsResist(self, resist):
        return sum([gun.dpsResist(resist) for gun in self.guns])

    def ammoTime(self):
        times = [gun.ammoTime() for gun in self.guns]
        return min(times)

    def range(self):
        ranges = [gun.range for gun in self.guns]
        if max(ranges) == min(ranges):
            return max(ranges)
        else:
            return[min(ranges),max(ranges)]




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
        "range": 0,
        "cooldown": 24.0,
        "effectType": 0,
        "effect2": 0,
        "effects2": 0,
        "processor": 26.0,
        "power": 11.0,
        "effect": 28.0,
        "effectTime": 18.0,
        "effects": 3
    }
}

TestShipDB = {
    "Convert": {
        "type": 0,
        'tech': 1,
        "race": "OE",
        "armor": 1760,
        "shield": 1876,
        "processor": 243,
        "power": 107,
        "comCap": 1,
        "resistances": [0.3, 0.1, 0.5],  # EM,KINETIC,THERMAL
        "warpStab": 2,
        "warpSpeed": 10.58,
        "speed": 688,
        "energy": 1241,
        "cargo": 100,
        "energyRecovery": 12,
        "agility": 693,
        "volume": 140,
        "shieldRecovery": 1,
        "hullBonuses": {"26": 1, "15": 15, "16": 55},
        "licenseBonuses": {"10": 4.5, "12": 2, "601": 3},
        "artillery": {
            "tech": 1,
            "rank": 1,
            "damage": 18,
            "damages": [6, 6, 6],
            "cooldown": 1,
            "range": 9,
            "id": 10,
            'precision': 0,
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
        "shield":{
            "name": "Frigate Std. Shield Recharger",
            "id": 20,
            "tech": 1.0,
            "rank": 1.0,
            "activation": 230,
            "range": 0,
            "cooldown": 30,
            "effectType": 0,
            "effect2": 0,
            "effects2": 0,
            "processor": 0,
            "power": 0,
            "effect": 14.2604,
            "effectTime": 30,
            "effects": 23
        },
        "thruster":{
            "name": "Frigate Std. Ion Thruster",
            "id": 10,
            "tech": 1.0,
            "rank": 1.0,
            "activation": 459,
            "range": 0,
            "cooldown": 30,
            "effectType": 0,
            "effect2": 0,
            "effects2": 0,
            "processor": 0,
            "power": 0,
            "effect": 100,
            "effectTime": 30,
            "effects": 8
        }
    }
}
TestGunDB = {
    "artillery": {
        "damage": 18,
        "damages": [6, 6, 6, ],
        "cooldown": 1,
        "range": 9,
        'precision': 0,
        "tech": 0,
        "rank": 0,
        "tracking": 0,
        "critChance": 0,
        "id": 100,
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
        "damages": [31, 93, 0],
        "cooldown": 4,
        "range": 12.5,
        "critChance": 10.0,
        "id": 91,
        "critDmg": 2,
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
    def __init__(self, level=None):
        self.ships = []
        self.implants = []
        self.p = [0, 0]
        self.t = [0, 0]
        self.f = [0, 0]
        self.o = [0, 0]
        self.slots = [self.p, self.t, self.f, self.o]
        if level:
            self.setLevel(level)
        else:
            self.level = 0
        self.research = {
            "Ships": {
                "OE": [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]],
                "NEF": [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]],
                "ECD": [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]],
                "RS": [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]
            },
            "Weapons": {
                'Blasters': [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
                'Blasters Adv': [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
                'Lasers': [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
                'Lasers Adv': [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
                'Railguns': [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
                'Railguns Adv': [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
                'Missiles': [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
                'Missiles Adv': [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
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
            "Weapon": {
                "Railgun": [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
                "Launcher": [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
                "Laser": [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
                "Blaster": [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
            },
            "Defense": {
                "Resistance": [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
                "Recharge": [[0, 0], [0, 0], [0, 0]]
            },
            "Electronics": {
                "Energy": [[0, 0], [0, 0], [0, 0]],
                "Recharge": [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
            },
            "Ship Piloting": {
                "Propulsion": [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
            }
        }
        self.affects = {}

    def applySkills(self):
        step1 = combo({}, self.research, research_multipliers, research_effects, research_sequence)
        step2 = combo(step1, self.skill, skill_multipliers, skill_effects, skill_sequence)
        for each in self.implants:
            step2 = collate(step2, each.output)
        self.affects = step2
        for each in self.ships:
            each.base = self.affects
            each.recompile(self.affects,0)
        return self.affects

    def allX(self, x):
        for one in self.research.keys():
            for two in self.research[one].keys():
                for i in range(len(self.research[one][two])):
                    for j in range(len(self.research[one][two][i])):
                        self.research[one][two][i][j] = x
        for one in self.skill.keys():
            for two in self.skill[one].keys():
                for i in range(len(self.skill[one][two])):
                    for j in range(len(self.skill[one][two][i])):
                        self.skill[one][two][i][j] = x
        self.applySkills()

    def setSkills(self, skills):
        self.skill = skills
        self.applySkills()

    def setResearches(self, researches):
        self.research = researches
        self.applySkills()

    def setLicenses(self, licenses):
        self.license = licenses
        self.applySkills()

    def skills(self):
        return self.skill

    def researches(self):
        return self.research

    def licenses(self):
        return self.license

    def setLevel(self, level):
        self.level = level
        con = math.floor((min(level, 32)) / 4)
        noc = implantDB["unlocks"][con]
        self.p[0] = noc[0]
        self.t[0] = noc[1]
        self.f[0] = noc[2]
        self.o[0] = noc[3]

    def addShip(self, db):
        return Ship(db, self)

    def addImplant(self, name="", implant=""):
        if not implant:
            implant = Implant(name)
        slot = self.slots[implantDB["lobes"].index(implant.lobe)]
        if slot[0] > slot[1]:
            self.implants.append(implant)
            slot[0] = slot[0] + 1
            self.applySkills()

    def removeImplant(self, implant):
        self.implants.remove(implant)
        slot = self.slots[implantDB["lobes"].index(implant.lobe)]
        slot[0] = slot[0] - 1


class Gun:
    def __init__(self, db, matrix):
        self.db = db
        self.affects = matrix
        self.inverted = [1, 7]
        self.active = True
        self.applySkills(self.affects)

    def applySkills(self, matrix):
        self.reset()
        for i in range(len(self.attributes)):
            j = (self.id * 10) + i
            if i in self.inverted:
                value = invertedCompiler(j, matrix)
            else:
                value = compiler(j, matrix)
            self.attributes[i] = self.attributes[i] * value
            if not self.id == 10:
                j = 50 + i
                if i in self.inverted:
                    value = invertedCompiler(j, matrix)
                else:
                    value = compiler(j, matrix)
                self.attributes[i] = self.attributes[i] * value
                j = (round(self.id, -1) * 10) + i
                value = compiler(j, matrix)
                self.attributes[i] = self.attributes[i] * value
        self.cooldown = self.attributes[1]
        self.damage = self.attributes[2]
        self.range = self.attributes[3]
        self.tracking = self.attributes[4]
        self.critDmg = self.attributes[5]
        self.critChance = self.attributes[6]
        self.activation = self.attributes[7]
        for i in range(len(self.damages)):
            self.damages[i] = self.damages[i] * (self.damage / self.db['damage'])

    def reset(self):
        self.damage = self.db['damage']
        self.damages = self.db['damages']
        self.cooldown = self.db['cooldown']
        self.range = self.db['range']
        self.id = self.db['id']
        self.precision = self.db['precision']
        self.tracking = self.db['tracking']
        self.activation = self.db['activation']
        self.ammo = self.db['ammo']
        self.tech = self.db['tech']
        self.rank = self.db['rank']
        self.ammoUsage = self.db['ammoUsage']
        self.processor = self.db['processor']
        self.power = self.db['power']
        self.type = self.db['type']
        self.critChance = self.db['critChance'] / 10
        self.critDmg = self.db['critDmg']
        self.name = self.db['name']
        self.attributes = [0, self.cooldown, self.damage, self.range, self.tracking, self.critDmg, self.critChance, self.activation, self.precision]

    def naming(self):
        return self.name

    def fitting(self):
        return [self.processor, self.power]

    def dps(self):
        if self.active:
            if self.damages:
                return ((sum(self.damages) / self.cooldown) * (1 - self.critChance)) + (
                        (sum(self.damages) / self.cooldown) * (self.critChance * self.critDmg))
            else:
                return ((self.damage / self.cooldown) * (1 - self.critChance)) + (
                        (self.damage / self.cooldown) * (self.critChance * self.critDmg))
        else:
            return 0

    def dpsResist(self, resist):
        if self.active:
            if self.damages:
                one = (((self.damages[0] / self.cooldown) * (1 - self.critChance)) + (
                        (self.damages[0] / self.cooldown) * (self.critChance * self.critDmg))) * (1 - resist[0])
                two = (((self.damages[1] / self.cooldown) * (1 - self.critChance)) + (
                        (self.damages[1] / self.cooldown) * (self.critChance * self.critDmg))) * (1 - resist[1])
                three = (((self.damages[2] / self.cooldown) * (1 - self.critChance)) + (
                        (self.damages[2] / self.cooldown) * (self.critChance * self.critDmg))) * (1 - resist[2])
                return one + two + three
            else:
                return ((self.damage / self.cooldown) * (1 - self.critChance)) + (
                        (self.damage / self.cooldown) * (self.critChance * self.critDmg))
        else:
            return 0

    def drain(self):
        if self.active:
            return self.activation / self.cooldown
        else:
            return 0

    def ammoTime(self):
        if self.active:
            if self.ammo == 0:
                return math.inf
            else:
                return (self.ammo / self.ammoUsage) * self.cooldown
        else:
            return math.inf


class Device:
    def __init__(self, db, matrix):
        self.db = db
        self.affects = matrix
        self.inverted = [2, 3]
        self.active = True
        self.applySkills(self.affects)

    def applySkills(self, matrix):
        self.reset()
        for i in range(len(self.attributes)):
            j = self.id * 10 + i
            if i in self.inverted:
                value = invertedCompiler(j, matrix)
            else:
                value = compiler(j, matrix)
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
        self.effectType = self.db['effectType']
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
        self.attributes = [0, self.effect, self.cooldown, self.activation, self.range]

    def matrixReturn(self):
        if self.active:
            if self.effectType == 0:
                returns = {}
                if self.effects == 3:
                    returns[31] = self.effect
                    returns[32] = self.effect
                    returns[33] = self.effect
                elif isinstance(self.effects, list):
                    for each in self.effects:
                        returns[each] = self.effect
                else:
                    returns[self.effects] = self.effect
                if isinstance(self.effects2, list):
                    for each in self.effects2:
                        returns[each] = self.effect2
                else:
                    returns[self.effects2] = self.effect2
                return returns
            else:
                return {}
        else:
            return {}

    def aoeReturn(self):
        if self.active:
            if self.effectType == 2:
                returns = {}
                if isinstance(self.effects, list):
                    for each in self.effects:
                        returns[each] = self.effect
                else:
                    returns[self.effects] = self.effect
                if isinstance(self.effects2, list):
                    for each in self.effects2:
                        returns[each] = self.effect2
                else:
                    returns[self.effects2] = self.effect2
                return returns
            else:
                return {}
        else:
            return {}

    def extendedReturn(self):
        if self.active:
            if self.effectType == 1:
                returns = {}
                if isinstance(self.effects, list):
                    for each in self.effects:
                        returns[each] = self.effect
                else:
                    returns[self.effects] = self.effect
                if isinstance(self.effects2, list):
                    for each in self.effects2:
                        returns[each] = self.effect2
                else:
                    returns[self.effects2] = self.effect2
                return returns
            else:
                return {}
        else:
            return {}

    def drain(self):
        if self.active:
            return self.activation / self.cooldown
        else:
            return 0

    def naming(self):
        return self.name

    def fitting(self):
        return [self.processor, self.power]


class Component:
    def __init__(self, db):
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
        returns = {}
        if isinstance(self.effects, list):
            for each in self.effects:
                returns[each] = self.effect
        else:
            returns[self.effects] = self.effect
        if isinstance(self.effects2, list):
            for each in self.effects2:
                returns[each] = self.effect2
        else:
            returns[self.effects2] = self.effect2
        return returns

    def fitting(self):
        return [self.processor, self.power]

    def naming(self):
        return self.name


class Implant:
    def __init__(self, name):
        self.name = name
        self.lobe = ""
        self.tech = 0
        self.rank = 0
        self.type = ""
        self.output = {}
        self.subtype = 0
        self.oem = False
        self.decode()

    def decode(self):
        x = next((y for y in implantDB["oemNames"] if y in self.name), None)
        if x:
            self.lobe = implantDB["lobes"][implantDB["oemNames"].index(x)]
            self.oem = True
            z = self.name.strip(x).strip()
            self.type = z[0:2]
        else:
            x = next((y for y in implantDB["amNames"] if y in self.name), None)
            if x:
                self.lobe = implantDB["lobes"][implantDB["amNames"].index(x)]
                self.type = self.name.split()[0]
            else:
                return
        try:
            x = self.name.strip("I").strip()
            self.rank = int(x[-1])
            self.tech = int(x[-2])
            self.subtype = int(x[-3])
        except:
            return
        multi = implantDB["sequence"][(self.rank + ((self.tech - 1) * 5)) - 1]
        if self.oem:
            primary = self.type[0]
            secondary = self.type[1]
            if secondary in implantDB["oemCombos"][primary]:
                if primary in ["A", "R", "C", "F"]:
                    if secondary == "O":
                        if self.subtype == 0:
                            affects = implantDB["oemAffects"][primary][0] + 50
                            effect = round(implantDB["oemMultipliers"][primary][0] * multi, 1)
                            self.output = {
                                affects: effect
                            }
                        else:
                            effect = round(implantDB["oemMultipliers"][primary][0] * (1 / 3) * multi, 1)
                            affects = implantDB["oemAffects"][primary][0]
                            self.output = {
                                affects + implantDB["oemCycle"][self.subtype][0]: effect,
                                affects + implantDB["oemCycle"][self.subtype][1]: effect
                            }
                    else:
                        if self.subtype == 0:
                            affects = [implantDB["oemAffects"][primary][0] + 50].extend(implantDB["oemAffects"][secondary])
                            effect = round(implantDB["oemMultipliers"][primary][0] * 0.75 * multi, 1)
                            for each in affects:
                                self.output[each] = effect
                        else:
                            effect = round(implantDB["oemMultipliers"][primary][0] * 0.75 * (1 / 3) * multi, 1)
                            affects = implantDB["oemAffects"][primary][0]
                            self.output = {
                                affects + implantDB["oemCycle"][self.subtype][0]: effect,
                                affects + implantDB["oemCycle"][self.subtype][1]: effect,
                            }
                            affects = implantDB["oemAffects"][secondary]
                            for each in affects:
                                self.output[each] = round(implantDB["oemMultipliers"][secondary][1] * multi, 1)
                else:
                    if secondary == "O":
                        affects = implantDB["oemAffects"][primary]
                        effects = round(implantDB["oemMultipliers"][primary][0] * multi, 1)
                        for each in affects:
                            self.output[each] = effects
                    if secondary in ["A", "R", "C", "F"]:
                        affects = implantDB["oemAffects"][primary]
                        effects = round(implantDB["oemMultipliers"][primary][0] * 0.75 * multi, 1)
                        for each in affects:
                            self.output[each] = effects
                        effect = round(implantDB["oemMultipliers"][secondary][1] * multi, 1)
                        affects = implantDB["oemAffects"][secondary][0]
                        self.output[affects + implantDB["oemCycle"][self.subtype][0]] = effect
                        self.output[affects + implantDB["oemCycle"][self.subtype][1]] = effect
                    else:
                        affects = implantDB["oemAffects"][primary]
                        effects = round(implantDB["oemMultipliers"][primary][0] * 0.75 * multi, 1)
                        for each in affects:
                            self.output[each] = effects
                        affects = implantDB["oemAffects"][secondary]
                        effects = round(implantDB["oemMultipliers"][secondary][1] * multi, 1)
                        for each in affects:
                            self.output[each] = effects
            else:
                return
        else:
            affects = implantDB["amAffects"][self.lobe][self.type][self.subtype - 1]
            effect = implantDB["amMultipliers"][self.lobe][self.type][self.subtype - 1]
            if isinstance(effect, list):
                self.output = {
                    affects[0]: round(effect[0] * multi, 1),
                    affects[1]: round(effect[1] * multi, 1)
                }
            else:
                if isinstance(affects, list):
                    for each in affects:
                        self.output[each] = round(effect * multi, 1)
                else:
                    self.output[affects] = round(effect * multi, 1)


loader()
steve = Character(level=32)
rifter = Ship(TestShipDB["Convert"], steve)
print(rifter.guns[0].damage)
strang = "Crowley AO-024 II"
steve.addImplant(name=strang)
print(rifter.guns[0].damage)
steve.addImplant(name=strang)
print(rifter.guns[0].damage)
