from datetime import datetime
from sanic import Sanic
from sanic.response import json, text
import pymysql.cursors
from random import randint
import time
import json as js
import threading

db_conn = pymysql.Connect(host='127.0.0.1', user='pmauser', password='game0934', 
                        db='game_sql', cursorclass=pymysql.cursors.DictCursor)

app = Sanic("ARGame_Server")

#db function
def db_search_all(sql):
    result = ''
    with db_conn.cursor() as cur:
        cur.execute(sql)
        result = cur.fetchall()
    return result

def db_search_one(sql):
    result = ''
    with db_conn.cursor() as cur:
        cur.execute(sql)
        result = cur.fetchone()
    return result

def db_modify(sql):
    with db_conn.cursor() as cur:
        cur.execute(sql)
    db_conn.commit()
#-----------------------------------------------------------------------------------------------------
#skill_list
#對自己以外的目標施放技能=>`account`=target
#對自己施放技能=>`account`=account
fighter = {
    'skill_1':'UPDATE `status_{team_id}` SET `hp`=hp-{num} WHERE `account`=\'{target}\'', 
    'skill_2':'UPDATE `status_{team_id}` SET `enhance_de3`=enhance_de3+2 WHERE `account`=\'{target}\'', 
    'skill_3':'UPDATE `status_{team_id}` SET `hp`=hp-{num} WHERE `account`=\'{target}\'', 
    'skill_31':'UPDATE `status_{team_id}` SET `numb`=numb+1 WHERE `account`=\'{target}\'', 
    'skill_4':'UPDATE `status_{team_id}` SET `hp`=hp*0.8 WHERE `account`=\'{target}\'', 
    'skill_41':'UPDATE `status_{team_id}` SET `numb`=0,`sleep`=0,`poison`=0,`blood`=0,`drop_de1`=0,`drop_de2`=0,`drop_sk1`=0,`drop_sk2`=0 WHERE `account`=\'{account}\''
    }
            
traveler = {
    'skill_1':'UPDATE `status_{team_id}` SET `hp`=hp-{num} WHERE `account`=\'{target}\'', 
    'skill_2':'UPDATE `status_{team_id}` SET `enhance_sk1`=enhance_sk1+1 WHERE `account`=\'{target}\'', 
    'skill_3':'UPDATE `status_{team_id}` SET `gather`=gather+1 WHERE `account`=\'{account}\'', 
    'skill_31':'UPDATE `status_{team_id}` SET `numb`=numb+1 WHERE `account`=\'{target}\'', 
    'skill_4':'UPDATE `status_{team_id}` SET `hp`=hp-{num},`drop_sk2`=drop_sk2+3 WHERE `account`=\'{target}\''
    }

magician = {
    'skill_1':'UPDATE `status_{team_id}` SET `hp`=hp-{num} WHERE `account`=\'{target}\'', 
    'skill_2':'UPDATE `status_{team_id}` SET `enhance_de1`=enhance_de1+1 WHERE `account`=\'{m0}\' or `account`=\'{m1}\' or `account`=\'{m2}\' or `account`=\'{m3}\'', 
    'skill_3':'UPDATE `status_{team_id}` SET `hp`=hp-{num} WHERE `account`=\'{target}\'', 
    'skill_31':'UPDATE `status_{team_id}` SET `enhance_sk2`=enhance_sk2+2 WHERE `account`=\'{account}\'', 
    'skill_4':'UPDATE `status_{team_id}` SET `gather`=gather+2 WHERE `account`=\'{account}\'', 
    'skill_41':'UPDATE `status_{team_id}` SET `hp`=hp-{num} WHERE `account`=\'{target}\''
    }

