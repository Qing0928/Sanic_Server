from datetime import datetime
from sanic import Sanic
from sanic.response import json, text
import pymysql.cursors
from random import randint,choices
import time
#import json as js
import threading

app = Sanic("ARGame_Server")
#lock = threading.Lock()#多執行緒鎖定

#db function
def db_fetchall(sql):
    result = ''
    try:
        db_conn = pymysql.Connect(
        host='127.0.0.1', 
        user='pmauser', 
        password='game0934', 
        db='game_sql', #db='game_sql'
        cursorclass=pymysql.cursors.DictCursor)

        with db_conn.cursor() as cur:
            cur.execute(sql)
            result = cur.fetchall()
        return result

    except Exception as e:
        return e

def db_fetchone(sql):
    result = ''
    try:
        db_conn = pymysql.Connect(
        host='127.0.0.1', 
        user='pmauser', 
        password='game0934', 
        db='game_sql', #db='game_sql'
        cursorclass=pymysql.cursors.DictCursor)

        with db_conn.cursor() as cur:
            cur.execute(sql)
            result = cur.fetchone()
        return result

    except Exception as e:
        return e

def db_modify(sql):
    result = ''
    try:
        db_conn = pymysql.Connect(
        host='127.0.0.1', 
        user='pmauser', 
        password='game0934', 
        db='game_sql', #db='game_sql'
        cursorclass=pymysql.cursors.DictCursor)

        with db_conn.cursor() as cur:
            result = cur.execute(sql)
        db_conn.commit()
        return result

    except Exception as e:
        return e 
#------------------------------------------------------------------
def fight_fetchall(sql):
    result = ''
    try:
        db_conn_fight = pymysql.Connect(
        host = '127.0.0.1', 
        user='pmauser', 
        password='game0934', 
        db='fight_sql', 
        cursorclass=pymysql.cursors.DictCursor)

        with db_conn_fight.cursor() as cur:
            cur.execute(sql)
            result = cur.fetchall()
        return result

    except Exception as e:
        return e

def fight_fatchone(sql):
    result = ''
    try:
        db_conn_fight = pymysql.Connect(
        host = '127.0.0.1', 
        user='pmauser', 
        password='game0934', 
        db='fight_sql', 
        cursorclass=pymysql.cursors.DictCursor)

        with db_conn_fight.cursor() as cur:
            cur.execute(sql)
            result = cur.fetchone()
        return result

    except Exception as e:
        return e

def fight_modify(sql):
    result = ''
    try:
        db_conn_fight = pymysql.Connect(
        host = '127.0.0.1', 
        user='pmauser', 
        password='game0934', 
        db='fight_sql', 
        cursorclass=pymysql.cursors.DictCursor)

        with db_conn_fight.cursor() as cur:
            result = cur.execute(sql)
        db_conn_fight.commit()
        return result

    except Exception as e:
        return e 
#-----------------------------------------------------------------------------------------------------
#prototype of status & action table 
status_table = 'CREATE TABLE IF NOT EXISTS `status_{id}`( \
                    `account` varchar(40) PRIMARY KEY NOT NULL, \
                    `hp` int NOT NULL DEFAULT \'0\', \
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
                    `assist_lock` int NOT NULL DEFAULT \'0\', \
                    `b_type` varchar(40) NOT NULL DEFAULT \'\' \
                )'

action_table = 'CREATE TABLE IF NOT EXISTS `action_{id}`(\
                        `account` varchar(40) PRIMARY KEY NOT NULL, \
                        `action` varchar(40) NOT NULL DEFAULT \'\', \
                        `target` varchar(40) NOT NULL DEFAULT \'\' \
                        )'
#-----------------------------------------------------------------------------------------------------
#user_skill_list
#對自己以外的目標施放技能=>`account`=target
#對自己施放技能=>`account`=account
fighter = {
    'skill_1':'UPDATE `status_{team_id}` SET `hp`=hp-{num} WHERE `account`=\'{target}\'', 
    'skill_2':'UPDATE `status_{team_id}` SET `enhance_de3`=enhance_de3+2 WHERE `account`=\'{account}\'', 
    'skill_3':'UPDATE `status_{team_id}` SET `hp`=hp-{num} WHERE `account`=\'{target}\'', 
    'skill_31':'UPDATE `status_{team_id}` SET `numb`=numb+1 WHERE `account`=\'{target}\'', 
    'skill_4':'UPDATE `status_{team_id}` SET `hp`=hp*0.8 WHERE `account`=\'{target}\'', 
    'skill_41':'UPDATE `status_{team_id}` SET `numb`=0,`sleep`=0,`poison`=0,`blood`=0,`drop_de1`=0,`drop_de2`=0,`drop_sk1`=0,`drop_sk2`=0 WHERE `account`=\'{account}\'', 
    'skill_u_2':'UPDATE `status_{team_id}` SET `hp`=hp-{num} WHERE `account`=\'{target}\'', 
    'skill_u_21':'UPDATE `status_{team_id} SET `enhance_sk4`=enhance_sk4+5 WHERE `account`=\'{account}\''
    }
         
traveler = {
    'skill_1':'UPDATE `status_{team_id}` SET `hp`=hp-{num} WHERE `account`=\'{target}\'', 
    'skill_2':'UPDATE `status_{team_id}` SET `enhance_sk1`=enhance_sk1+1 WHERE `account`=\'{target}\'', 
    'skill_3':'UPDATE `status_{team_id}` SET `gather`=gather+1 WHERE `account`=\'{account}\'', 
    'skill_31':'UPDATE `status_{team_id}` SET `numb`=numb+1 WHERE `account`=\'{target}\'', 
    'skill_4':'UPDATE `status_{team_id}` SET `hp`=hp-{num},`drop_sk2`=drop_sk2+3 WHERE `account`=\'{target}\'', 
    'skill_u_2':'UPDATE `status_{team_id}` SET `gather`=gather+2 WHERE `account`=\'{account}\'', 
    'skill_u_21':'UPDATE `status_{team_id}` SET `hp`=hp*0.7 WHERE `account`=\'{target}\''
    }

magician = {
    'skill_1':'UPDATE `status_{team_id}` SET `hp`=hp-{num} WHERE `account`=\'{target}\'', 
    'skill_2':'UPDATE `status_{team_id}` SET `enhance_de1`=enhance_de1+1 WHERE `account`=\'{m0}\' or `account`=\'{m1}\' or `account`=\'{m2}\' or `account`=\'{m3}\'', 
    'skill_3':'UPDATE `status_{team_id}` SET `hp`=hp-{num} WHERE `account`=\'{target}\'', 
    'skill_31':'UPDATE `status_{team_id}` SET `enhance_sk2`=enhance_sk2+2 WHERE `account`=\'{account}\'', 
    'skill_4':'UPDATE `status_{team_id}` SET `gather`=gather+2 WHERE `account`=\'{account}\'', 
    'skill_41':'UPDATE `status_{team_id}` SET `hp`=hp-{num} WHERE `account`=\'{target}\'', 
    'skill_u_2':'UPDATE `status_{team_id}` SET `drop_sk2`=drop_sk2+2 WHERE `account`=\'{target}\'', 
    'skill_u_21':'UPDATE `status_{team_id}` SET `enhance_sk4`=enhance_sk4+2 WHERE `account`!=\'boss\''
    }

assistant = {
    'skill_1':'UPDATE `status_{team_id}` SET `hp`=hp+{num} WHERE `account`=\'{m0}\' or `account`=\'{m1}\' or `account`=\'{m2}\' or `account`=\'{m3}\'', 
    'skill_2':'UPDATE `status_{team_id}` SET `enhance_sk2`=enhance_sk2+2,`enhance_de2`=enhance_de2+2 WHERE `account`=\'{target}\'', 
    'skill_3':'UPDATE `status_{team_id}` SET `numb`=0,`sleep`=0,`poison`=0,`blood`=0,`drop_de1`=0,`drop_de2`=0,`drop_sk1`=0,`drop_sk2`=0,`status_lock`=2 WHERE `account`=\'{m0}\' or `account`=\'{m1}\' or `account`=\'{m2}\' or `account`=\'{m3}\'', 
    'skill_31':'UPDATE `status_{team_id}` SET `hp`=hp+{num} WHERE `account`=\'{m0}\' or `account`=\'{m1}\' or `account`=\'{m2}\' or `account`=\'{m3}\'', 
    'skill_4':'UPDATE `status_{team_id}` SET `numb`=0,`sleep`=0,`poison`=0,`blood`=0,`drop_de1`=0,`drop_de2`=0,`drop_sk1`=0,`drop_sk2`=0 WHERE `account`=\'{m0}\' or `account`=\'{m1}\' or `account`=\'{m2}\' or `account`=\'{m3}\'', 
    'skill_41':'UPDATE `status_{team_id}` SET `enhance_de3`=enhance_de2+5 WHERE `account`=\'{m0}\' or `account`=\'{m1}\' or `account`=\'{m2}\' or `account`=\'{m3}\'', 
    'skill_u_1':'UPDATE `status_{team_id}` SET `gather`=gather+1 WHERE `account`=\'{account}\'',
    'skill_u_11':'UPDATE `status_{team_id}` SET `hp`=hp*0.5 WHERE `account`=\'{target}\'', 
    'skill_u_2':'UPDATE `status_{team_id}` SET `gather`=gather+3 WHERE `account`=\'{account}\'', 
    'skill_u_21':'UPDATE `status_{team_id}` SET `hp`={num} WHERE `account`=\'{target}\''
    }
