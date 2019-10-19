import requests
from requests_html import HTMLSession
import json

types = ["Damage Enhancer","Range Enhancer","Electronics","Shield Enhancer","Piloting Enhancer"]

effects = {

}

form = {
    'appId': 1,
    'order': 1,
    'pageNumber': 1,
    'pageCounts': 250,
    'title': "",
    'channel': 258
}
components = {}
session = HTMLSession()
header = {'user_agent':'skeet skeet yeet','Accept-Encoding':'gzip'}

def num_there(s):
    return any(i.isdigit() for i in s)

def writer(target,tbw):
    with open(target,'w') as outfile:
        json.dump(tbw,outfile)

def intextract(string):
    flat = [item for sublist in string for item in sublist]
    base = [x for x in flat if x.isdigit() or x == "."]
    while base[-1] == ".":
        base.pop()
    while base[0] == ".":
        base.pop(0)
    return(float(''.join(base)))

def parse(data):
    component = {}
    if id == 10:
        name = data.html.find(".weapon_inner_show_desc.fl > h2", first=True).text
        component['name'] = name
        if 'Artillery' in name:
            if 'Damage' in name:
                component['id'] = 1502
                component['effects'] = 102
                component['effects2'] = 0
            if 'Tracking' in name:
                component['id'] = 1504
                component['effects'] = 104
                component['effects2'] = 103
        if 'Laser' in name:
            if 'Damage' in name:
                component['id'] = 1102
                component['effects'] = 602
                component['effects2'] = 0
            if 'Tracking' in name:
                component['id'] = 1104
                component['effects'] = 604
                component['effects2'] = 603
            if 'Critical' in name:
                component['id'] = 1105
                component['effects'] = 605
                component['effects2'] = 604
        if 'Blaster' in name:
            if 'Damage' in name:
                component['id'] = 1202
                component['effects'] = 702
                component['effects2'] = 0
            if 'Tracking' in name:
                component['id'] = 1204
                component['effects'] = 704
                component['effects2'] = 703
            if 'Critical' in name:
                component['id'] = 1205
                component['effects'] = 705
                component['effects2'] = 704
        if 'Missile' in name:
            if 'Damage' in name:
                component['id'] = 1302
                component['effects'] = 802
                component['effects2'] = 0
            if 'Tracking' in name:
                component['id'] = 1304
                component['effects'] = 804
                component['effects2'] = 803
            if 'Critical' in name:
                component['id'] = 1305
                component['effects'] = 805
                component['effects2'] = 804
        if 'Railgun' in name:
            if 'Damage' in name:
                component['id'] = 1402
                component['effects'] = 902
                component['effects2'] = 0
            if 'Tracking' in name:
                component['id'] = 1404
                component['effects'] = 904
                component['effects2'] = 903
            if 'Critical' in name:
                component['id'] = 1405
                component['effects'] = 905
                component['effects2'] = 904
        if 'Vulnerability Strike' in name:
            component['id'] = 1005
            component['effects'] = 55
            component['effects2'] = 0
        if 'Vulnerability Analysis' in name:
            component['id'] = 1006
            component['effects'] = 56
            component['effects2'] = 0
        for each in data.html.find(".weapon_inner_show_desc.fl > p"):
            if 'Tech Level' in each.text:
                component['tech'] = intextract(each.text)
            if 'Rank' in each.text:
                component['rank'] = intextract(each.text)
                name = name + " " + str(int(component['rank']))
                component['name'] = name
        for each in data.html.find(".weapon_inner_list_list > li"):
            if 'Processor' in each.text:
                component['processor'] = intextract(each.text)
            if 'Power' in each.text:
                component['power'] = intextract(each.text)
        if component['id'] == 1005 or component['id'] == 1006:
            yeet = data.html.find(".weapon_inner_list_list > li")
            for each in yeet:
                if 'Crit' in each.text:
                    component['effect'] = intextract(each.text)
        else:
            yeet = data.html.find(".weapon_inner_attr > .weapon_inner_list_list")
            component['effect'] = intextract(yeet[0].text)
            if not component['id'] % 100 == 2:
                yeet = data.html.find(".weapon_inner_attr.zj_switch_parent > .weapon_inner_list_list")
                component['effect2'] = -1 * intextract(yeet[0].text)
    if id == 20:
        name = data.html.find(".weapon_inner_show_desc.fl > h2", first=True).text
        component['name'] = name
        if 'Artillery' in name:
            if 'Range' in name:
                component['id'] = 1503
                component['effects'] = 103
                component['effects2'] = 0
        if 'Laser' in name:
            if 'Range' in name:
                component['id'] = 1103
                component['effects'] = 603
                component['effects2'] = 8
        if 'Blaster' in name:
            if 'Range' in name:
                component['id'] = 1203
                component['effects'] = 703
                component['effects2'] = 8
        if 'Missile' in name:
            if 'Range' in name:
                component['id'] = 1303
                component['effects'] = 803
                component['effects2'] = 8
        if 'Railgun' in name:
            if 'Range' in name:
                component['id'] = 1403
                component['effects'] = 903
                component['effects2'] = 8
        for each in data.html.find(".weapon_inner_show_desc.fl > p"):
            if 'Tech Level' in each.text:
                component['tech'] = intextract(each.text)
            if 'Rank' in each.text:
                component['rank'] = intextract(each.text)
                name = name + " " + str(int(component['rank']))
                component['name'] = name
        for each in data.html.find(".weapon_inner_list_list > li"):
            if 'Processor' in each.text:
                component['processor'] = intextract(each.text)
            if 'Power' in each.text:
                component['power'] = intextract(each.text)
        yeet = data.html.find(".weapon_inner_attr > .weapon_inner_list_list")
        component['effect'] = intextract(yeet[0].text)
        try:
            yeet = data.html.find(".weapon_inner_attr.zj_switch_parent > .weapon_inner_list_list")
            component['effect2'] = -1 * intextract(yeet[0].text)
        except:
            component['effect2'] = 0
    if id == 30:
        name = data.html.find(".weapon_inner_show_desc.fl > h2", first=True).text
        component['name'] = name
        if 'Co-Processor' in name:
            component['id'] = 1610
            component['effects'] = 4
            component['effects2'] = 0
        if 'Power Core' in name:
            component['id'] = 1620
            component['effects'] = 5
            component['effects2'] = 0
        if 'Energy Battery' in name:
            component['effects'] = 29
            component['effects2'] = 0
            if 'S-Auxiliary' in name:
                component['id'] = 1631
            if 'M-Auxiliary' in name:
                component['id'] = 1632
            if 'L-Auxiliary' in name:
                component['id'] = 1633
        if 'Energy Recovery' in name:
            component['id'] = 1640
            component['effects'] = [10,4201]
            component['effects2'] = 0
        if 'Energy Projection' in name:
            component['id'] = 1650
            component['effects'] = [5201,6201]
            component['effects2'] = 10
        for each in data.html.find(".weapon_inner_show_desc.fl > p"):
            if 'Tech Level' in each.text:
                component['tech'] = intextract(each.text)
            if 'Rank' in each.text:
                component['rank'] = intextract(each.text)
                name = name + " " + str(int(component['rank']))
                component['name'] = name
        for each in data.html.find(".weapon_inner_list_list > li"):
            if 'Processor' in each.text:
                component['processor'] = intextract(each.text)
            if 'Power' in each.text:
                component['power'] = intextract(each.text)
        yeet = data.html.find(".weapon_inner_attr > .weapon_inner_list_list")
        if component['id'] == 1640:
            component['effect'] = intextract(yeet[0].text.split('%')[0])
            component['effect2'] = component['effect']
        else:
            component['effect'] = intextract(yeet[0].text)
        try:
            yeet = data.html.find(".weapon_inner_attr.zj_switch_parent > .weapon_inner_list_list")
            component['effect2'] = -1 * intextract(yeet[0].text)
        except:
            component['effect2'] = 0
    if id == 40:
        name = data.html.find(".weapon_inner_show_desc.fl > h2", first=True).text
        component['name'] = name
        if 'Extender' in name:
            component['effects'] = 29
            component['effects2'] = 0
            if 'S-Shield' in name:
                component['id'] = 1711
            if 'M-Shield' in name:
                component['id'] = 1712
            if 'L-Shield' in name:
                component['id'] = 1713
        if 'Power Relay' in name:
            component['effects'] = 29
            component['effects2'] = 4101
            if 'S-Shield' in name:
                component['id'] = 1721
            if 'M-Shield' in name:
                component['id'] = 1722
            if 'L-Shield' in name:
                component['id'] = 1723
        if 'Res Enhancer' in name:
            if 'Adaptive' in name:
                component['id'] = 1740
                component['effects'] = 3
                component['effects2'] = 0
            if 'EM' in name:
                component['id'] = 1731
                component['effects'] = 31
                component['effects2'] = 0
            if 'Thermal' in name:
                component['id'] = 1732
                component['effects'] = 32
                component['effects2'] = 0
            if 'Kinetic' in name:
                component['id'] = 1733
                component['effects'] = 33
                component['effects2'] = 0
        if 'Amplifier' in name:
            if 'EM' in name:
                component['id'] = 1751
                component['effects'] = 31
                component['effects2'] = 12
            if 'Heat' in name:
                component['id'] = 1752
                component['effects'] = 32
                component['effects2'] = 12
            if 'Kinetic' in name:
                component['id'] = 1753
                component['effects'] = 33
                component['effects2'] = 12
        if 'Shield Recharge Augmentor' in name:
            if '(A)' in name:
                component['id'] = 1760
                component['effects'] = [4201,5201,6201]
                component['effects2'] = 0
            if "(B)" in name:
                component['id'] = 1770
                component['effects'] = 4201
                component['effects2'] = 9
        if 'Shield Projection' in name:
            component['id'] = 1780
            component['effects'] = [5201, 6201]
            component['effects2'] = 52
        if 'Shield Radiation' in name:
            component['id'] = 1790
            component['effects'] = 12
            component['effects2'] = 2
        for each in data.html.find(".weapon_inner_show_desc.fl > p"):
            if 'Tech Level' in each.text:
                component['tech'] = intextract(each.text)
            if 'Rank' in each.text:
                component['rank'] = intextract(each.text)
                name = name + " " + str(int(component['rank']))
                component['name'] = name
        for each in data.html.find(".weapon_inner_list_list > li"):
            if 'Processor' in each.text:
                component['processor'] = intextract(each.text)
            if 'Power' in each.text:
                component['power'] = intextract(each.text)
        yeet = data.html.find(".weapon_inner_attr > .weapon_inner_list_list")
        if component['id'] == 1760 or component['id'] == 1740:
            component['effect'] = intextract(yeet[0].text.split('%')[0])
            component['effect2'] = component['effect']
        else:
            component['effect'] = intextract(yeet[0].text)
        try:
            yeet = data.html.find(".weapon_inner_attr.zj_switch_parent > .weapon_inner_list_list")
            component['effect2'] = -1 * intextract(yeet[0].text)
        except:
            component['effect2'] = 0
    if id == 50:
        name = data.html.find(".weapon_inner_show_desc.fl > h2", first=True).text
        component['name'] = name
        if 'Auxiliary Propulsion' in name:
            component['id'] = 1810
            component['effects'] = 8
            component['effects2'] = 0
        if 'Overdrive' in name:
            component['id'] = 1820
            component['effects'] = 8
            component['effects2'] = 11
        if 'Control Engine' in name:
            component['id'] = 1830
            component['effects'] = 11
            component['effects2'] = 0
        if 'Titanium Plating' in name:
            component['id'] = 1840
            component['effects'] = 11
            component['effects2'] = 1
        if 'Expanded Cargo' in name:
            component['id'] = 1850
            component['effects'] = 14
            component['effects2'] = 0
        if 'Warp Core Stabilizer' in name:
            component['id'] = 1860
            component['effects'] = 26
            component['effects2'] = 0
        if 'Warp Core Cover' in name:
            component['id'] = 1870
            component['effects'] = 26
            component['effects2'] = 53
        if 'Warp Accelerator' in name:
            component['id'] = 1880
            component['effects'] = 8
            component['effects2'] = 7
        for each in data.html.find(".weapon_inner_show_desc.fl > p"):
            if 'Tech Level' in each.text:
                component['tech'] = intextract(each.text)
            if 'Rank' in each.text:
                component['rank'] = intextract(each.text)
                name = name + " " + str(int(component['rank']))
                component['name'] = name
        for each in data.html.find(".weapon_inner_list_list > li"):
            if 'Processor' in each.text:
                component['processor'] = intextract(each.text)
            if 'Power' in each.text:
                component['power'] = intextract(each.text)
        yeet = data.html.find(".weapon_inner_attr > .weapon_inner_list_list")
        component['effect'] = intextract(yeet[0].text)
        try:
            yeet = data.html.find(".weapon_inner_attr.zj_switch_parent > .weapon_inner_list_list")
            component['effect2'] = -1 * intextract(yeet[0].text.split('%')[0])
        except:
            component['effect2'] = 0
    if not 'effect2' in component:
        component['effect2'] = 0
    components[name] = component
    if component['tech'] == 1:
        if component['rank'] == 1:
            print(component)
    if component['tech'] == 3:
        if component['rank'] == 5:
            print(component)

for each in types:
    id = (types.index(each) + 1)*10
    form['pd_base_type'] = each
    r = requests.post('https://us-news.zlongame.com/pd_search.jspx', data=form)
    content = [z['content_id'] for z in r.json()['list']]
    for each in content:
        datab = session.get('https://us-news.zlongame.com/sgdevice/' + str(each) + '.jhtml')
        parse(datab)
    print(len(components))

writer('Components.json',components)