assistant = {
    'skill_1':'UPDATE `status_{team_id}` SET `hp`=hp+{num} WHERE `account`=\'{m0}\' or `account`=\'{m1}\' or `account`=\'{m2}\' or `account`=\'{m3}\'', 
    'skill_2':'UPDATE `status_{team_id}` SET `enhance_sk2`=enhance_sk2+2,`enhance_de2`=enhance_de2+2 WHERE `account`=\'{target}\'', 
    'skill_3':'UPDATE `status_{team_id}` SET `numb`=0,`sleep`=0,`poison`=0,`blood`=0,`drop_de1`=0,`drop_de2`=0,`drop_sk1`=0,`drop_sk2`=0,`status_lock`=2 WHERE `account`=\'{m0}\' or `account`=\'{m1}\' or `account`=\'{m2}\' or `account`=\'{m3}\'', 
    'skill_31':'UPDATE `status_{team_id}` SET `hp`=hp+{num} WHERE `account`=\'{m0}\' or `account`=\'{m1}\' or `account`=\'{m2}\' or `account`=\'{m3}\'', 
    'skill_4':'UPDATE `status_{team_id}` SET `numb`=0,`sleep`=0,`poison`=0,`blood`=0,`drop_de1`=0,`drop_de2`=0,`drop_sk1`=0,`drop_sk2`=0 WHERE `account`=\'{m0}\' or `account`=\'{m1}\' or `account`=\'{m2}\' or `account`=\'{m3}\'', 
    'skill_41':'UPDATE `status_{team_id}` SET `enhance_de3`=enhance_sk2+5 WHERE `account`=\'{m0}\' or `account`=\'{m1}\' or `account`=\'{m2}\' or `account`=\'{m3}\''
    }