#-----------------------------------------------------------------------------------------------------
#boss_skill_list
engineer = {
    'auto_attack':'UPDATE `status_{team_id}` SET `hp`=hp-{num} WHERE `account`!=\'boss\'', 
    'skill_1':'UPDATE `status_{team_id}` SET `hp`=hp-{num} WHERE `account`!=\'boss\'', 
    'skill_2':'UPDATE `status_{team_id}` SET `hp`=hp-{num} WHERE `account`!=\'boss\';', 
    'skill_21':'UPDATE `status_{team_id}` SET `poison`=poison+3 WHERE `account`!=\'boss\'', 
    'skil_3':'UPDATE `status_{team_id}` SET `hp`=hp-{num} WHERE `account`!=\'boss\'', 
    'skill_31':'UPDATE `status_{team_id}` SET `sleep`=sleep+1 WHERE `account`!=\'boss\'', 
    'skill_4':'UPDATE `status_{team_id}` SET `hp`=hp-{num} WHERE `account`!=\'boss\''
    }

business = {
    'auto_attack':'UPDATE `status_{team_id}` SET `hp`=hp-{num} WHERE `account`!=\'boss\'', 
    'skill_1':'UPDATE `status_{team_id}` SET `hp`=hp-{num} WHERE `account`!=\'boss\'', 
    'skill_11':'UPDATE `status_{team_id}` SET `gather`=\'0\' WHERE `account`=\'{target}\'', 
    'skill_2':'UPDATE `status_{team_id}` SET `hp`=hp-{num} WHERE `account`!=\'boss\'', 
    'skill_21':'UPDATE `status_{team_id}` SET `drop_sk1`=drop_sk1+3 WHERE `account`!=\'boss\'', 
    'skill_3':'UPDATE `status_{team_id}` SET `hp`=hp-{num},`drop_sk2`=drop_sk2+2 WHERE `account`=\'{target}\'', 
    'skill_4':'UPDATE `status_{team_id}` SET `hp`=hp-{num} WHERE `account`!=\'boss\'', 
    'skill_41':'UPDATE `status_{team_id}` SET `drop_de2`=drop_de2+2,`numb`=numb+2 WHERE `account`!=\'boss\''
    }
#-----------------------------------------------------------------------------------------------------
#compute_user_action(已整合->暫時停用)
def compute_user_action(team_id):
    try:
        #取得玩家動作
        sql = 'SELECT * FROM `action_{team_id}`'
        result = fight_fetchall(sql.format(team_id=team_id))
        #先檢查有沒有動作沒進來
        chk = 0
        for i in range(0, len(result)):
            if result[i]['action'] == '':
                chk += 1
        #逐個計算
        for i in range (0, len(result)):
            tmp = result[i]
            if (chk != 0):#動作還沒進來就跳掉
                break
            elif (tmp['account'] == 'boss'):
                continue
            else:
                #技能倍率
                if tmp['action'] != 'item_1' or 'item_2' or 'item_3' or 'item_4' or 'item_5' or 'item_6' or 'item_7':
                    sql = 'SELECT `drop_sk1`,`drop_sk2`, `enhance_sk1`, `enhance_sk2`, `enhance_sk3`, `enhance_sk4` FROM `status_{team_id}` WHERE account=\'{account}\''
                    damage_status = fight_fatchone(sql.format(team_id=team_id, account=tmp['account']))
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
                    #計算戰鬥資料
                    sql = 'SELECT `career` FROM `user_skill` WHERE account=\'{account}\''
                    career_result = db_fetchone(sql.format(account=tmp['account']))
                    #fighter
                    if career_result['career'] == 'fighter':
                        #fate = 0 機率效果不會發動，fate = 1 機率效果發動
                        if (tmp['fate'] == 0) and (tmp['action'] != 'skill_4'):
                            sql = fighter[tmp['action']].format(team_id=team_id, target=tmp['target'], num=50*num)
                            fight_modify(sql)
                            sql = 'UPDATE `action_{team_id}` SET `action`=\'\',`target`=\'\' WHERE `account`=\'{account}\''
                            fight_modify(sql.format(team_id=team_id, account=tmp['account']))

                        elif (tmp['fate'] == 1) and ((tmp['action'] == 'skill_3') or (tmp['action'] == 'skill_4')):
                            if tmp['action'] == 'skill_3':
                                sql = fighter['skill_3'].format(team_id=team_id, target=tmp['target'], num=100*num)
                                fight_modify(sql)
                                sql = fighter['skill_31'].format(team_id=team_id, target=tmp['target'])
                                fight_modify(sql)
                                sql = 'UPDATE `action_{team_id}` SET `action`=\'\',`target`=\'\' WHERE `account`=\'{account}\''
                                fight_modify(sql.format(team_id=team_id, account=tmp['account']))

                            elif tmp['action'] == 'skill_4':
                                sql = fighter['skill_4'].format(team_id=team_id, target=tmp['target'])
                                fight_modify(sql)
                                sql = fighter['skill_41'].format(team_id=team_id, target=tmp['account'])
                                fight_modify(sql)
                                sql = 'UPDATE `action_{team_id}` SET `action`=\'\',`target`=\'\' WHERE `account`=\'{account}\''
                                fight_modify(sql.format(team_id=team_id, account=tmp['account']))
                    #traveler
                    elif career_result['career'] == 'traveler':
                        if (tmp['fate'] == 0) and (tmp['action'] == 'skill_1'):
                            sql = traveler[tmp['action']].format(team_id=team_id, target=tmp['target'], num=60*num)
                            fight_modify(sql)
                            sql = 'UPDATE `action_{team_id}` SET `action`=\'\',`target`=\'\' WHERE `account`=\'{account}\''
                            fight_modify(sql.format(team_id=team_id, account=tmp['account']))

                        elif (tmp['fate'] == 0) and (tmp['action'] == 'skill_2'):
                            sql = traveler[tmp['action']].format(team_id=team_id, target=tmp['target'])
                            fight_modify(sql)
                            sql = 'UPDATE `action_{team_id}` SET `action`=\'\',`target`=\'\' WHERE `account`=\'{account}\''
                            fight_modify(sql.format(team_id=team_id, account=tmp['account']))

                        elif (tmp['fate'] == 0) and (tmp['action'] == 'skill_3'):
                            sql = traveler[tmp['action']].format(team_id=team_id, account=tmp['account'])
                            fight_modify(sql)
                            sql = 'UPDATE `action_{team_id}` SET `action`=\'\',`target`=\'\' WHERE `account`=\'{account}\''
                            fight_modify(sql.format(team_id=team_id, account=tmp['account']))
                            
                        elif (tmp['fate'] == 0) and (tmp['action'] == 'skill_31'):
                            sql = traveler[tmp['action']].format(team_id=team_id, target=tmp['target'])
                            fight_modify(sql)
                            sql = 'UPDATE `action_{team_id}` SET `action`=\'\',`target`=\'\' WHERE `account`=\'{account}\''
                            fight_modify(sql.format(team_id=team_id, account=tmp['account']))

                        elif (tmp['fate'] == 0) and (tmp['action'] == 'skill_4'):
                            sql = traveler[tmp['action']].format(team_id=team_id, target=tmp['target'], num=200*num)
                            fight_modify(sql)
                            sql = 'UPDATE `action_{team_id}` SET `action`=\'\',`target`=\'\' WHERE `account`=\'{account}\''
                            fight_modify(sql.format(team_id=team_id, account=tmp['account']))
                    #magician
                    elif career_result['career'] == 'magician':
                        if (tmp['fate'] == 0) and (tmp['action'] == 'skill_1'):
                            sql = magician[tmp['action']].format(team_id=team_id, target=tmp['target'], num=60*num)
                            fight_modify(sql)
                            sql = 'UPDATE `action_{team_id}` SET `action`=\'\',`target`=\'\' WHERE `account`=\'{account}\''
                            fight_modify(sql.format(team_id=team_id, account=tmp['account']))

                        if (tmp['fate'] == 0) and (tmp['action'] == 'skill_2'):
                            sql = magician[tmp['action']].format(team_id=team_id, m0=result[0]['account'], m1=result[1]['account'], m2=result[2]['account'], m3=result[3]['account'])
                            fight_modify(sql)
                            sql = 'UPDATE `action_{team_id}` SET `action`=\'\',`target`=\'\' WHERE `account`=\'{account}\''
                            fight_modify(sql.format(team_id=team_id, account=tmp['account']))

                        if (tmp['fate'] == 0) and (tmp['action'] == 'skill_3'):
                            sql = magician[tmp['action']].format(team_id=team_id, target=tmp['target'], num=100*num)
                            fight_modify(sql)
                            sql = magician['skill_31'].format(team_id=team_id, account=tmp['account'])
                            fight_modify(sql)
                            sql = 'UPDATE `action_{team_id}` SET `action`=\'\',`target`=\'\' WHERE `account`=\'{account}\''
                            fight_modify(sql.format(team_id=team_id, account=tmp['account']))

                        if (tmp['fate'] == 0) and (tmp['action'] == 'skill_4'):
                            sql = magician[tmp['action']].format(team_id=team_id, account=tmp['account'])
                            fight_modify(sql)
                            sql = 'UPDATE `action_{team_id}` SET `action`=\'\',`target`=\'\' WHERE `account`=\'{account}\''
                            fight_modify(sql.format(team_id=team_id, account=tmp['account']))
                            
                        if (tmp['fate'] == 0) and (tmp['action'] == 'skill_41'):
                            sql = magician[tmp['action']].format(team_id=team_id, target=tmp['target'], num=500*num)
                            fight_modify(sql)
                            sql = 'UPDATE `action_{team_id}` SET `action`=\'\',`target`=\'\' WHERE `account`=\'{account}\''
                            fight_modify(sql.format(team_id=team_id, account=tmp['account']))
                    #assistant
                    elif career_result['career'] == 'assistant':
                        #持續恢復技能檢查
                        sql = 'SELECT `assist_lock`,`account` FROM `status_{team_id}`'
                        assist_lock = fight_fetchall(sql.format(team_id=team_id))
                        for i in range(0, len(assist_lock)):
                            if assist_lock[i]['assist_lock'] <= 0:
                                continue
                            if assist_lock[i]['account'] == 'boss':
                                continue
                            if assist_lock[i]['assist_lock'] > 0:
                                sql = 'UPDATE `status_{team_id}` SET `hp`=hp+{num} WHERE `account`=\'{account}\''
                                fight_modify(sql.format(team_id=team_id, num=200*num, account=assist_lock[i]['account']))
                        #主要技能
                        if (tmp['fate'] == 0) and (tmp['action'] == 'skill_1'):
                            sql = assistant[tmp['action']].format(team_id=team_id, num=150*num, m0=result[0]['account'], m1=result[1]['account'], m2=result[2]['account'], m3=result[3]['account'])
                            fight_modify(sql)
                            sql = 'UPDATE `action_{team_id}` SET `action`=\'\',`target`=\'\' WHERE `account`=\'{account}\''
                            fight_modify(sql.format(team_id=team_id, account=tmp['account']))

                        if (tmp['fate'] == 0) and (tmp['action'] == 'skill_2'):
                            sql = assistant[tmp['action']].format(team_id=team_id, target=tmp['target'])
                            fight_modify(sql)
                            sql = 'UPDATE `action_{team_id}` SET `action`=\'\',`target`=\'\' WHERE `account`=\'{account}\''
                            fight_modify(sql.format(team_id=team_id, account=tmp['account']))

                        if (tmp['fate'] == 0) and (tmp['action'] == 'skill_3'):
                            sql = assistant[tmp['action']].format(team_id=team_id, m0=result[0]['account'], m1=result[1]['account'], m2=result[2]['account'], m3=result[3]['account'])
                            fight_modify(sql)
                            sql = assistant['skill_31'].format(team_id=team_id, num=200*num, m0=result[0]['account'], m1=result[1]['account'], m2=result[2]['account'], m3=result[3]['account'])
                            fight_modify(sql)
                            sql = 'UPDATE `action_{team_id}` SET `action`=\'\',`target`=\'\' WHERE `account`=\'{account}\''
                            fight_modify(sql.format(team_id=team_id, account=tmp['account']))

                        if (tmp['fate'] == 0) and (tmp['action'] == 'skill_4'):
                            sql = assistant[tmp['action']].format(team_id=team_id, m0=result[0]['account'], m1=result[1]['account'], m2=result[2]['account'], m3=result[3]['account'])
                            fight_modify(sql)
                            sql = assistant[tmp['action']].format(team_id=team_id, m0=result[0]['account'], m1=result[1]['account'], m2=result[2]['account'], m3=result[3]['account'])
                            fight_modify(sql)
                            sql = 'UPDATE `action_{team_id}` SET `action`=\'\',`target`=\'\' WHERE `account`=\'{account}\''
                            fight_modify(sql.format(team_id=team_id, account=tmp['account']))
                else:
                    print('still have long way')
        
        #重製`action_{team_id}`的資料

    except Exception as e:
        print(e)
