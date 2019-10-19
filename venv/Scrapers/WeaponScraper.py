import requests
import json
from requests_html import HTMLSession

def writer(target,tbw):
    with open(target,'w') as outfile:
        json.dump(tbw,outfile)

def intextract(string):
    flat = [item for sublist in string for item in sublist]
    base =[x for x in flat if x.isdigit() or x == "."]
    while base[-1] == ".":
        base.pop()
    while base[0] == ".":
        base.pop(0)
    return(float(''.join(base)))

form = {
    'appId': 1,
    'order': 1,
    'pageNumber': 1,
    'pageCounts': 10,
    'title': "",
    'channel': 257
}
content = []
distri = [
    1,
    [0.1,0.2,0.7],
    [0.7,0.2,0.1],
    [0,0.6,0.4],
    [0.25,0.75,0],
]
guns = {}
session = HTMLSession()
header = {'user_agent':'skeet skeet yeet','Accept-Encoding':'gzip'}
r = requests.post('https://us-news.zlongame.com/pd_search.jspx',data = form)
total = r.json()['totalPage']
def parse(data):
    gun = {}
    name = data.html.find(".weapon_inner_show_desc.fl > h2", first=True).text
    gun['name'] = name
    if 'Laser' in name:
        gun['type'] = 1
    if 'Blaster' in name:
        gun['type'] = 2
    if 'Missile' in name:
        gun['type'] = 3
    if 'Railgun' in name:
        gun['type'] = 4
    if 'S-' in name:
        gun['id'] = 50 + (10*gun['type']) + 1
    if 'M-' in name:
        gun['id'] = 50 + (10*gun['type']) + 2
    if 'L-' in name:
        gun['id'] = 50 + (10*gun['type']) + 3
    for each in data.html.find(".weapon_inner_list_list > li"):
        if 'Damage Per Cycle' in each.text:
            gun['damage'] = intextract(each.text)
        if 'Cooldown' in each.text:
            gun['cooldown'] = intextract(each.text)
        if 'Range' in each.text:
            try:
                gun['range'] = intextract(each.text)
            except:
                gun['range'] = 0
        if 'Crit Rate' in each.text:
            gun['critChance'] = intextract(each.text)
        if 'Precision' in each.text:
            gun['precision'] = intextract(each.text)
        if 'Tracking Speed' in each.text:
            gun['tracking'] = intextract(each.text)
        if 'Activation Cost' in each.text:
            gun['activation'] = intextract(each.text)
        if 'Ammo Capacity' in each.text:
            gun['ammo'] = intextract(each.text)
        if 'Processor' in each.text:
            gun['processor'] = intextract(each.text)
        if 'Power' in each.text:
            gun['power'] = intextract(each.text)
    damages = [0,0,0]
    damages[0] = distri[gun['type']][0] * gun['damage']
    damages[1] = distri[gun['type']][1] * gun['damage']
    damages[2] = distri[gun['type']][2] * gun['damage']
    gun['damages'] = damages
    for each in data.html.find(".weapon_inner_show_desc.fl > p"):
        if 'Tech Level' in each.text:
            gun['tech'] = intextract(each.text)
        if 'Rank' in each.text:
            gun['rank'] = intextract(each.text)
    gun["critDmg"] = 2
    if gun['tech'] == 1:
        if gun['rank'] == 1:
            print(gun)
    if gun['tech'] == 3:
        if gun['rank'] == 5:
            print(gun)
    guns[name + " " + str(gun['rank'])] = gun

while form['pageNumber'] <= total:
    r = requests.post('https://us-news.zlongame.com/pd_search.jspx', data=form)
    for each in r.json()['list']:
        content.append(each['content_id'])
    print(r.json()['currPage'])
    form['pageNumber'] = form['pageNumber'] + 1

for each in content:
    datab = session.get('https://us-news.zlongame.com/sgweapon/' + str(each) + '.jhtml')
    parse(datab)

writer('Guns.json',guns)