#-----------------------------------------------------------------------------------------------------
#compute_action
def compute_user_action(team_id):
    #取得玩家動作
    sql = 'SELECT * FROM `action_{team_id}`'
    result = db_search_all(sql.format(team_id=team_id))
    #逐個計算
    for i in range(0, len(result)):
        print("i=" + str(i))
        tmp = result[i]
        if tmp['action'] == '':
            continue
        #技能倍率
        if tmp['action'] != 'item_1' or 'item_2' or 'item_3' or 'item_4' or 'item_5' or 'item_6' or 'item_7':
            sql = 'SELECT `drop_sk1`,`drop_sk2`, `enhance_sk1`, `enhance_sk2`, `enhance_sk3`, `enhance_sk4` FROM `status_{team_id}` WHERE account=\'{account}\''
            damage_status = db_search_one(sql.format(team_id=team_id, account=tmp['account']))
            num = 1
            if damage_status['drop_sk1'] > 0:
                num *= 0.85
            elif damage_status['drop_sk2'] > 0:
                num *= 0.7
            elif damage_status['enhance_sk1'] > 0:
                num *= 1.15
            elif damage_status['enhance_sk2'] > 0:
                num *= 1.2
            elif damage_status['enhance_sk3'] > 0:
                num *= 1.5
            elif damage_status['enhance_sk4'] > 0:
                num *= 2.5
            else:
                num *= 1
            print("動作:" + str(tmp))
            print("倍率:" + str(num))
            #計算戰鬥資料
            sql = 'SELECT `career` FROM `user_skill` WHERE account=\'{account}\''
            career_result = db_search_one(sql.format(account=tmp['account']))
            #fighter
            if career_result['career'] == 'fighter':
                #fate = 0 機率效果不會發動，fate = 1 機率效果發動
                if (tmp['fate'] == 0) and (tmp['action'] != 'skill_4'):
                    sql = fighter[tmp['action']].format(team_id=team_id, target=tmp['target'], num=50*num)
                    db_modify(sql)

                elif (tmp['fate'] == 1) and ((tmp['action'] == 'skill_3') or (tmp['action'] == 'skill_4')):
                    if tmp['action'] == 'skill_3':
                        sql = fighter['skill_3'].format(team_id=team_id, target=tmp['target'], num=100*num)
                        db_modify(sql)
                        sql = fighter['skill_31'].format(team_id=team_id, target=tmp['target'])
                        db_modify(sql)

                    elif tmp['action'] == 'skill_4':
                        sql = fighter['skill_4'].format(team_id=team_id, target=tmp['target'])
                        db_modify(sql)
                        sql = fighter['skill_41'].format(team_id=team_id, target=tmp['account'])
                        db_modify(sql)
            #traveler
            elif career_result['career'] == 'traveler':
                if (tmp['fate'] == 0) and (tmp['action'] == 'skill_1'):
                    sql = traveler[tmp['action']].format(team_id=team_id, target=tmp['target'], num=60*num)
                    db_modify(sql)

                elif (tmp['fate'] == 0) and (tmp['action'] == 'skill_2'):
                    sql = traveler[tmp['action']].format(team_id=team_id, target=tmp['target'])
                    db_modify(sql)
                
                elif (tmp['fate'] == 0) and (tmp['action'] == 'skill_3'):
                    sql = traveler[tmp['action']].format(team_id=team_id, account=tmp['account'])
                    db_modify(sql)
                
                elif (tmp['fate'] == 0) and (tmp['action'] == 'skill_31'):
                    sql = traveler[tmp['action']].format(team_id=team_id, target=tmp['target'])
                    db_modify(sql)

                elif (tmp['fate'] == 0) and (tmp['action'] == 'skill_4'):
                    sql = traveler[tmp['action']].format(team_id=team_id, target=tmp['target'], num=200*num)
                    db_modify(sql)
            #magician
            elif career_result['career'] == 'magician':
                if (tmp['fate'] == 0) and (tmp['action'] == 'skill_1'):
                    sql = magician[tmp['action']].format(team_id=team_id, target=tmp['target'], num=60*num)
                    db_modify(sql)

                if (tmp['fate'] == 0) and (tmp['action'] == 'skill_2'):
                    sql = magician[tmp['action']].format(team_id=team_id, m0=result[0]['account'], m1=result[1]['account'], m2=result[2]['account'], m3=result[3]['account'])
                    db_modify(sql)

                if (tmp['fate'] == 0) and (tmp['action'] == 'skill_3'):
                    sql = magician[tmp['action']].format(team_id=team_id, target=tmp['target'], num=100*num)
                    db_modify(sql)
                    sql = magician['skill_31'].format(team_id=team_id, account=tmp['account'])
                    db_modify(sql)

                if (tmp['fate'] == 0) and (tmp['action'] == 'skill_4'):
                    sql = magician[tmp['action']].format(team_id=team_id, account=tmp['account'])
                    db_modify(sql)
                
                if (tmp['fate'] == 0) and (tmp['action'] == 'skill_41'):
                    sql = magician[tmp['action']].format(team_id=team_id, target=tmp['target'], num=500*num)
                    db_modify(sql)
            #assistant
            elif career_result['career'] == 'assistant':
                #持續恢復技能檢查
                sql = 'SELECT `assist_lock`,`account` FROM `status_{team_id}`'
                assist_lock = db_search_all(sql.format(team_id=team_id))
                for i in range(0, len(assist_lock)):
                    if assist_lock[i]['assist_lock'] <= 0:
                        continue
                    if assist_lock[i]['account'] == 'boss':
                        continue
                    if assist_lock[i]['assist_lock'] > 0:
                        sql = 'UPDATE `status_{team_id}` SET `hp`=hp+{num} WHERE `account`=\'{account}\''
                        db_modify(sql.format(team_id=team_id, num=200*num, account=assist_lock[i]['account']))
                #主要技能
                if (tmp['fate'] == 0) and (tmp['action'] == 'skill_1'):
                    sql = assistant[tmp['action']].format(team_id=team_id, num=150*num, m0=result[0]['account'], m1=result[1]['account'], m2=result[2]['account'], m3=result[3]['account'])
                    db_modify(sql)
                if (tmp['fate'] == 0) and (tmp['action'] == 'skill_2'):
                    sql = assistant[tmp['action']].format(team_id=team_id, target=tmp['target'])
                    db_modify(sql)
                if (tmp['fate'] == 0) and (tmp['action'] == 'skill_3'):
                    sql = assistant[tmp['action']].format(team_id=team_id, m0=result[0]['account'], m1=result[1]['account'], m2=result[2]['account'], m3=result[3]['account'])
                    db_modify(sql)
                    sql = assistant['skill_31'].format(team_id=team_id, num=200*num, m0=result[0]['account'], m1=result[1]['account'], m2=result[2]['account'], m3=result[3]['account'])
                    db_modify(sql)
                if (tmp['fate'] == 0) and (tmp['action'] == 'skill_4'):
                    sql = assistant[tmp['action']].format(team_id=team_id, m0=result[0]['account'], m1=result[1]['account'], m2=result[2]['account'], m3=result[3]['account'])
                    db_modify(sql)
                    sql = assistant[tmp['action']].format(team_id=team_id, m0=result[0]['account'], m1=result[1]['account'], m2=result[2]['account'], m3=result[3]['account'])
                    db_modify(sql)
        else:
            print('still have long way')      
