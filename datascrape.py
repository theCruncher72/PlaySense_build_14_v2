import requests
import os
import json
import pymongo
import time

def get_details(appid):
    url = 'https://store.steampowered.com/api/appdetails?appids='
    time.sleep(1)
    response = requests.get(url=url+str(appid)+'&cc=in', headers={'User-Agent': 'Mozilla/5.0'}, hooks={'response':'done'})
    return response.text

def dict_convert(json_string):
    dict_file = json.loads(json_string)
    return dict_file

def filter_game(dict_file,appid):
    y = dict_file
    flag = 0
    try:
        check_val = y[str(appid)]['data']['type']
        if(check_val=='game'):
            flag = 1
    except:
        flag = 0
    return flag

def exe(fileresult,appid,dataf):
    if (fileresult == 1) :
        json_object = json.dumps(dataf, indent=4)
        with open('E:/code dump/test/venv/resultfile/scarpe_results/steam_'+str(appid)+'.json', 'w') as outfile:
            outfile.write(json_object)
        return json_object

def run():
    with open('E:/code dump/test/venv/resultfile/appid_file.txt', 'r') as appid_file:
        # convert appid.txt file to list var
        data = appid_file.read()
        listvar = data.split("\n")

    gameappcount = 0
    errcount = 0
    err_appid = []
    # limitter: limits appid entries start at 1 for easier counting
    listcount = 1
    for i in listvar:
        #i is appid
        try:
            if(listcount<=5250):
                if((listcount % 180) == 0):
                    print('waiting')
                    time.sleep(60)
                print(i)
                print(gameappcount)
                dataf = get_details(i)
                dictobj = dict_convert(dataf)
                fileresult = filter_game(dictobj,i)
                mongo_file = exe(fileresult, i, dictobj)
                client = pymongo.MongoClient("mongodb+srv://user_e:i1ETzmXh3Dh99Hyj@cluster0.va8s0xd.mongodb.net/?retryWrites=true&w=majority")
                db = client['steamdata']
                mon = json.loads(mongo_file)
                print(mon)
                print(errcount)
                print(err_appid)
                bing = db.bing
                bing.insert_one(mon)
                listcount = listcount + 1
                gameappcount = gameappcount + 1
            else:
                break
        except:
            if ((listcount % 180) == 0):
                print(waiting)
                time.sleep(60)
            errcount = errcount + 1
            if (errcount > 0):
                err_appid.append(i)
            listcount = listcount + 1

run()