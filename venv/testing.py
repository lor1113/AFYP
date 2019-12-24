from pathlib import Path
import json

options = ["DB/1.0/"]
default = "DB/1.0/"


def reader(target):
    json_data = open(target).read()
    return json.loads(json_data)


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
    research_sequence = data['research_sequence']
    skill_sequence = data['skill_sequence']
    research_multipliers = data['research_multipliers']
    research_effects = data["research_effects"]
    skill_multipliers = data["skill_multipliers"]
    skill_effects = data["skill_effects"]
    implantDB = data["ImplantDB"]


class Implant:
    def __init__(self, name):
        self.name = name
        self.lobe = ""
        self.tech = 0
        self.rank = 0
        self.type = ""
        self.effects = []
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
        if self.oem:
            return
        else:
            self.effects = implantDB["amAffects"][self.lobe][self.type][self.subtype - 1]


loader()
strang = "Thunder PL-113 I"
new = Implant(strang)
print(new.effects)