#-----------------------------------------------------------------------------------------------------
#just for test
@app.get("/test")
async def test(request):
    try:
        return text("Hello World")
    except Exception as e:
        return text(str(e))

@app.get("/favicon.ico")
async def fav(request):
    return text("nothing")
#-----------------------------------------------------------------------------------------------------
#about item issue
@app.post("/user_item")
async def user_info(request):
    try:
        account = request.json['account']
        sql = 'SELECT * FROM `user_item` WHERE account=\'' + str(account) + '\''
        #sql = 'SELECT * FROM `user_item` WHERE account='*******''
        result = db_search_one(sql)
        return json(result)
    except Exception as e:
        return text(str(e))

@app.post("/get_new_item")
async def get_new_item(request):
    try:
        account = request.json['account']
        item = request.json['item']
        search_item_num = 'SELECT ' + str(item) + ' FROM `user_item` WHERE account=\'' + str(account) + '\''
        result = db_search_one(search_item_num)
        num = int(result[item]) + 1
        sql = 'UPDATE `user_item` SET ' + str(item) + '=' + str(num) + ' WHERE account=\'' + str(account) + '\''
        db_modify(sql)
        str_re = '{\"item\":' + '\"' + item + '\"' + '}'
        return json(str_re)
    except Exception as e:
        print(str(e))
        return text("Explode")

@app.post("/use_item")
async def use_item(request):
    try:
        account = request.json['account']
        item = request.json['item']
        search_item_num = 'SELECT ' + str(item) + ' FROM `user_item` WHERE account=\'' + str(account) + '\''
        result = db_search_one(search_item_num)
        num = int(result[item]) - 1
        if num < 0:
            return text("Explode")
        else:
            sql = 'UPDATE `user_item` SET ' + str(item) + '=' + str(num) + ' WHERE account=\'' + str(account) + '\''
            db_modify(sql)
        return text("done")
    except Exception as e:
        print('error:' + str(e))
        return text("Explode")
#-----------------------------------------------------------------------------------------------------
#about skill issue
@app.post("/user_skill")
async def user_skill(requset):
    try:
        account = requset.json['account']
        sql = 'SELECT * FROM `user_skill` WHERE account=\'' + str(account) + '\''
        # sql = 'SELECT * FROM `user_skill` WHERE account='*******''
        result = db_search_one(sql)
        return json(result)
    except Exception as e:
        print('error:' + str(e))
        return text(str(e))

@app.post("/get_skill")
async def get_skill(request):
    try:
        account = request.json['account']
        skill = request.json['skill']
        result = ''
        sql = 'SELECT ' + str(skill) + ' FROM `user_skill` WHERE account=\'' + str(account) + '\''
        result = db_search_all(sql)
        chk = dict(result[0])[skill]
        if chk == 0:
            sql_skill = 'UPDATE `user_skill` SET ' + str(skill) + '=' + '1' + ' WHERE account=\'' + str(account) + '\''
            db_modify(sql_skill)
        else:
            return text("learned")
        return text("done")
    except Exception as e:
        print(str(e))
        return text("Explode")
