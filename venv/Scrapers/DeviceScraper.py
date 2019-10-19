import requests
from requests_html import HTMLSession
import json

types = ["Enhancer","Area Enhancer","Extended Enhancer","Recharger","Area Recharger","Extended Recharger","Tactical","Area Interference","Extended Interference"]

effects = {
    110: 8,
    120: 8,
    131: 31,
    132: 32,
    133: 33,
    140: 3,
    151: 52,
    152: 53,
    153: 56,
    154: 54,
    211: 31,
    212: 32,
    213: 33,
    220: 3,
    230: 8,
    241: 52,
    242: 53,
    243: 56,
    244: 54,
    311: 31,
    312: 32,
    313: 33,
    320: 3,
    330: 8,
    410: 13,
    420: 10,
    510: 13,
    520: 10,
    610: 13,
    620: 10,
    711: 0,
    712: 0,
    713: 0,
    720: 0,
    730: 22,
    741: 0,
    742: 0,
    743: 0,
    810: 3,
    821: 31,
    822: 32,
    823: 33,
    830: 8,
    840: 26,
    850: 52,
    860: 53,
    870: 54,
    880: 12,
    890: 10,
    910: 3,
    921: 31,
    922: 32,
    923: 33,
    930: 8,
    940: 26,
    950: 52,
    960: 53,
    970: 54,
    980: 12,
    990: 10,
}