#-----------------------------------------------------------------------------------------------------
#produce_boss_action
def produce_boss_action(team_id):
    try:
        #取得boss相關資訊
        sql = 'SELECT `hp`,`b_type` FROM `status_{team_id}` WHERE `account`=\'boss\''
        result = fight_fatchone(sql.format(team_id=team_id))
        b_hp = result['hp']
        b_type = result['b_type']
        
        if (b_type == 'engineer'):
            remain_hp = b_hp / 1000

            if ((remain_hp >= 0.75) and (remain_hp <= 1)):
                action_list = ['auto_attack', 'skill_1']
                action = choices(action_list, weights=[6, 4])
                sql = 'UPDATE `action_{team_id}` SET `action`=\'{action}\' WHERE `account`=\'boss\''
                result = fight_modify(sql.format(team_id=team_id, action=action[0]))

            elif ((remain_hp >= 0.5) and (remain_hp <= 0.74)):
                action_list = ['skill_1', 'skill_2']
                action = choices(action_list, weights=[4, 6])
                sql = 'UPDATE `action_{team_id}` SET `action`=\'{action}\' WHERE `account`=\'boss\''
                result = fight_modify(sql.format(team_id=team_id, action=action[0]))

            elif ((remain_hp >= 0.3) and (remain_hp <= 0.49)):
                action_list = ['skill_2', 'skill_3']
                action = choices(action_list, weights=[2, 8])
                sql = 'UPDATE `action_{team_id}` SET `action`=\'{action}\' WHERE `account`=\'boss\''
                result = fight_modify(sql.format(team_id=team_id, action=action[0]))
            
            elif ((remain_hp >= 0) and (remain_hp <= 0.29)):
                action_list = ['skill_3', 'skill_4']
                action = choices(action_list, weights=[1, 9])
                sql = 'UPDATE `action_{team_id}` SET `action`=\'{action}\' WHERE `account`=\'boss\''
                result = fight_modify(sql.format(team_id=team_id, action=action[0]))

        elif (b_type == 'business'):
            remain_hp = b_hp/1000

            sql = 'SELECT `account` FROM `status_{team_id}` WHERE `gather`!=\'0\' and `account`!=\'boss\''
            result = fight_fetchall(sql.format(team_id=team_id))
            #如果有人發動蓄能技
            if len(list(result)) != 0:
                debuff_list = ['enable', 'disable']
                debuff = choices(debuff_list, weights=[4, 6])
                #發動skill_1
                if debuff[0] == 'enable':
                    sql = 'UPDATE `action_{team_id}` SET `action`=\'skill_1\',`target`=\'{target}\' WHERE `account`=\'boss\''
                    fight_modify(sql.format(team_id=team_id, target=result[0]['account']))

                #沒發動，按照規劃的方式動作
                elif debuff[0] == 'disable':
                    if ((remain_hp <=1) and (remain_hp >= 0.6)):
                        action_list = ['auto_attack', 'skill_2']
                        action = choices(action_list, weights=[6, 4])
                        sql = 'UPDATE `action_{team_id}` SET `action`=\'{action}\' WHERE `account`=\'boss\''
                        result = fight_modify(sql.format(team_id=team_id, action=action[0]))

                    elif ((remain_hp <= 0.59) and (remain_hp >= 0.3)):
                        action_list = ['skill_2', 'skill_3']
                        action = choices(action_list, weights=[3, 7])
                        sql = 'UPDATE `action_{team_id}` SET `action`=\'{action}\' WHERE `account`=\'boss\''
                        result = fight_modify(sql.format(team_id=team_id, action=action[0]))
                
                    elif ((remain_hp <= 0.29) and (remain_hp >= 0)):
                        action_list = ['skill_3', 'skill_4']
                        action = choices(action_list, weights=[2, 8])
                        sql = 'UPDATE `action_{team_id}` SET `action`=\'{action}\' WHERE `account`=\'boss\''
                        result = fight_modify(sql.format(team_id=team_id, action=action[0]))

            #沒有人發動蓄能技
            elif len(list(result)) == 0:
                if ((remain_hp <=1) and (remain_hp >= 0.6)):
                    action_list = ['auto_attack', 'skill_2']
                    action = choices(action_list, weights=[6, 4])
                    sql = 'UPDATE `action_{team_id}` SET `action`=\'{action}\' WHERE `account`=\'boss\''
                    result = fight_modify(sql.format(team_id=team_id, action=action[0]))

                if ((remain_hp <= 0.59) and (remain_hp >= 0.3)):
                    action_list = ['skill_2', 'skill_3']
                    action = choices(action_list, weights=[3, 7])
                    sql = 'UPDATE `action_{team_id}` SET `action`=\'{action}\' WHERE `account`=\'boss\''
                    result = fight_modify(sql.format(team_id=team_id, action=action[0]))
                
                if ((remain_hp <= 0.29) and (remain_hp >= 0)):
                    action_list = ['skill_3', 'skill_4']
                    action = choices(action_list, weights=[2, 8])
                    sql = 'UPDATE `action_{team_id}` SET `action`=\'{action}\' WHERE `account`=\'boss\''
                    result = fight_modify(sql.format(team_id=team_id, action=action[0]))

        elif (b_type == 'humanities'):
            remain_hp = b_hp / 1200

            if ((remain_hp <= 1) and (remain_hp >= 0.6)):
                action_list = ['auto_attack', 'skill_2']
                action = choices(action_list, weights=[6, 4])
                sql = 'UPDATE `action_{team_id}` SET `action`=\'{action}\' WHERE `account`=\'boss\''
                result = fight_modify(sql.format(team_id=team_id, action=action[0]))

            elif ((remain_hp <= 0.59) and (remain_hp >= 0.3)):
                action_list = ['skill_2', 'skill_3']
                action = choices(action_list, weights=[3, 7])
                sql = 'UPDATE `action_{team_id}` SET `action`=\'{action}\' WHERE `account`=\'boss\''
                result = fight_modify(sql.format(team_id=team_id, action=action[0]))

            elif ((remain_hp <= 0.29) and (remain_hp >= 0)):
                sql = 'UPDATE `action_{team_id}` SET `action`=\'{action}\' WHERE `account`=\'boss\''
                result = fight_modify(sql.format(team_id=team_id, action='skill_4'))

        elif (b_type == 'design'):
            remain_hp = b_hp / 2000
            sql = 'SELECT `action` FROM `action_{team_id}` WHERE `account`=\'boss\''
            result = fight_fatchone(sql.format(team_id=team_id))

            sql = 'SELECT `immortal` FROM `status_{team_id}` WHERE `account`=\'boss\''
            immortal_result = fight_fatchone(sql.format(team_id=team_id))
            if (remain_hp <= 0.2) and (immortal_result['immortal'] == 0):
                sql = 'UPDATE `action_{team_id}` SET `action`=\'skill_4\' WHERE `account`=\'boss\''
                action = 'skill_4'
                fight_modify(sql.format(team_id=team_id))

            else:
                if (result['action'] == 'skill_1') and (remain_hp > 0.2):
                    sql = 'UPDATE `action_{team_id}` SET `action`=\'skill_2\' WHERE `account`=\'boss\''
                    action = 'skill_2'
                    fight_modify(sql.format(team_id=team_id))
                    

                if (result['action'] == 'skill_2') and (remain_hp > 0.2):
                    sql = 'UPDATE `action_{team_id}` SET `action`=\'skill_3\' WHERE `account`=\'boss\''
                    action = 'skill_3'
                    fight_modify(sql.format(team_id=team_id))
                    
                if (result['action'] == 'skill_3') and (remain_hp > 0.2):
                    sql = 'UPDATE `action_{team_id}` SET `action`=\'skill_1\' WHERE `account`=\'boss\''
                    action = 'skill_1'
                    fight_modify(sql.format(team_id=team_id))
                    
        elif (b_type == 'future'):
            remain_hp = b_hp /2000

            if (remain_hp <= 1) and (remain_hp >= 0.2):
                action_list = ['skill_1', 'skill_2', 'skill_3']
                action = choices(action_list, weights=[3, 3, 3])
                sql = 'UPDATE `action_{team_id}` SET `action`=\'{action}\' WHERE `account`=\'boss\''
                result = fight_modify(sql.format(team_id=team_id, action=action[0]))
            
            else:
                sql = 'UPDATE `action_{team_id}` SET `action`=\'skill_4\' WHERE `account`=\'boss\''
                action = 'skill_4'
                fight_modify(sql.format(team_id=team_id))

        print('b_type:' + str(b_type))
        print('remain_hp:' + str(remain_hp))
        print(str(action))
        
    except Exception as e:
        print(e)