#-----------------------------------------------------------------------------------------------------
#about account issue
@app.post("/sign_up")
async def sign_up(request):
    #start = time.time()
    try:
        account = request.json['account']
        password = request.json['password']
        name = request.json['name']
        sql_info = 'INSERT INTO `user_info` (account, password, name) VALUES' + '(\'' + account + '\',\'' + password + '\',\'' + name + '\')'
        #sql_info = 'INSERT INTO `user_info` (account, password, name) VALUES('test01', '********', '****')'
        sql_item = 'INSERT INTO `user_item` (account) VALUES' + '(\'' + account + '\')'
        #sql_item = 'INSERT INTO `user_item (account) VALUES('test01')'
        sql_skill = 'INSERT INTO `user_skill` (account) VALUES' + '(\'' + account + '\')'
        #sql_skill = 'INSERT INTO `user_skill (account) VALUES('test01')'
        db_modify(sql_info)
        db_modify(sql_item)
        db_modify(sql_skill)     
        #end = time.time()
        #print('Time use:' + str(end - start))  
        return text("註冊成功")
    except Exception as e:
        print('錯誤訊息：' + str(e))
        return text("帳號可能已經被註冊" + "\n" + "有疑問請洽管理員")
    
@app.post("/sign_in")
async def sign_in(request):
    try:
        account = request.json['account']
        password = request.json['password']
        sql = 'SELECT password FROM `user_info` WHERE account=\'' + str(account) + '\''
        #sql = 'SELECT password FROM `user_info` WHERE account='test01''
        result = db_search_all(sql)
        if dict(result[0])['password'] == password:
            return text("Succes")
        else:
            return text("Error")
    except Exception as e:
        print('Error Message:' + str(e))
        return text("Explode")

@app.post("select_career")
async def select_career(request):
    try:
        account = request.json['account']
        career = request.json['career']
        sql = 'UPDATE `user_skill` SET `career`=' + '\'' + career + '\'' + ' WHERE account=' + '\'' + account + '\''
        db_modify(sql)
        return text("done")
    except Exception as e:
        print(str(e))
        return text("Explode")

@app.post("get_career")
async def get_career(request):
    try:
        account = request.json['account']
        sql = 'SELECT `career` FROM `user_skill` WHERE account=' + '\'' + account + '\''
        result = db_search_one(sql)
        return json(result)
    except Exception as e:
        print(e)
        return text("Explode")

@app.post("/get_user_name")
async def get_user_name(request):
    try:
        account = request.json['account']
        sql = 'SELECT `name` FROM `user_info` WHERE account=\'{account}\''
        result = db_search_one(sql.format(account=account))
        return json(result)
    except Exception as e:
        print(str(e))
        return text("Explode")
#-----------------------------------------------------------------------------------------------------
#about status issue
@app.post("/change_status")
async def change_status(request):
    try:
        account = request.json['account']
        status = request.json['status']
        sql = 'UPDATE `user_info` SET play_status=' + str(status) + ' WHERE account=\'' + str(account) + '\''
        db_modify(sql)
        return text("done")
    except Exception as e:
        print(str(e))
        return text("Explode")

@app.post("/get_status")
async def get_status(request):
    try:
        account = request.json['account']
        sql = 'SELECT `play_status` FROM `user_info` WHERE account=' + '\'' + account + '\''
        result = db_search_one(sql)
        return json(result)
    except Exception as e:
        print(str(e))
        return text("Explode")
#-----------------------------------------------------------------------------------------------------
#about team issue
@app.post("/create_team")
async def create_team(request):
    try:
        account = request.json['account']
        id = randint(100000, 999999)
        sql_leader = 'INSERT INTO `teams` ' + '(leader, id) VALUES ' + '(\'' + account + '\',' + str(id) + ')'
        db_modify(sql_leader)
        sql_team_id = 'UPDATE `user_info` SET `team_id`=' + str(id) + ' WHERE account=' + '\'' + account + '\''
        db_modify(sql_team_id)
        return text("create done")
    except Exception as e:
        print(str(e))
        return text("Explode")

