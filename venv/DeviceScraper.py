import requests
from requests_html import HTMLSession
import json

types = ["Enhancer","Area Enhancer","Extended Enhancer","Recharger","Area Recharger","Extended Recharger","Tactical","Area Interference","Extended Interference"]

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
                device['id'] = id+2
            else:
                device['id'] = id+1
        if 'Screen' in name:
            if 'Adaptive' in name:
                device['id'] = id+4
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
                device['id'] = id+2
            else:
                if 'EM' in name:
                    device['id'] = 211
                if 'Thermal' in name:
                    device['id'] = 212
                if 'Kinetic' in name:
                    device['id'] = 213
        if 'Velocity' in name:
            device['id'] = 23
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
                device['id'] = id+1
            else:
                if 'EM' in name:
                    device['id'] = 311
                if 'Thermal' in name:
                    device['id'] = 312
                if 'Kinetic' in name:
                    device['id'] = 313
        elif 'Velocity' in name:
            device['id'] = 32
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
            device['id'] = 41
        elif 'Energy' in name:
            device['id'] = 42
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
            device['id'] = 51
        elif 'Energy' in name:
            device['id'] = 52
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
            device['id'] = 61
        elif 'Energy' in name:
            device['id'] = 62
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
            device['id'] = 72
        elif 'Generator' in name:
            device['id'] = 73
        elif 'Scanner' in name:
            device['id'] = 74
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
        if device['id'] > 700:
            for each in data.html.find(".fl.dis_l"):
                words = each.text.split()
                for each in words:
                    if num_there(each):
                        if 's' in each:
                            device['effectTime'] = intextract(each)
                            words.remove(each)
                        if '%' in each:
                            device['effect'] = intextract(each)
        elif device['id'] == 72:
            device['effect'] = 0
            for each in data.html.find(".fl.dis_l"):
                words = each.text.split()
                for each in words:
                    if num_there(each):
                        if 's' in each:
                            device['effectTime'] = intextract(each)
        elif device['id'] == 73:
            for each in data.html.find(".fl.dis_l"):
                words = each.text.split()
                for each in words:
                    if num_there(each):
                        if 's' in each:
                            device['effectTime'] = intextract(each)
                            words.remove(each)
                word = ''.join(words)
                device['effect'] = intextract(word)
        elif device['id'] == 74:
            device['effectTime'] = 0
            device['effect'] = intextract(data.html.find(".fl.dis_l",first=True).text)
    elif id == 80:
        device = {}
        name = data.html.find(".weapon_inner_show_desc.fl > h2", first=True).text
        device['name'] = name
        if 'Res' in name:
            if 'Adaptive' in name:
                device['id'] = id+1
            else:
                if 'EM' in name:
                    device['id'] = 821
                if 'Thermal' in name:
                    device['id'] = 822
                if 'Kinetic' in name:
                    device['id'] = 823
        if 'Velocity' in name:
            device['id'] = 83
        if 'Warp' in name:
            device['id'] = 84
        if 'Damage' in name:
             device['id'] = 85
        if 'Range' in name:
            device['id'] = 86
        if 'Precision' in name:
            device['id'] = 87
        if 'Signal' in name:
            device['id'] = 88
        if 'Nullification' in name:
            device['id'] = 89
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
                device['id'] = id+1
            else:
                if 'EM' in name:
                    device['id'] = 821
                if 'Thermal' in name:
                    device['id'] = 822
                if 'Kinetic' in name:
                    device['id'] = 823
        if 'Velocity' in name:
            device['id'] = 83
        if 'Warp' in name:
            device['id'] = 84
        if 'Damage' in name:
             device['id'] = 85
        if 'Range' in name:
            device['id'] = 86
        if 'Precision' in name:
            device['id'] = 87
        if 'Signal' in name:
            device['id'] = 88
        if 'Nullification' in name:
            device['id'] = 89
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
    devices[name] = device
    if device['tech'] == 1:
        if device['rank'] == 1:
            print(device)

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