#-----------------------------------------------------------------------------------------------------
#compute_boss_action(已整合->暫時停用)
def compute_boss_action(team_id):
    try:
        #計算倍率
        sql = 'SELECT `drop_sk1`,`drop_sk2`, `enhance_sk1`, `enhance_sk2`, `enhance_sk3`, `enhance_sk4` \
            FROM `status_{team_id}` WHERE `account`=\'boss\''
        damage_status = fight_fatchone(sql.format(team_id=team_id))
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
        
        #取得boss的類別和動作
        sql = 'SELECT `b_type` FROM `status_{team_id}` WHERE `account`=\'boss\''
        b_type = fight_fatchone(sql.format(team_id=team_id))
        sql = 'SELECT `action` FROM `action_{team_id}` WHERE `account`=\'boss\''
        result = fight_fatchone(sql.format(team_id=team_id))
        #依照類別處理技能效果
        if b_type['b_type'] == 'engineer':
            if result['action'] == 'auto_attack':
                sql = engineer['auto_attack'].format(team_id=team_id, num=100*num)
                fight_modify(sql)
            
            if result['action'] == 'skill_1':
                sql = engineer['skill_1'].format(team_id=team_id, num=120*num)
                fight_modify(sql)

            if result['action'] == 'skill_2':
                sql = engineer['skill_2'].format(team_id=team_id, num=105*num)
                fight_modify(sql)

                #中毒效果是否發動
                debuff_list = ['enable', 'disable']
                debuff = choices(debuff_list, weights=[2, 8])
                print(debuff[0])
                #發動
                if debuff[0] == 'enable':
                    sql = engineer['skill_21'].format(team_id=team_id)
                    fight_modify(sql)
                else:
                    pass

            if result['action'] == 'skill_3':
                sql = engineer['skil_3'].format(team_id=team_id, num=175*num)
                fight_modify(sql)
                
                #睡眠效果是否發動
                debuff_list = ['enable', 'disable']
                debuff = choices(debuff_list, weights=[4, 6])
                print(debuff[0])
                #發動
                if debuff[0] == 'enable':
                    sql = engineer['skill_31'].format(team_id=team_id)
                    fight_modify(sql)
                else:
                    pass

            if result['action'] == 'skill_4':
                sql = engineer['skill_4'].format(team_id=team_id, num=455*num)
                fight_modify(sql)
        
    except Exception as e:
        print(e)