@app.post("/join_party")
async def join_party(request):
    start = time.time()
    try:
        account = request.json['account']
        id = request.json['id']
        sql = 'SELECT * FROM `teams` WHERE id=' + str(id)
        #sql = SELECT * FROM `teams` WHERE id=*
        result = db_search_one(sql)#type of `result` is dict
        for i in range(1, 4):
            tar = list(result.keys())[i]#transfer keys of `result` into list
            if result[tar] == '':#find out which member is empty
                sql = 'UPDATE `teams` SET ' + tar + '=' + '\'' + account + '\'' + ' WHERE id=' + str(id)
                #sql = UPDARE `teams` SET member*=account WHERE id=******
                db_modify(sql)
                sql = 'UPDATE `user_info` SET `team_id`=' + str(id) + ' WHERE account=' + '\'' + account + '\''
                db_modify(sql)
                end = time.time()
                print('Time use:' + str(end - start))
                return text("done")
            elif (i==3) and (result[tar] != ''):
                return text("team is full")
    except Exception as e:
        print(str(e))
        return text("Explode")

@app.post("/quit_team")
async def quit_team(request):
    start = time.time()
    try:
        account = request.json['account']
        id = request.json['id']
        sql = 'SELECT * FROM `teams` WHERE id=' + str(id)
        result = db_search_one(sql)#type of `result` is dict
        for i in range (0, 4):
            tar = list(result.keys())[i]#transfer keys of `result` into list 
            if (result[tar] == str(account)) and (tar != 'leader'):#find out account in which member and check is not leader
                sql = 'UPDATE `teams` SET ' + tar + '=\'\'' + ' WHERE id=' + str(id)
                #sql = UPDATE `teams` SET member*='' WHERE id=******
                db_modify(sql)
                end = time.time()
                print('Time use:' + str(end - start))
                return text("done")
            elif (result[tar] == str(account)) and (tar == 'leader'):#delete whole team
                sql = 'DELETE FROM `teams` WHERE ' + tar + '=\'' + str(account) + '\''
                #sql = DELETE FROM `teams` WHERE member*=account
                db_modify(sql)
                return text("done")
    except Exception as e:
        print(str(e))
        return text("Explode")

@app.post("/get_team_id")
async def get_team_id(request):
    try:
        account = request.json['account']
        sql = 'SELECT `team_id` FROM `user_info` WHERE account=' + '\'' + account + '\''
        result = db_search_one(sql)
        return json(result)
    except Exception as e:
        print(str(e))
        return text("Explode")

@app.post("get_team_member")
async def get_team_member(request):
    try:
        id = request.json['id']
        sql = 'SELECT * FROM `teams` WHERE id=' + str(id)
        result = db_search_one(sql)
        return json(result)
    except Exception as e:
        print(str(e))
        return text("Explode")
