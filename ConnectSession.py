import pymysql.cursors

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
#-----------------------------------------------------------------------------------------------------
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