#-----------------------------------------------------------------------------------------------------
#compute_action
def compute_action(team_id):
    try:
        #取得玩家動作
        sql = 'SELECT * FROM `action_{team_id}` WHERE `account`!=\'boss\''
        result = fight_fetchall(sql.format(team_id=team_id))

        #先檢查有沒有動作沒進來
        chk = 0
        for i in range(0, len(result)):
            if result[i]['action'] == '':
                chk += 1
            if chk > 0:
                break

        #補師持續恢復技能檢查，動作都進來時優先發動
        if chk == 0:
            sql = 'SELECT `assist_lock`,`account` FROM `status_{team_id}` WHERE `account`!=\'boss\''
            assist_lock = fight_fetchall(sql.format(team_id=team_id))
            for i in range(0, len(assist_lock)):
                if assist_lock[i]['assist_lock'] <= 0:
                    continue
                
                if assist_lock[i]['assist_lock'] > 0:
                    sql = 'UPDATE `status_{team_id}` SET `hp`=hp+{num} WHERE `account`=\'{account}\''
                    fight_modify(sql.format(team_id=team_id, num=200, account=assist_lock[i]['account']))
        else:
            pass

        #逐個計算
        for i in range (0, len(result)):
            tmp = result[i]
            #沒進來就跳掉
            if (chk != 0):
                print('還不用處理')
                break

            #開始處理動作
            else:
                #計算技能倍率
                sql = 'SELECT `drop_sk1`,`drop_sk2`, `enhance_sk1`, `enhance_sk2`, `enhance_sk3`, `enhance_sk4` FROM `status_{team_id}` WHERE account=\'{account}\''
                enhance_status = fight_fatchone(sql.format(team_id=team_id, account=tmp['account']))
                skill_times = 1
                if enhance_status['drop_sk1'] > 0:
                    skill_times *= 0.85
                if enhance_status['drop_sk2'] > 0:
                    skill_times *= 0.7
                if enhance_status['enhance_sk1'] > 0:
                    skill_times *= 1.15
                if enhance_status['enhance_sk2'] > 0:
                    skill_times *= 1.2
                if enhance_status['enhance_sk3'] > 0:
                    skill_times *= 1.5
                if enhance_status['enhance_sk4'] > 0:
                    skill_times *= 2.5
                else:
                    skill_times *= 1

                sql = 'SELECT `drop_de1`,`drop_de2`,`sleep` FROM `status_{team_id}` WHERE `account`=\'boss\''
                b_weaken_status = fight_fatchone(sql.format(team_id=team_id))
                if b_weaken_status['drop_de1'] > 0:
                    skill_times *= 1.15
                if b_weaken_status['drop_de2'] > 0:
                    skill_times *= 1.25
                if b_weaken_status['sleep'] > 0:
                    skill_times *= 1.5


                #是否可以行動
                if (tmp['action'] == 'numb') or (tmp['action'] == 'gather') or (tmp['action'] == 'sleep'):
                    print(str(tmp['account']) + ':' + '無法行動 why:' + str(tmp['action']))
                    sql = 'UPDATE `action_{team_id}` SET `action`=\'\',`target`=\'\',`fate`=\'0\' WHERE `account`=\'{account}\''
                    fight_modify(sql.format(team_id=team_id, account=tmp['account']))    
                
                if (tmp['action'] == 'dead'):
                    print(str(tmp['account']) + ':' + '無法行動 why:' + str(tmp['action']))
                    continue
                    
                #可以行動
                else:
                    #技能發動
                    if (tmp['action'] != 'item_1') and (tmp['action'] != 'item_2') and (tmp['action'] != 'item_3') and (tmp['action'] != 'item_4') and (tmp['action'] != 'item_5'):
                        #取得職業類型
                        sql = 'SELECT `career` FROM `user_skill` WHERE account=\'{account}\''
                        career_result = db_fetchone(sql.format(account=tmp['account']))

                        #fighter
                        if career_result['career'] == 'fighter':
                            try:
                                #檢測常駐型Ultra_Skill
                                sql = 'SELECT `skill_u_1` FROM `user_skill` WHERE `account`=\'{account}\''
                                u_chk = db_fetchone(sql.format(account=tmp['account']))
                                if u_chk['skill_u_1'] != 0:
                                    skill_times *= 2.5
                                else:
                                    skill_times *= 1

                                if tmp['action'] == 'skill_1':
                                    sql = fighter['skill_1'].format(team_id=team_id, target=tmp['target'], num=50*skill_times)
                                    fight_modify(sql)
                                    sql = 'UPDATE `action_{team_id}` SET `action`=\'\',`target`=\'\' WHERE `account`=\'{account}\''
                                    fight_modify(sql.format(team_id=team_id, account=tmp['account']))

                                elif tmp['action'] == 'skill_2':
                                    sql = fighter['skill_2'].format(team_id=team_id, account=tmp['account'])
                                    fight_modify(sql)
                                    sql = 'UPDATE `action_{team_id}` SET `action`=\'\',`target`=\'\' WHERE `account`=\'{account}\''
                                    fight_modify(sql.format(team_id=team_id, account=tmp['account']))

                                elif tmp['action'] == 'skill_3':
                                    debuff_list = ['enable', 'disable']
                                    debuff = choices(debuff_list, weights=[1, 9])
                                    if debuff[0] == 'enable':
                                        sql = fighter['skill_3'].format(team_id=team_id, num=100*skill_times, target=tmp['target'])
                                        fight_modify(sql)
                                        sql = fighter['skill_31'].format(team_id=team_id, target=tmp['target'])
                                        fight_modify(sql)
                                        sql = 'UPDATE `action_{team_id}` SET `action`=\'\',`target`=\'\' WHERE `account`=\'{account}\''
                                        fight_modify(sql.format(team_id=team_id, account=tmp['account']))

                                    if debuff[0] == 'disable':
                                        sql = fighter['skill_3'].format(team_id=team_id, num=100*skill_times, target=tmp['target'])
                                        fight_modify(sql)
                                        sql = 'UPDATE `action_{team_id}` SET `action`=\'\',`target`=\'\' WHERE `account`=\'{account}\''
                                        fight_modify(sql.format(team_id=team_id, account=tmp['account']))
                                
                                elif tmp['action'] == 'skill_4':
                                    sql = fighter['skill_4'].format(team_id=team_id, target=tmp['target'])
                                    fight_modify(sql)
                                    sql = fighter['skill_41'].format(team_id=team_id, account=tmp['account'])
                                    fight_modify(sql)
                                    sql = 'UPDATE `action_{team_id}` SET `action`=\'\',`target`=\'\' WHERE `account`=\'{account}\''
                                    fight_modify(sql.format(team_id=team_id, account=tmp['account']))

                                elif tmp['action'] == 'skill_u_2':
                                    sql = fighter['skill_u_2'].format(team_id=team_id, target=tmp['target'], num=300*skill_times)
                                    fight_modify(sql)
                                    sql = fighter['skill_u_21'].format(team_id=team_id, account=tmp['account'])
                                    fight_modify(sql)
                                    sql = 'UPDATE `action_{team_id}` SET `action`=\'\',`target`=\'\' WHERE `account`=\'{account}\''
                                    fight_modify(sql.format(team_id=team_id, account=tmp['account']))

                            except Exception as e:
                                print(e)
                                print('fighter' + str(tmp['action']) + 'error')

                        #traveler
                        elif career_result['career'] == 'traveler':
                            try:
                                sql = 'SELECT `skill_u_1` FROM `user_skill` WHERE `account`=\'{account}\''
                                u_chk = db_fetchone(sql.format(account=tmp['account']))
                                if u_chk['skill_u_1'] != 0:
                                    sql = 'UPDATE `status_{team_id}` SET `enhance_sk2`=enhance_sk2+3 WHERE `account`!=\'boss\''
                                    fight_modify(sql.format(team_id=team_id))
                                else:
                                    pass

                                if tmp['action'] == 'skill_1':
                                    sql = traveler[tmp['action']].format(team_id=team_id, target=tmp['target'], num=60*skill_times)
                                    fight_modify(sql)
                                    sql = 'UPDATE `action_{team_id}` SET `action`=\'\',`target`=\'\' WHERE `account`=\'{account}\''
                                    fight_modify(sql.format(team_id=team_id, account=tmp['account']))

                                elif tmp['action'] == 'skill_2':
                                    sql = traveler[tmp['action']].format(team_id=team_id, target=tmp['target'])
                                    fight_modify(sql)
                                    sql = 'UPDATE `action_{team_id}` SET `action`=\'\',`target`=\'\' WHERE `account`=\'{account}\''
                                    fight_modify(sql.format(team_id=team_id, account=tmp['account']))

                                elif tmp['action'] == 'skill_3':
                                    sql = traveler[tmp['action']].format(team_id=team_id, account=tmp['account'])
                                    fight_modify(sql)
                                    sql = 'UPDATE `action_{team_id}` SET `action`=\'\',`target`=\'\' WHERE `account`=\'{account}\''
                                    fight_modify(sql.format(team_id=team_id, account=tmp['account']))
                                    
                                elif tmp['action'] == 'skill_31':
                                    sql = traveler[tmp['action']].format(team_id=team_id, target=tmp['target'])
                                    fight_modify(sql)
                                    sql = 'UPDATE `action_{team_id}` SET `action`=\'\',`target`=\'\' WHERE `account`=\'{account}\''
                                    fight_modify(sql.format(team_id=team_id, account=tmp['account']))

                                elif tmp['action'] == 'skill_4':
                                    sql = traveler[tmp['action']].format(team_id=team_id, target=tmp['target'], num=200*skill_times)
                                    fight_modify(sql)
                                    sql = 'UPDATE `action_{team_id}` SET `action`=\'\',`target`=\'\' WHERE `account`=\'{account}\''
                                    fight_modify(sql.format(team_id=team_id, account=tmp['account']))

                                elif tmp['action'] == 'skill_u_2':
                                    sql = traveler['skill_u_2'].format(team_id=team_id, account=tmp['account'])
                                    fight_modify(sql)
                                    sql = 'UPDATE `action_{team_id}` SET `action`=\'\',`target`=\'\' WHERE `account`=\'{account}\''
                                    fight_modify(sql.format(team_id=team_id, account=tmp['account']))
                                
                                elif tmp['action'] == 'skill_u_21':
                                    sql = traveler['skill_u_21'].format(team_id=team_id, target=tmp['target'])
                                    fight_modify(sql)
                                    sql = 'UPDATE `action_{team_id}` SET `action`=\'\',`target`=\'\' WHERE `account`=\'{account}\''
                                    fight_modify(sql.format(team_id=team_id, account=tmp['account']))

                            except Exception as e:
                                print(e)
                                print('traveler' + str(tmp['action']) + 'error')

                        #magician
                        elif career_result['career'] == 'magician':
                            try:
                                #檢測常駐型Ultra_Skill
                                sql = 'SELECT `skill_u_1` FROM `user_skill` WHERE `account`=\'{account}\''
                                u_chk = db_fetchone(sql.format(account=tmp['account']))
                                if u_chk['skill_u_1'] != 0:
                                    skill_times *= 2.5
                                else:
                                    skill_times *= 1

                                if tmp['action'] == 'skill_1':
                                    sql = magician[tmp['action']].format(team_id=team_id, target=tmp['target'], num=60*skill_times)
                                    fight_modify(sql)
                                    sql = 'UPDATE `action_{team_id}` SET `action`=\'\',`target`=\'\' WHERE `account`=\'{account}\''
                                    fight_modify(sql.format(team_id=team_id, account=tmp['account']))

                                elif tmp['action'] == 'skill_2':
                                    sql = magician[tmp['action']].format(team_id=team_id, m0=result[0]['account'], m1=result[1]['account'], m2=result[2]['account'], m3=result[3]['account'])
                                    fight_modify(sql)
                                    sql = 'UPDATE `action_{team_id}` SET `action`=\'\',`target`=\'\' WHERE `account`=\'{account}\''
                                    fight_modify(sql.format(team_id=team_id, account=tmp['account']))

                                elif tmp['action'] == 'skill_3':
                                    sql = magician[tmp['action']].format(team_id=team_id, target=tmp['target'], num=100*skill_times)
                                    fight_modify(sql)
                                    sql = magician['skill_31'].format(team_id=team_id, account=tmp['account'])
                                    fight_modify(sql)
                                    sql = 'UPDATE `action_{team_id}` SET `action`=\'\',`target`=\'\' WHERE `account`=\'{account}\''
                                    fight_modify(sql.format(team_id=team_id, account=tmp['account']))

                                elif tmp['action'] == 'skill_4':
                                    sql = magician[tmp['action']].format(team_id=team_id, account=tmp['account'])
                                    fight_modify(sql)
                                    sql = 'UPDATE `action_{team_id}` SET `action`=\'\',`target`=\'\' WHERE `account`=\'{account}\''
                                    fight_modify(sql.format(team_id=team_id, account=tmp['account']))
                                    
                                elif tmp['action'] == 'skill_41':
                                    sql = magician[tmp['action']].format(team_id=team_id, target=tmp['target'], num=500*skill_times)
                                    fight_modify(sql)
                                    sql = 'UPDATE `action_{team_id}` SET `action`=\'\',`target`=\'\' WHERE `account`=\'{account}\''
                                    fight_modify(sql.format(team_id=team_id, account=tmp['account']))

                                elif tmp['action'] == 'skill_u_2':
                                    sql = magician['skill_u_2'].format(team_id=team_id, target=tmp['target'])
                                    fight_modify(sql)
                                    sql = magician['skill_u_21'].format(team_id=team_id)
                                    fight_modify(sql)
                                    sql = 'UPDATE `action_{team_id}` SET `action`=\'\',`target`=\'\' WHERE `account`=\'{account}\''
                                    fight_modify(sql.format(team_id=team_id, account=tmp['account']))
                            
                            except Exception as e:
                                print(e)
                                print('magician' + str(tmp['action']) + 'error')

                        #assistant
                        elif career_result['career'] == 'assistant':
                            try:
                                if tmp['action'] == 'skill_1':
                                    sql = assistant[tmp['action']].format(team_id=team_id, num=150, m0=result[0]['account'], m1=result[1]['account'], m2=result[2]['account'], m3=result[3]['account'])
                                    fight_modify(sql)
                                    sql = 'UPDATE `action_{team_id}` SET `action`=\'\',`target`=\'\' WHERE `account`=\'{account}\''
                                    fight_modify(sql.format(team_id=team_id, account=tmp['account']))

                                elif tmp['action'] == 'skill_2':
                                    sql = assistant[tmp['action']].format(team_id=team_id, target=tmp['target'])
                                    fight_modify(sql)
                                    sql = 'UPDATE `action_{team_id}` SET `action`=\'\',`target`=\'\' WHERE `account`=\'{account}\''
                                    fight_modify(sql.format(team_id=team_id, account=tmp['account']))

                                elif tmp['action'] == 'skill_3':
                                    sql = assistant[tmp['action']].format(team_id=team_id, m0=result[0]['account'], m1=result[1]['account'], m2=result[2]['account'], m3=result[3]['account'])
                                    fight_modify(sql)
                                    sql = assistant['skill_31'].format(team_id=team_id, num=200*skill_times, m0=result[0]['account'], m1=result[1]['account'], m2=result[2]['account'], m3=result[3]['account'])
                                    fight_modify(sql)
                                    sql = 'UPDATE `action_{team_id}` SET `action`=\'\',`target`=\'\' WHERE `account`=\'{account}\''
                                    fight_modify(sql.format(team_id=team_id, account=tmp['account']))

                                elif tmp['action'] == 'skill_4':
                                    sql = assistant[tmp['action']].format(team_id=team_id, m0=result[0]['account'], m1=result[1]['account'], m2=result[2]['account'], m3=result[3]['account'])
                                    fight_modify(sql)
                                    sql = assistant[tmp['action']].format(team_id=team_id, m0=result[0]['account'], m1=result[1]['account'], m2=result[2]['account'], m3=result[3]['account'])
                                    fight_modify(sql)
                                    sql = 'UPDATE `action_{team_id}` SET `action`=\'\',`target`=\'\' WHERE `account`=\'{account}\''
                                    fight_modify(sql.format(team_id=team_id, account=tmp['account']))

                                elif tmp['action'] == 'skill_u_1':
                                    sql = assistant['skill_u_1'].format(team_id=team_id, account=tmp['account'])
                                    fight_modify(sql)
                                    sql = 'UPDATE `action_{team_id}` SET `action`=\'\',`target`=\'\' WHERE `account`=\'{account}\''
                                    fight_modify(sql.format(team_id=team_id, account=tmp['account']))

                                elif tmp['action'] == 'skill_u_11':
                                    sql = assistant['skill_u_11'].format(team_id=team_id, target=tmp['target'])
                                    fight_modify(sql)
                                    sql = 'UPDATE `action_{team_id}` SET `action`=\'\',`target`=\'\' WHERE `account`=\'{account}\''
                                    fight_modify(sql.format(team_id=team_id, account=tmp['account']))

                                elif tmp['action'] == 'skill_u_2':
                                    sql = assistant['skill_u_2'].format(team_id=team_id, account=tmp['account'])
                                    fight_modify(sql)
                                    sql = 'UPDATE `action_{team_id}` SET `action`=\'\',`target`=\'\' WHERE `account`=\'{account}\''
                                    fight_modify(sql.format(team_id=team_id, account=tmp['account']))

                                elif tmp['action'] == 'skill_u_21':
                                    sql = 'SELECT `career` FROM `user_skill` WHERE `account`=\'{target}\''
                                    target_career = db_fetchone(sql.format(target=tmp['target']))
                                    if target_career['career'] == 'fighter':
                                        sql = assistant['skill_u_21'].format(team_id=team_id, num=1000*0.7, target=tmp['target'])
                                        fight_modify(sql)
                                        sql = 'UPDATE `action_{team_id}` SET `action`=\'\',`target`=\'\' WHERE `account`=\'{account}\''
                                        fight_modify(sql.format(team_id=team_id, account=tmp['account']))

                                    elif target_career['career'] == 'traveler':
                                        sql = assistant['skill_u_21'].format(team_id=team_id, num=850*0.7, target=tmp['target'])
                                        fight_modify(sql)
                                        sql = 'UPDATE `action_{team_id}` SET `action`=\'\',`target`=\'\' WHERE `account`=\'{account}\''
                                        fight_modify(sql.format(team_id=team_id, account=tmp['account']))

                                    elif target_career['career'] == 'magician':
                                        sql = assistant['skill_u_21'].format(team_id=team_id, num=700*0.7, target=tmp['target'])
                                        fight_modify(sql)
                                        sql = 'UPDATE `action_{team_id}` SET `action`=\'\',`target`=\'\' WHERE `account`=\'{account}\''
                                        fight_modify(sql.format(team_id=team_id, account=tmp['account']))

                                    elif target_career['career'] == 'assistant':
                                        sql = assistant['skill_u_21'].format(team_id=team_id, num=700*0.7, target=tmp['target'])
                                        fight_modify(sql)
                                        sql = 'UPDATE `action_{team_id}` SET `action`=\'\',`target`=\'\' WHERE `account`=\'{account}\''
                                        fight_modify(sql.format(team_id=team_id, account=tmp['account']))

                            except Exception as e:
                                print(e)
                                print('assisant' + str(tmp['action']) + 'error')
                        
                    elif tmp['action'] == 'item_1':
                        sql = 'UPDATE `status_{team_id}` SET `hp`=hp+100 WHERE `account`=\'{target}\''
                        fight_modify(sql.format(team_id=team_id, account=tmp['target']))

                    elif tmp['action'] == 'item_2':
                        sql = 'UPDATE `status_{team_id}` SET `numb`=0,`poison`=0,`blood`=0 WHERE `account`=\'{target}\''
                        fight_modify(sql.format(team_id=team_id, account=tmp['target']))

                    elif tmp['action'] == 'item_3':
                        sql = 'UPDATE `status_{team_id}` SET `hp`=hp+150 WHERE `account`=\'{target}\''
                        fight_modify(sql.format(team_id=team_id, account=tmp['target']))

                    elif tmp['action'] == 'item_4':
                        sql = 'UPDATE `status_{team_id}` SET `enhance_sk2`=enhance_sk2+3 WHERE `account`=\'{target}\''
                        fight_modify(sql.format(team_id=team_id, account=tmp['target']))

                    elif tmp['action'] == 'item_5':#不會折斷的信念
                        #取得目標的職業
                        sql = 'SELECT `career` FROM `user_skill` WHERE account=\'{target}\''
                        target_career = db_fetchone(sql.format(target=tmp['target']))

                        if target_career['career'] == 'fighter':
                            sql = 'UPDATE `status_{team_id}` SET `hp`=1000 WHERE `account`=\'{target}\''
                            fight_modify(sql.format(team_id=team_id, target=tmp['target']))

                        elif target_career['career'] == 'traveler':
                            sql = 'UPDATE `status_{team_id}` SET `hp`=850 WHERE `account`=\'{target}\''
                            fight_modify(sql.format(team_id=team_id, target=tmp['target']))

                        elif target_career['career'] == 'magician':
                            sql = 'UPDATE `status_{team_id}` SET `hp`=700 WHERE `account`=\'{target}\''
                            fight_modify(sql.format(team_id=team_id, target=tmp['target']))

                        elif target_career['career'] == 'assistant':
                            sql = 'UPDATE `status_{team_id}` SET `hp`=700 WHERE `account`=\'{target}\''
                            fight_modify(sql.format(team_id=team_id, target=tmp['target']))

                    else:
                        print('nothing can match')

            #扣血型減益
            sql = 'SELECT `poison`,`blood` FROM `status_{team_id}` WHERE `account`=\'{account}\''
            hp_debuff = fight_fatchone(sql.format(team_id=team_id, account=tmp['account']))

            if hp_debuff['poison'] != 0:
                sql = 'UPDATE `status_{team_id}` SET `hp`=hp-60  WHERE `account`=\'{account}\''
                fight_modify(sql.format(team_id=team_id, account=tmp['account']))
            
            if hp_debuff['blood'] != 0:
                sql = 'UPDATE `status_{team_id}` SET `hp`=hp-105 WHERE `account`=\'{account}\''
                fight_modify(sql.format(team_id=team_id, account=tmp['account']))
        #--------------------------------------------------------------------------------------------------------------------
        #計算倍率boss
        sql = 'SELECT `drop_sk1`,`drop_sk2`, `enhance_sk1`, `enhance_sk2`, `enhance_sk3`, `enhance_sk4` FROM `status_{team_id}` WHERE `account`=\'boss\''
        enhance_status = fight_fatchone(sql.format(team_id=team_id))
        skill_times = 1
        if enhance_status['drop_sk1'] > 0:
            skill_times *= 0.85
        if enhance_status['drop_sk2'] > 0:
            skill_times *= 0.7
        if enhance_status['enhance_sk1'] > 0:
            skill_times *= 1.15
        if enhance_status['enhance_sk2'] > 0:
            skill_times *= 1.2
        if enhance_status['enhance_sk3'] > 0:
            skill_times *= 1.5
        if enhance_status['enhance_sk4'] > 0:
            skill_times *= 2.5
        else:
            skill_times *= 1
        
        #取得boss的類別和動作
        sql = 'SELECT `b_type` FROM `status_{team_id}` WHERE `account`=\'boss\''
        b_type = fight_fatchone(sql.format(team_id=team_id))
        sql = 'SELECT `action` FROM `action_{team_id}` WHERE `account`=\'boss\''
        result = fight_fatchone(sql.format(team_id=team_id))

        #依照類別處理技能效果
        if b_type['b_type'] == 'engineer':
            if result['action'] == 'auto_attack':
                sql = engineer['auto_attack'].format(team_id=team_id, num=100*skill_times)
                fight_modify(sql)
            
            elif result['action'] == 'skill_1':
                sql = engineer['skill_1'].format(team_id=team_id, num=120*skill_times)
                fight_modify(sql)

            elif result['action'] == 'skill_2':
                sql = engineer['skill_2'].format(team_id=team_id, num=105*skill_times)
                fight_modify(sql)

                #中毒效果是否發動
                debuff_list = ['enable', 'disable']
                debuff = choices(debuff_list, weights=[2, 8])
                print(debuff[0])
                #發動
                if debuff[0] == 'enable':
                    sql = engineer['skill_21'].format(team_id=team_id)
                    fight_modify(sql)
                else:
                    pass

            elif result['action'] == 'skill_3':
                sql = engineer['skil_3'].format(team_id=team_id, num=175*skill_times)
                fight_modify(sql)
                
                #睡眠效果是否發動
                debuff_list = ['enable', 'disable']
                debuff = choices(debuff_list, weights=[4, 6])
                print(debuff[0])
                #發動
                if debuff[0] == 'enable':
                    sql = engineer['skill_31'].format(team_id=team_id)
                    fight_modify(sql)
                else:
                    pass

            elif result['action'] == 'skill_4':
                sql = engineer['skill_4'].format(team_id=team_id, num=455*skill_times)
                fight_modify(sql)

    except Exception as e:
        print(e)
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
        result = db_fetchone(sql)
        return json(result)
    except Exception as e:
        return text(str(e))