#-----------------------------------------------------------------------------------------------------
#about duel issue
@app.post("/duel_start")
async def duel_start(request):
    try:
        #start = time.time()
        #account of leader
        account = request.json['account']
        #change user play_status 
        sql = 'SELECT `team_id` FROM `user_info` WHERE account=\'{account}\''
        result = db_search_one(sql.format(account=account))
        id = result['team_id']
        sql = 'UPDATE `user_info` SET `play_status`=1 WHERE team_id={id}'
        db_modify(sql.format(id=id))
        #create table to store status data
        sql = 'CREATE TABLE IF NOT EXISTS `status_{id}`( \
                    `account` varchar(40) PRIMARY KEY NOT NULL, \
                    `hp` int NOT NULL DEFAULT \'0\', \
                    `turn_stat` int NOT NULL DEFAULT \'0\', \
                    `enhance_sk1` int NOT NULL DEFAULT \'0\', \
                    `enhance_sk2` int NOT NULL DEFAULT \'0\', \
                    `enhance_sk3` int NOT NULL DEFAULT \'0\', \
                    `enhance_sk4` int NOT NULL DEFAULT \'0\', \
                    `enhance_de1` int NOT NULL DEFAULT \'0\', \
                    `enhance_de2` int NOT NULL DEFAULT \'0\', \
                    `enhance_de3` int NOT NULL DEFAULT \'0\', \
                    `gather` int NOT NULL DEFAULT \'0\', \
                    `immortal` int NOT NULL DEFAULT \'0\', \
                    `numb` int NOT NULL DEFAULT \'0\', \
                    `sleep` int NOT NULL DEFAULT \'0\', \
                    `poison` int NOT NULL DEFAULT \'0\', \
                    `blood` int NOT NULL DEFAULT \'0\', \
                    `drop_de1` int NOT NULL DEFAULT \'0\', \
                    `drop_de2` int NOT NULL DEFAULT \'0\', \
                    `drop_sk1` int NOT NULL DEFAULT \'0\', \
                    `drop_sk2` int NOT NULL DEFAULT \'0\', \
                    `assist_lock` int NOT NULL DEFAULT \'0\' \
                )'
        db_modify(sql.format(id=id))
        sql = 'SELECT * FROM `teams` WHERE leader=\'{account}\''
        result = db_search_one(sql.format(account=account))
        for i in range (0, len(result)):
            tar = list(result.keys())
            sql = 'INSERT INTO `status_{id}` (account) VALUES (\'' + str(result[tar[i]]) + '\')'
            db_modify(sql.format(id=id))
        sql = 'INSERT INTO `status_{id}` (account) VALUES (\'boss\')'
        db_modify(sql.format(id=id))
        sql = 'CREATE TABLE IF NOT EXISTS `action_{id}`(\
                        `account` varchar(40) PRIMARY KEY NOT NULL, \
                        `action` varchar(40) NOT NULL DEFAULT \'\', \
                        `target` varchar(40) NOT NULL DEFAULT \'\', \
                        `fate` int NOT NULL DEFALT \'0\' \
                    )'
        db_modify(sql.format(id=id))
        for i in range (0, len(result)):
            tar = list(result.keys())
            sql = 'INSERT INTO `action_{id}` (account) VALUES (\'' + str(result[tar[i]]) + '\')'
            db_modify(sql.format(id=id))
        sql = 'INSERT INTO `action_{id}` (account) VALUES (\'boss\')'
        db_modify(sql.format(id=id))
        '''end = time.time()
        cost = end - start
        print('time cost:' + str(round(cost*1000, 3)) + 'ms')'''
        return text('done')
    except Exception as e:
        print(str(e))
        return text("Explode")

@app.post("/commit_status_data")
async def commit_status_data(request):
    try:
        id = request.json['id']
        account = request.json['account']
        start = time.time()
        #fdata is status json
        fdata = request.json #type of fdata is dict
        #key of fdata is status name 
        l_fdata = list(fdata.keys()) #transfer keys of fdata into list
        sql_update = ''
        #create update values
        for i in range (0, len(l_fdata)):
            if l_fdata[i] == 'id' or 'account':
                continue
            elif i <(len(fdata) - 1):
                sql_update += l_fdata[i] + '=' + '\'' + str(fdata[l_fdata[i]]) + '\'' + ',' 
                #`column`=`values`,
            else:
                sql_update += l_fdata[i] + '=' + '\'' + str(fdata[l_fdata[i]]) + '\''
        sql = 'UPDATE `status_' + str(id) + '`' + ' SET ' + sql_update + ' WHERE account=' + '\'' + account + '\''
        #sql = UPDATE `status_id` SET col1=val1, col2=val2... WHERE `account`=account
        db_modify(sql)
        end = time.time()
        cost = end - start
        print('time cost:' + str(round(cost*1000, 3)) + 'ms')
        return text('done')
    except Exception as e:
        print(str(e))
        return text("Explode")

