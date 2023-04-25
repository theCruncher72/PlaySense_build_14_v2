import json
import pymongo
import csv

client = pymongo.MongoClient("mongodb+srv://user_e:i1ETzmXh3Dh99Hyj@cluster0.va8s0xd.mongodb.net/?retryWrites=true&w=majority")
global db
global col
db = client['steamdata']
col = db.price
csv_col = db.csv_entries
global errcount
global errappid
errappid = []
#global head
#head = ['id','recommendations','name','is_free','steam_price','steam_link','epic_price','epic_link','tags','requirements_min','requirements_recom','release_date','background_img','screenshots','about_the_game','developers','publishers']

def make_coll_price(appid):
    global count
    x = db.bing.find()[count]
    print('x=')
    print (x)
    #process name for epic link look into it further.........................
    gname = x[str(appid)]['data']['name']
    gnamef = gname.lower()
    special_characters = ['@', '#', '$', '*', '&', '.', "'",':',';']
    for i in special_characters:
    # Replace the special character with an empty string
        gnamef = gnamef.replace(i,"")

    price_pydict = {
        'id' : appid,
        'recommendations' : '',
        'name' : x[str(appid)]['data']['name'],
        'is_free' : x[str(appid)]['data']['is_free'],
        'steam_price' : '',
        'steam_link' : 'https://store.steampowered.com/app/'+ str(appid),
        #need to scrape epic_price
        'epic_price' : '',
        #use lower case name to access site can add more links like this
        'epic_link' : 'https://store.epicgames.com/en-US/p/'+ gnamef.replace(' ','-'),
        'tags' : [],
        'requirements_min' : '',
        'requirements_recom' : '',
        'release_date' : x[str(appid)]['data']['release_date']['date'],
        'background_img': x[str(appid)]['data']['background_raw'],
        'screenshots' : [],
        #not there in the json'supported languages' : price_insobj.find(),
        'about_the_game' : x[str(appid)]['data']['about_the_game'],
        'developers' : '',
        'publishers' : x[str(appid)]['data']['publishers']
    }
    print(price_pydict)

    #
    #error handling
    #

    #steam price
    try:
        if(price_pydict['is_free'] == False):
            price_pydict['steam_price'] = (x[str(appid)]['data']['price_overview']['final'])/100
    except:
        pass

    #tags
    try:
        tags_vals = x[str(appid)]['data']['genres']
        for key in tags_vals:
            price_pydict['tags'].append(key['description'])
    except:
        pass

    #screenshots
    try:
        scrshot_vals = x[str(appid)]['data']['screenshots']
        for key in scrshot_vals:
            price_pydict['screenshots'].append(key['path_thumbnail'])
    except:
        pass

    #specs recommended
    try:
        price_pydict['requirements_recom'] = x[str(appid)]['data']['pc_requirements']['recommended']
    except:
        pass

    #specs min
    try:
        price_pydict['requirements_min'] = x[str(appid)]['data']['pc_requirements']['minimum']
    except:
        pass

    #recommendations
    try:
        price_pydict['recommendations'] = x[str(appid)]['data']['recommendations']['total']
    except:
        pass

    #developers
    try:
        price_pydict['developers'] = x[str(appid)]['data']['developers']
    except:
        pass

    print(price_pydict)
    #add new entry into new collection
    #col.insert_one(price_pydict)
    return price_pydict

def csv_convert(price_pydict,appid):
    errcount = 0
    try:
        global flag
        if(flag == 0):
            with open('E:/code dump/test/venv/resultfile/final_csv.csv', 'w+') as f:
                writer = csv.DictWriter(f, fieldnames=price_pydict.keys())
                writer.writeheader()
                flag = flag+1
                writer.writerow(price_pydict)
        else:
            with open('E:/code dump/test/venv/resultfile/final_csv.csv', 'a') as f:
                writer = csv.DictWriter(f, fieldnames=price_pydict.keys())
                writer.writerow(price_pydict)
    except:
        errcount = errcount + 1
        errappid.append(appid)


def updictdb(price_pydict):
    outline_dict = {
        str(price_pydict['id']) :{}
    }
    outline_dict[str(price_pydict['id'])] = price_pydict
    col.insert_one(outline_dict)

flag=0
count=0
with open ('E:/code dump/test/venv/resultfile/appid_file.txt', 'r') as appid_file:
    #convert appid.txt fioe to list var
    data = appid_file.read()
    listvar = data.split("\n")

#limitter: limits appid entries start at 1 for easier counting
listcount = 1
for i in listvar:
    if(listcount<=5230):
        print(i)
        dict_csv = make_coll_price(i)
        csv_convert(dict_csv,i)
        updictdb(dict_csv)
        count = count + 1
        listcount = listcount + 1
    else:
        break