@app.post("/get_new_item")
async def get_new_item(request):
    try:
        account = request.json['account']
        item = request.json['item']
        search_item_num = 'SELECT ' + str(item) + ' FROM `user_item` WHERE account=\'' + str(account) + '\''
        result = db_fetchone(search_item_num)
        num = int(result[item]) + 1
        sql = 'UPDATE `user_item` SET ' + str(item) + '=' + str(num) + ' WHERE account=\'' + str(account) + '\''
        db_modify(sql)
        #str_re = '{"item":' + '"' + item + '"' + '}'
        #return json(str_re)
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
        result = db_fetchone(search_item_num)
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
        result = db_fetchone(sql)
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
        result = db_fetchall(sql)
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
        result = db_fetchall(sql)
        if dict(result[0])['password'] == password:
            return text("Succes")
        else:
            return text("Error")
    except Exception as e:
        print('Error Message:' + str(e))
        return text("Explode")

@app.post("/select_career")
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

@app.post("/get_career")
async def get_career(request):
    try:
        account = request.json['account']
        sql = 'SELECT `career` FROM `user_skill` WHERE `account`=\'{account}\''
        result = db_fetchone(sql.format(account=account))
        return json(result)
    except Exception as e:
        print(e)
        return text("Explode")

@app.post("/get_user_name")
async def get_user_name(request):
    try:
        account = request.json['account']
        sql = 'SELECT `name` FROM `user_info` WHERE account=\'{account}\''
        result = db_fetchone(sql.format(account=account))
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
        result = db_fetchone(sql)
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
    try:
        account = request.json['account']
        id = request.json['id']
        sql = 'SELECT * FROM `teams` WHERE id=\'{id}\''
        result = db_fetchone(sql.format(id=id))#type of `result` is dict
        for i in range(1, 4):
            #transfer keys of `result` into list
            tar = list(result.keys())[i]
            
            #find out which member is empty
            if result[tar] == '':
                #sql = 'UPDATE `teams` SET ' + tar + '=' + '\'' + account + '\'' + ' WHERE id=' + str(id)
                #sql = UPDARE `teams` SET member*=account WHERE id=******
                sql = 'UPDATE `teams` SET `{member}`=\'{account}\' WHERE `id`=\'{id}\''
                db_modify(sql.format(member=tar, account=account, id=id))
                #sql = 'UPDATE `user_info` SET `team_id`=' + str(id) + ' WHERE account=' + '\'' + account + '\''
                sql = 'UPDATE `user_info` SET `team_id`=\'{id}\' WHERE `account`=\'{account}\''
                db_modify(sql.format(id=id, account=account))
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
        result = db_fetchone(sql)#type of `result` is dict
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
        result = db_fetchone(sql)
        return json(result)
    except Exception as e:
        print(str(e))
        return text("Explode")

