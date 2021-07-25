from sanic import Sanic
from sanic.response import json, text
import pymysql.cursors
from random import randint
import time
import datetime

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
        result = ''
        return text("done")
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
        account = request.json['account']#account of leader
        #force change user play_status 
        sql = 'SELECT `team_id` FROM `user_info` WHERE account=' + '\'' + account + '\''
        result = db_search_one(sql)
        id = result['team_id']
        sql = 'UPDATE `user_info` SET `play_status`=1 WHERE team_id=' + str(id)
        db_modify(sql)
        #create table to store fight data
        #TABLENAME team_`team_id` or team_`account`
        if int(id) != 0:#team fight
            sql = 'CREATE TABLE IF NOT EXISTS `team_' + str(id) + '`' + \
                    '(`count` int AUTO_INCREMENT PRIMARY KEY NOT NULL, \
                        `account` varchar(40) NOT NULL,  \
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
                        `drop_sk2` int NOT NULL DEFAULT \'0\' \
                        )'
            db_modify(sql)
        else:#solo
            sql = 'CREATE TABLE IF NOT EXISTS `team_' + account + '`' + \
                    '(`count` int AUTO_INCREMENT PRIMARY KEY NOT NULL, \
                        `account` varchar(40) NOT NULL,  \
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
                        `drop_sk2` int NOT NULL DEFAULT \'0\' \
                        )'
            db_modify(sql)
        return text('done')
    except Exception as e:
        print(str(e))
        return text("Explode")

@app.post("/commit_status_data")
async def commit_status_data(request):
    try:
        id = request.json['id']
        start = time.time()
        fdata = request.json #type of fdata is dict
        l_fdata = list(fdata.keys()) #transfer keys of fdata into list
        sql_col = ''
        sql_val = ''
        for i in range (0, len(l_fdata)):
            if l_fdata[i] == 'id':
                continue
            if i < (len(fdata) - 1):
                sql_col += l_fdata[i] + ','
                sql_val += '\'' + str(fdata[l_fdata[i]]) + '\'' + ','
            else:
                sql_col += l_fdata[i]
                sql_val += '\'' + str(fdata[l_fdata[i]]) + '\''
            #sql_col = account,enhance_sk1,enhance_de2,gather,sleep,drop_de2
            #sql_val = 'test02','1','1','3','3','1'
        sql = 'ALTER TABLE `team_' + str(id) + '`' + 'AUTO_INCREMENT=1'#avoid count jump
        db_modify(sql)
        sql = 'INSERT INTO `team_' + str(id) + '`' + \
                ' (' + sql_col + ') VALUES' +\
                ' (' + sql_val + ')' 
        db_modify(sql)
        end = time.time()
        cost = end - start
        print('time cost:' + str(round(cost*1000, 3)) + 'ms')
        return text('done')
    except Exception as e:
        print(str(e))
        return text("Explode")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='1234', debug=False, access_log=True)
    app.config['workers'] = '4'