form = {
    'appId': 1,
    'order': 1,
    'pageNumber': 1,
    'pageCounts': 250,
    'title': "",
    'channel': 259
}
devices = {}
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
    device = {}
    if id == 10:
        name = data.html.find(".weapon_inner_show_desc.fl > h2", first=True).text
        device['name'] = name
        if 'Thruster' in name:
            if 'Agility' in name:
                device['id'] = 120
                device['effect2'] = 20
                device['effects2'] = 11
            else:
                device['id'] = 110
        if 'Screen' in name:
            if 'Adaptive' in name:
                device['id'] = 140
            else:
                if 'EM' in name:
                    device['id'] = 131
                if 'Heat' in name:
                    device['id'] = 132
                if 'Kinetic' in name:
                    device['id'] = 133
        if 'Enhancer' in name:
            if 'Damage' in name:
                device['id'] = 151
            if 'Range' in name:
                device['id'] = 152
            if 'Critical' in name:
                device['id'] = 153
            if 'Precision' in name:
                device['id'] = 154
        for each in data.html.find(".weapon_inner_show_desc.fl > p"):
            if 'Tech Level' in each.text:
                device['tech'] = intextract(each.text)
            if 'Rank' in each.text:
                device['rank'] = intextract(each.text)
                name = name + " " + str(int(device['rank']))
                device['name'] = name
        for each in data.html.find(".weapon_inner_list_list > li"):
            if 'Processor' in each.text:
                device['processor'] = intextract(each.text)
            if 'Power' in each.text:
                device['power'] = intextract(each.text)
            if 'Startup Energy' in each.text:
                device['activation'] = intextract(each.text)
            if 'Cooldown' in each.text:
                device['cooldown'] = intextract(each.text)
        for each in data.html.find(".fl.dis_l"):
            words = each.text.split()
            for each in words:
                if each == "20%":
                    if device['id'] == 12:
                        words.remove(each)
            for each in words:
                if '%' in each:
                    device['effect'] = intextract(each)
                    words.remove(each)
            word = ''.join(words)
            device['effectTime'] = intextract(word)
    elif id == 20:
        device = {}
        name = data.html.find(".weapon_inner_show_desc.fl > h2", first=True).text
        device['name'] = name
        if 'Field' in name:
            if 'Adaptive' in name:
                device['id'] = 220
            else:
                if 'EM' in name:
                    device['id'] = 211
                if 'Thermal' in name:
                    device['id'] = 212
                if 'Kinetic' in name:
                    device['id'] = 213
        if 'Velocity' in name:
            device['id'] = 230
        if 'Link' in name:
            if 'Damage' in name:
                device['id'] = 241
            if 'Range' in name:
                device['id'] = 242
            if 'Critical' in name:
                device['id'] = 243
            if 'Precision' in name:
                device['id'] = 244
        for each in data.html.find(".weapon_inner_show_desc.fl > p"):
            if 'Tech Level' in each.text:
                device['tech'] = intextract(each.text)
            if 'Rank' in each.text:
                device['rank'] = intextract(each.text)
                name = name + " " + str(int(device['rank']))
                device['name'] = name
        for each in data.html.find(".weapon_inner_list_list > li"):
            if 'Processor' in each.text:
                device['processor'] = intextract(each.text)
            if 'Power' in each.text:
                device['power'] = intextract(each.text)
            if 'Startup Energy' in each.text:
                device['activation'] = intextract(each.text)
            if 'Cooldown' in each.text:
                device['cooldown'] = intextract(each.text)
        for each in data.html.find(".fl.dis_l"):
            words = each.text.split()
            for each in words:
                if each == 'ally':
                    words.pop(words.index(each)-1)
                if 's' in each:
                    if num_there(each):
                        device['effectTime'] = intextract(each)
                        words.remove(each)
            word = ''.join(words)
            device['effect'] = intextract(word)
    elif id == 30:
        name = data.html.find(".weapon_inner_show_desc.fl > h2", first=True).text
        device['name'] = name
        if 'Res' in name:
            if 'Adaptive' in name:
                device['id'] = 320
            else:
                if 'EM' in name:
                    device['id'] = 311
                if 'Thermal' in name:
                    device['id'] = 312
                if 'Kinetic' in name:
                    device['id'] = 313
        elif 'Velocity' in name:
            device['id'] = 330
        for each in data.html.find(".weapon_inner_show_desc.fl > p"):
            if 'Tech Level' in each.text:
                device['tech'] = intextract(each.text)
            if 'Rank' in each.text:
                device['rank'] = intextract(each.text)
                name = name + " " + str(int(device['rank']))
                device['name'] = name
        for each in data.html.find(".weapon_inner_list_list > li"):
            if 'Processor' in each.text:
                device['processor'] = intextract(each.text)
            if 'Power' in each.text:
                device['power'] = intextract(each.text)
            if 'Startup Energy' in each.text:
                device['activation'] = intextract(each.text)
            if 'Cooldown' in each.text:
                device['cooldown'] = intextract(each.text)
        for each in data.html.find(".fl.dis_l"):
            words = each.text.split()
            for each in words:
                if '%' in each:
                    device['effect'] = intextract(each)
                    words.remove(each)
            word = ''.join(words)
            device['effectTime'] = intextract(word)
    elif id == 40:
        name = data.html.find(".weapon_inner_show_desc.fl > h2", first=True).text
        device['name'] = name
        if 'Shield' in name:
            device['id'] = 410
        elif 'Energy' in name:
            device['id'] = 420
        for each in data.html.find(".weapon_inner_show_desc.fl > p"):
            if 'Tech Level' in each.text:
                device['tech'] = intextract(each.text)
            if 'Rank' in each.text:
                device['rank'] = intextract(each.text)
                name = name + " " + str(int(device['rank']))
                device['name'] = name
        for each in data.html.find(".weapon_inner_list_list > li"):
            if 'Processor' in each.text:
                device['processor'] = intextract(each.text)
            if 'Power' in each.text:
                device['power'] = intextract(each.text)
            if 'Startup Energy' in each.text:
                device['activation'] = intextract(each.text)
            if 'Cooldown' in each.text:
                device['cooldown'] = intextract(each.text)
        for each in data.html.find(".fl.dis_l"):
            words = each.text.split()
            for each in words:
                if num_there(each):
                    if 's' in each:
                        device['effectTime'] = intextract(each)
                        words.remove(each)
            word = ''.join(words)
            device['effect'] = intextract(word)
    elif id == 50:
        name = data.html.find(".weapon_inner_show_desc.fl > h2", first=True).text
        device['name'] = name
        if 'Shield' in name:
            device['id'] = 510
        elif 'Energy' in name:
            device['id'] = 520
        for each in data.html.find(".weapon_inner_show_desc.fl > p"):
            if 'Tech Level' in each.text:
                device['tech'] = intextract(each.text)
            if 'Rank' in each.text:
                device['rank'] = intextract(each.text)
                name = name + " " + str(int(device['rank']))
                device['name'] = name
        for each in data.html.find(".weapon_inner_list_list > li"):
            if 'Processor' in each.text:
                device['processor'] = intextract(each.text)
            if 'Power' in each.text:
                device['power'] = intextract(each.text)
            if 'Startup Energy' in each.text:
                device['activation'] = intextract(each.text)
            if 'Cooldown' in each.text:
                device['cooldown'] = intextract(each.text)
        for each in data.html.find(".fl.dis_l"):
            words = each.text.split()
            for each in words:
                if each == 'ally':
                    words.pop(words.index(each)-1)
                if 's' in each:
                    if num_there(each):
                        device['effectTime'] = intextract(each)
                        words.remove(each)
            word = ''.join(words)
            device['effect'] = intextract(word)
    elif id == 60:
        name = data.html.find(".weapon_inner_show_desc.fl > h2", first=True).text
        device['name'] = name
        if 'Shield' in name:
            device['id'] = 610
        elif 'Energy' in name:
            device['id'] = 620
        for each in data.html.find(".weapon_inner_show_desc.fl > p"):
            if 'Tech Level' in each.text:
                device['tech'] = intextract(each.text)
            if 'Rank' in each.text:
                device['rank'] = intextract(each.text)
                name = name + " " + str(int(device['rank']))
                device['name'] = name
        for each in data.html.find(".weapon_inner_list_list > li"):
            if 'Processor' in each.text:
                device['processor'] = intextract(each.text)
            if 'Power' in each.text:
                device['power'] = intextract(each.text)
            if 'Startup Energy' in each.text:
                device['activation'] = intextract(each.text)
            if 'Cooldown' in each.text:
                device['cooldown'] = intextract(each.text)
        for each in data.html.find(".fl.dis_l"):
            words = each.text.split()
            for each in words:
                if num_there(each):
                    if 's' in each:
                        device['effectTime'] = intextract(each)
                        words.remove(each)
            word = ''.join(words)
            device['effect'] = intextract(word)
    elif id == 70:
        name = data.html.find(".weapon_inner_show_desc.fl > h2", first=True).text
        device['name'] = name
        if 'Flashjump' in name:
            if 'Short' in name:
                device['id'] = 711
            if 'Medium' in name:
                device['id'] = 712
            if 'Long' in name:
                device['id'] = 713
        elif 'Cloaking' in name:
            device['id'] = 720
        elif 'Generator' in name:
            device['id'] = 730
        elif 'Scanner' in name:
            if 'Radio' in name:
                device['id'] = 741
            if 'EM' in name:
                device['id'] = 742
            if 'Gravitational' in name:
                device['id'] = 743
        for each in data.html.find(".weapon_inner_show_desc.fl > p"):
            if 'Tech Level' in each.text:
                device['tech'] = intextract(each.text)
            if 'Rank' in each.text:
                device['rank'] = intextract(each.text)
                name = name + " " + str(int(device['rank']))
                device['name'] = name
        for each in data.html.find(".weapon_inner_list_list > li"):
            if 'Processor' in each.text:
                device['processor'] = intextract(each.text)
            if 'Power' in each.text:
                device['power'] = intextract(each.text)
            if 'Startup Energy' in each.text:
                device['activation'] = intextract(each.text)
            if 'Cooldown' in each.text:
                device['cooldown'] = intextract(each.text)
        if device['id'] < 720:
            for each in data.html.find(".fl.dis_l"):
                words = each.text.split()
                for each in words:
                    if num_there(each):
                        if 's' in each:
                            device['effectTime'] = intextract(each)
                            words.remove(each)
                        if '%' in each:
                            device['effect'] = intextract(each)
        elif device['id'] == 720:
            device['effect'] = 0
            for each in data.html.find(".fl.dis_l"):
                words = each.text.split()
                for each in words:
                    if num_there(each):
                        if 's' in each:
                            device['effectTime'] = intextract(each)
        elif device['id'] == 730:
            for each in data.html.find(".fl.dis_l"):
                words = each.text.split()
                for each in words:
                    if num_there(each):
                        if 's' in each:
                            device['effectTime'] = intextract(each)
                            words.remove(each)
                word = ''.join(words)
                device['effect'] = intextract(word)
        elif device['id'] == 740:
            device['effectTime'] = 0
            device['effect'] = intextract(data.html.find(".fl.dis_l",first=True).text)
    elif id == 80:
        device = {}
        name = data.html.find(".weapon_inner_show_desc.fl > h2", first=True).text
        device['name'] = name
        if 'Res' in name:
            if 'Adaptive' in name:
                device['id'] = 810
            else:
                if 'EM' in name:
                    device['id'] = 821
                if 'Thermal' in name:
                    device['id'] = 822
                if 'Kinetic' in name:
                    device['id'] = 823
        if 'Propulsion' in name:
            device['id'] = 830
        if 'Warp' in name:
            device['id'] = 840
        if 'Damage' in name:
             device['id'] = 850
        if 'Range' in name:
            device['id'] = 860
        if 'Precision' in name:
            device['id'] = 870
        if 'Signal' in name:
            device['id'] = 880
        if 'Nullification' in name:
            device['id'] = 890
        for each in data.html.find(".weapon_inner_show_desc.fl > p"):
            if 'Tech Level' in each.text:
                device['tech'] = intextract(each.text)
            if 'Rank' in each.text:
                device['rank'] = intextract(each.text)
                name = name + " " + str(int(device['rank']))
                device['name'] = name
        for each in data.html.find(".weapon_inner_list_list > li"):
            if 'Processor' in each.text:
                device['processor'] = intextract(each.text)
            if 'Power' in each.text:
                device['power'] = intextract(each.text)
            if 'Startup Energy' in each.text:
                device['activation'] = intextract(each.text)
            if 'Cooldown' in each.text:
                device['cooldown'] = intextract(each.text)
        for each in data.html.find(".fl.dis_l"):
            words = each.text.split()
            for each in words:
                if each == 'enemy':
                    words.pop(words.index(each)-1)
                if 's' in each:
                    if num_there(each):
                        device['effectTime'] = intextract(each)
                        words.remove(each)
            word = ''.join(words)
            device['effect'] = intextract(word)
    elif id == 90:
        device = {}
        name = data.html.find(".weapon_inner_show_desc.fl > h2", first=True).text
        device['name'] = name
        if 'Res' in name:
            if 'Adaptive' in name:
                device['id'] = 910
            else:
                if 'EM' in name:
                    device['id'] = 921
                if 'Thermal' in name:
                    device['id'] = 922
                if 'Kinetic' in name:
                    device['id'] = 923
        if 'Propulsion' in name:
            device['id'] = 930
        if 'Warp' in name:
            device['id'] = 940
        if 'Damage' in name:
             device['id'] = 950
        if 'Range' in name:
            device['id'] = 960
        if 'Precision' in name:
            device['id'] = 970
        if 'Signal' in name:
            device['id'] = 980
        if 'Nullifier' in name:
            device['id'] = 990
        for each in data.html.find(".weapon_inner_show_desc.fl > p"):
            if 'Tech Level' in each.text:
                device['tech'] = intextract(each.text)
            if 'Rank' in each.text:
                device['rank'] = intextract(each.text)
                name = name + " " + str(int(device['rank']))
                device['name'] = name
        for each in data.html.find(".weapon_inner_list_list > li"):
            if 'Processor' in each.text:
                device['processor'] = intextract(each.text)
            if 'Power' in each.text:
                device['power'] = intextract(each.text)
            if 'Startup Energy' in each.text:
                device['activation'] = intextract(each.text)
            if 'Cooldown' in each.text:
                device['cooldown'] = intextract(each.text)
        for each in data.html.find(".fl.dis_l"):
            words = each.text.split()
            for each in words:
                if 's' in each:
                    if num_there(each):
                        device['effectTime'] = intextract(each)
                        words.remove(each)
            word = ''.join(words)
            device['effect'] = intextract(word)
    if 'range' not in device:
        device['range'] = 0
    if 'effect2' not in device:
        device['effect2'] = 0
    if 'effects2' not in device:
        device['effects2'] = 0
    device['effects'] =effects[device['id']]
    if device['tech'] == 1:
        if device['rank'] == 1:
            print(device)
    if device['tech'] == 3:
        if device['rank'] == 5:
            print(device)
    devices[name] = device

for each in types:
    id = (types.index(each) + 1)*10
    form['pd_base_type'] = each
    r = requests.post('https://us-news.zlongame.com/pd_search.jspx', data=form)
    content = [z['content_id'] for z in r.json()['list']]
    for each in content:
        datab = session.get('https://us-news.zlongame.com/sgdevice/' + str(each) + '.jhtml')
        parse(datab)
    print(len(devices))

writer('Devices.json',devices)