@app.post("get_team_member")
async def get_team_member(request):
    try:
        id = request.json['id']
        sql = 'SELECT * FROM `teams` WHERE id=' + str(id)
        result = db_fetchone(sql)
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
        b_type = request.json['b_type']

        #change user play_status 
        sql = 'SELECT `team_id` FROM `user_info` WHERE account=\'{account}\''
        result = db_fetchone(sql.format(account=account))
        id = result['team_id']
        
        sql = 'UPDATE `user_info` SET `play_status`=1 WHERE team_id={id}'
        result = db_modify(sql.format(id=id))

        #create table to store status data
        fight_modify(status_table.format(id=id))

        #insert player
        #找出所有隊員
        sql = 'SELECT * FROM `teams` WHERE leader=\'{account}\''
        result = db_fetchone(sql.format(account=account))

        #找出隊員的職業
        sql = 'SELECT `account`,`career` FROM `user_skill` WHERE `account`=\'{m0}\'or`account`=\'{m1}\'or`account`=\'{m2}\'or`account`=\'{m3}\''
        career_result = db_fetchall(sql.format(m0=result['leader'],m1=result['member1'],m2=result['member2'],m3=result['member3']))
        #初始化隊員狀態
        for i in range (0, len(career_result)):
            if (career_result[i]['career'] == 'fighter'):
                sql = 'INSERT INTO `status_{team_id}` (account,hp) VALUES (\'{account}\',\'{hp}\')'
                fight_modify(sql.format(team_id=id,account=career_result[i]['account'],hp=1000))
            elif (career_result[i]['career'] == 'traveler'):
                sql = 'INSERT INTO `status_{team_id}` (account,hp) VALUES (\'{account}\',\'{hp}\')'
                fight_modify(sql.format(team_id=id,account=career_result[i]['account'],hp=850))
            elif (career_result[i]['career'] == 'magician'):
                sql = 'INSERT INTO `status_{team_id}` (account,hp) VALUES (\'{account}\',\'{hp}\')'
                fight_modify(sql.format(team_id=id,account=career_result[i]['account'],hp=700))
            elif (career_result[i]['career'] == 'assistant'):
                sql = 'INSERT INTO `status_{team_id}` (account,hp) VALUES (\'{account}\',\'{hp}\')'
                fight_modify(sql.format(team_id=id,account=career_result[i]['account'],hp=700))
        
        #create table to store action 
        fight_modify(action_table.format(id=id))
        #初始化隊員動作
        for i in range (0, len(career_result)):
            sql = 'INSERT INTO `action_{id}` (account) VALUES (\'{account}\')'
            fight_modify(sql.format(id=id, account=career_result[i]['account']))

        #初始化boss動作與狀態
        if b_type == 'engineer':
            sql = 'INSERT INTO `status_{id}` (account,hp,b_type) VALUES (\'boss\',\'{hp}\',\'{b_type}\')'
            fight_modify(sql.format(id=id,hp=1000,b_type=b_type))
            sql = 'INSERT INTO `action_{id}` (account,action) VALUES (\'boss\', \'auto_attack\')'
            fight_modify(sql.format(id=id))

        if b_type == 'business':
            sql = 'INSERT INTO `status_{id}` (account,hp,b_type) VALUES (\'boss\',\'{hp}\',\'{b_type}\')'
            fight_modify(sql.format(id=id,hp=1000,b_type=b_type))
            sql = 'INSERT INTO `action_{id}` (account,action) VALUES (\'boss\', \'auto_attack\')'
            fight_modify(sql.format(id=id))

        if b_type == 'humanities':
            sql = 'INSERT INTO `status_{id}` (account,hp,b_type) VALUES (\'boss\',\'{hp}\',\'{b_type}\')'
            fight_modify(sql.format(id=id,hp=1200,b_type=b_type))
            sql = 'INSERT INTO `action_{id}` (account,action) VALUES (\'boss\', \'skill_1\')'
            fight_modify(sql.format(id=id))

        if b_type == 'design':
            sql = 'INSERT INTO `status_{id}` (account,hp,b_type) VALUES (\'boss\',\'{hp}\',\'{b_type}\')'
            fight_modify(sql.format(id=id,hp=2000,b_type=b_type))
            sql = 'INSERT INTO `action_{id}` (account,action) VALUES (\'boss\', \'skill_1\')'
            fight_modify(sql.format(id=id))

        if b_type == 'future':
            sql = 'INSERT INTO `status_{id}` (account,hp,b_type) VALUES (\'boss\',\'{hp}\',\'{b_type}\')'
            fight_modify(sql.format(id=id,hp=2000,b_type=b_type))
            sql = 'INSERT INTO `action_{id}` (account,action) VALUES (\'boss\', \'skill_4\')'
            fight_modify(sql.format(id=id))

        '''end = time.time()
        cost = end - start
        print('time cost:' + str(round(cost*1000, 3)) + 'ms')'''
        return text('done')
    except Exception as e:
        print(str(e))
        return text("Explode")

