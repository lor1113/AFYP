from requests_html import HTMLSession
import json
import re

ships = {}
session = HTMLSession()
header = {'user_agent': 'skeet skeet yeet', 'Accept-Encoding': 'gzip'}
datab = session.get('https://us-news.zlongame.com/sgwarship/index.jhtml', headers=header)
links = datab.html.links
links = [n for n in links if "shiptype" in n]


def intextract(string):
    flat = [item for sublist in string for item in sublist]
    base = ''.join(x for x in flat if x.isdigit())
    return (int(base))


names = ["Frigate", "Destroyer", "Cruiser", "Battlecruiser", "Battleship"]


def writer(target, tbw):
    with open(target, 'w') as outfile:
        json.dump(tbw, outfile)


def parse(data):
    ship = {}
    name = ''
    ship['resistances'] = [0, 0, 0]
    ship['artillery'] = {
        "damage": 0,
        "damages": False,
        "cooldown": 1,
        "range": 0,
        'precision': 0,
        "tracking": 0,
        "critChance": 0,
        "id": 10,
        "critDmg": 0,
        "activation": 0,
        "ammo": 0,
        "ammoUsage": 1,
        "processor": 0,
        "power": 0,
        "type": 0,
    }
    yeet = data.html.find(".ship_desc.ship_desc_t > li")
    for each in yeet:
        if "Type" in each.text:
            if "Frigate" in each.text:
                ship['type'] = 0
            if "Destroyer" in each.text:
                ship['type'] = 1
            if "Cruiser" in each.text:
                ship['type'] = 2
            if "Battlecruiser" in each.text:
                ship['type'] = 3
            if "Battleship" in each.text:
                ship['type'] = 4
        if "Class" in each.text:
            name = each.text.replace("Class", "").strip()
        if "Processor" in each.text:
            ship['processor'] = intextract(each.text.split())
        if "Power" in each.text:
            ship['power'] = intextract(each.text.split())

    yeet = data.html.find(".add_licence_h2", first=True)
    if 'T1' in yeet.text:
        ship['tech'] = 1
    elif 'T2' in yeet.text:
        ship['tech'] = 2
    elif 'T3' in yeet.text:
        ship['tech'] = 3
    if 'OE' in yeet.text:
        ship['race'] = "OE"
    if 'RS' in yeet.text:
        ship['race'] = "RS"
    if 'ECD' in yeet.text:
        ship['race'] = "ECD"
    if 'NEF' in yeet.text:
        ship['race'] = "NEF"
    yeet = data.html.find(".ship_desc.ship_sec_l > li")
    for each in yeet:
        if 'EM' in each.text:
            ship['resistances'][0] = intextract(each.text)
        if 'Kinetic' in each.text:
            ship['resistances'][1] = intextract(each.text)
        if 'Thermal' in each.text:
            ship['resistances'][2] = intextract(each.text)
        if 'Armor' in each.text:
            ship['armor'] = intextract(each.text)
        if 'Component Capacity' in each.text:
            ship['comCap'] = intextract(each.text)
    yeet = data.html.find(".ship_desc.ship_sec_r > li")
    for each in yeet:
        if 'Shield' in each.text:
            ship['shield'] = intextract(each.text)
        if 'Volume Factor' in each.text:
            ship['volume'] = intextract(each.text)
        if 'Warp Stability' in each.text:
            ship['warpStab'] = intextract(each.text)
        if 'Initial Speed' in each.text:
            ship['speed'] = intextract(each.text)
        if 'Cargo Space' in each.text:
            ship['cargo'] = intextract(each.text)
    yeet = data.html.find(".config_con > li")
    for each in yeet:
        if 'Artillery' in each.text:
            listNums = map(int, re.findall('\d+', each.text))
            listN = list(listNums)
            ship['artillery']['damage'] = listN.pop()
            ship['artillery']['damages'] = [ship['artillery']['damage'] / 3, ship['artillery']['damage'] / 3,ship['artillery']['damage'] / 3]
            ship['artillery']['range'] = listN.pop()
            ship['artillery']['name'] = names[ship['type']] + " Std Artillery"
    ships[name] = ship
    print(ship)


for each in links:
    datab = session.get(each, headers=header)
    parse(datab)

print(len(ships))
writer('Ships.json', ships)
