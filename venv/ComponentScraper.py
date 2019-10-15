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
    base =[x for x in flat if x.isdigit() or x == "."]
    while base[-1] == ".":
        base.pop()
    while base[0] == ".":
        base.pop(0)
    return(float(''.join(base)))

def parse(data):
    name = data.html.find(".weapon_inner_show_desc.fl > h2", first=True).text
    print(name)

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