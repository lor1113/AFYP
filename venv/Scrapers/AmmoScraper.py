import requests
from requests_html import HTMLSession
import json

form = {
    'appId': 1,
    'order': 1,
    'pageNumber': 1,
    'pageCounts': 250,
    'title': "",
    'channel': 260
}

types = ["Laser Charge","Blaster Charge","Missile","Railgun Charge"]

ammos = {}
session = HTMLSession()
header = {'user_agent':'skeet skeet yeet','Accept-Encoding':'gzip'}

def num_there(s):
    return any(i.isdigit() for i in s)

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

def parse(data):
    ammo = {}
    rank = 0
    name = ''
    if id == 60 or id == 70 or id == 90:
        name = data.html.find(".weapon_inner_show_desc.fl > h2", first=True).text
        if 'S-' in name:
            ammo['id'] = id + 1
        if 'M-' in name:
            ammo['id'] = id + 2
        if 'L-' in name:
            ammo['id'] = id + 3
        for each in data.html.find(".weapon_inner_show_desc.fl > p"):
            if 'Rank' in each.text:
                rank = intextract(each.text)
                name = name + " " + str(rank)
                ammo['name'] = name
        for each in data.html.find(".weapon_inner_list_list > li"):
            if 'Damage' in each.text:
                print(each.text)
                ammo['damage'] = intextract(each.text)
            if 'Range' in each.text:
                ammo['range'] = intextract(each.text)
    ammos[ammo["name"]] = ammo
    print(ammo)

for each in types:
    id = (types.index(each) + 6)*10
    form['pd_base_type'] = each
    r = requests.post('https://us-news.zlongame.com/pd_search.jspx', data=form)
    content = [z['content_id'] for z in r.json()['list']]
    for each in content:
        datab = session.get('https://us-news.zlongame.com/sgammo/' + str(each) + '.jhtml')
        print(each)
        parse(datab)
    print(len(ammos))