@app.post("/commit_status_data")#暫時停用
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
        sql = 'SELECT * FROM `status_{id}` WHERE `account`=\'{account}\''
        result = fight_fatchone(sql.format(id=id, account=account))
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
        sql = 'UPDATE `action_{team_id}` SET `action`=\'{act}\',`target`=\'{tar}\' WHERE `account`=\'{account}\''
        fight_modify(sql.format(team_id=id, act=act, tar=tar, account=account))
        return text("done")
    except Exception as e:
        print(str(e))
        return text("Explode")

@app.post("/get_action")
async def get_action(request):
    try:
        id = request.json['id']

        #產生動作清單
        sql = 'SELECT `account`,`action`,`target` FROM `action_{id}`'
        result = fight_fetchall(sql.format(id=id))
        action = '{\"act\":' + str(result) + '}'

        #啟動執行緒計算玩家的動作
        t_compute_action = threading.Thread(target=compute_action, args=(id, ))
        t_compute_action.start()
        
        '''#啟動執行緒計算boss的動作
        t_compute_boss_action = threading.Thread(target=compute_boss_action, args=(id, ))
        t_compute_boss_action.start()'''
        
        return text(action)
    except Exception as e:
        print(str(e))
        return text("Explode")

@app.post("/new_turn")
async def new_turn(requset):
    try:
        team_id = requset.json['id']

        #所有效果的回合數-1
        sql = 'SELECT `account`,`assist_lock`,`enhance_sk1`,`enhance_sk2`,`enhance_sk3`,`enhance_sk4`,`enhance_de1`,`enhance_de2`,`enhance_de3`,`gather`,`immortal`,`numb`,`sleep`,`poison`,`blood`,`drop_de1`,`drop_de2`,`drop_sk1`,`drop_sk2` \
                FROM `status_{team_id}`'
        result = fight_fetchall(sql.format(team_id=team_id))
        for j in range(0, len(result)):
            tmp_update = ''
            tmp_result = result[j]
            tmp_key = list(tmp_result[j].keys())
            for i in range (0, len(tmp_key)):
                if tmp_result[tmp_key[i]] == 0:
                    continue
                else:
                    tmp_result[tmp_key[i]] -= 1
                    tmp_update += tmp_key[i] + '=' + str(tmp_result[tmp_key[i]]) + ','
            update = tmp_update.rstrip(',')
            sql = 'UPDATE `status_{team_id}` SET {update} WHERE `account`=\'{account}\''
            fight_modify(sql.format(update=update, team_id=team_id,account=tmp_result['account']))

        #啟動其他執行緒來產生boss的動作
        t_produce_boss = threading.Thread(target=produce_boss_action,args=(team_id, ))
        t_produce_boss.start()

        return text("done")
    except Exception as e:
        print(str(e))
        return text("Explode")

@app.post("/end_turn")#暫時停用
async def end_turn(request):
    try:
        id = request.json['id']
        account = request.json['account']
        sql = 'UPDATE `action_{id}` SET `action`=\'\' WHERE `account`=\'{account}\''
        fight_modify(sql.format(id=id,account=account))
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
        sql = 'INSERT INTO `reward` (account, team_id, data, time) VALUES (\'{account}\',\'{id}\',\'{data}\',\'{now}\')'
        db_modify(sql.format(account=account,id=id,data=data,now=now))
        sql = 'DROP TABLE IF EXISTS `action_{id}`'
        fight_modify(sql.format(id=id))
        sql = 'DROP TABLE IF EXISTS `status_{id}`'
        fight_modify(sql.format(id=id))
        return text("done")
    except Exception as e:
        print(str(e))
        return text("Explode")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='2500', debug=False, access_log=True)
    app.config['workers'] = '4'