@app.post("/get_last_status")
async def get_last_status(request):
    try:
        account = request.json['account']
        id = request.json['id']
        sql = 'SELECT * FROM `status_' + str(id) + '`' + ' WHERE account=' + '\'' + account + '\''
        result = db_search_one(sql)
        return json(result)
    except Exception as e:
        print(str(e))
        return text("Explode")

@app.post("/commit_user_action")
async def user_action(request):
    try:
        account = request.json['account']
        act = request.json['act']
        id = request.json['id']
        tar = request.json['tar']
        set = ' SET action=' + '\'' + act + '\',' + 'target=' + '\'' + tar + '\''
        sql = 'UPDATE `action_' + str(id) + '`' + set + ' WHERE account=' + '\'' + account + '\''
        db_modify(sql)
        return text("done")
    except Exception as e:
        print(str(e))
        return text("Explode")

@app.post("/get_action")
async def get_action(request):
    try:
        id = request.json['id']
        sql = 'SELECT `action` FROM `action_{id}`'
        result = db_search_all(sql.format(id=id))
        data = '{\"act\":['
        for i in range(0, len(result)):
            tar = result[i]#dict
            if tar['action'] == '':
                return text("batching")
            elif i < len(result) - 1:
                data += js.dumps(tar) + ','
            else:
                data += js.dumps(tar)
        data += ']}'
        t_compute_action = threading.Thread(target=compute_user_action, args=(id, ))
        t_compute_action.start()
        return text(data)
    except Exception as e:
        print(str(e))
        return text("Explode")

@app.post("/new_turn")
async def new_turn(requset):
    try:
        team_id = requset.json['id']
        account = requset.json['account']
        sql = 'SELECT `assist_lock`,`enhance_sk1`,`enhance_sk2`,`enhance_sk3`,`enhance_sk4`,`enhance_de1`,`enhance_de2`,`enhance_de3`,`gather`,`immortal`,`numb`,`sleep`,`posion`,`blood`,`drop_de1`,`drop_de2`,`drop_sk1`,`drop_sk2` \
                FROM `status_{team_id}` WHERE `account`=\'{account}\''
        result = db_search_one(sql.format(team_id=team_id,account=account))
        tmp_key = list(result.keys())
        tmp_update = ''
        for i in range (0, len(tmp_key)):
            if result[tmp_key[i]] == 0:
                continue
            else:
                result[tmp_key[i]] -= 1
                tmp_update += tmp_key[i] + '=' + str(result[tmp_key[i]]) + ','
        update = tmp_update.rstrip(',')
        sql = 'UPDATE `status_{team_id}` SET {update} WHERE `account`=\'{account}\''
        db_modify(sql.format(update=update, team_id=team_id,account=account))
        return text("done")
    except Exception as e:
        print(str(e))
        return text("Explode")

@app.post("/end_turn")
async def end_turn(request):
    try:
        id = request.json['id']
        account = request.json['account']
        sql = 'UPDATE `action_' + str(id) + '`' + ' SET action=\'\' WHERE account=\'{account}\''
        db_modify(sql.format(account=account))
        return text("done")
    except Exception as e:
        print(str(e))
        return text("Explode")

@app.post("/finish_game")
async def finish_game(request):
    try:
        account = request.json['account']
        id = request.json['id']
        data = request.json['data']
        sql = 'UPDATE `user_info` SET play_status=0 WHERE account=' + '\'' + account + '\''
        db_modify(sql)
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        sql = 'INSERT INTO `reward` (account, team_id, data, time) VALUES ( ' + \
                '\'' + account + '\',' + \
                '\'' + str(id) + '\',' + \
                '\'' + str(data) + '\',' + \
                '\'' + now + '\'' + \
                ')'
        db_modify(sql)
        sql = 'DROP TABLE IF EXISTS `action_' + str(id) + '`'
        db_modify(sql)
        sql = 'DROP TABLE IF EXISTS `status_' + str(id) + '`'
        db_modify(sql)
        return text("done")
    except Exception as e:
        print(str(e))
        return text("Explode")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='2500', debug=False, access_log=True)
    app.config['workers'] = '4'