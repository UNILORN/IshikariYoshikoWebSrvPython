#-*- coding:utf-8 -*-

from websocket import create_connection
import sys
import os
import time
from os.path import join, dirname
from dotenv import load_dotenv
import json
import MySQLdb

def WebsocketConnect():
    dotenv_path = join(dirname(__file__), '.env')
    load_dotenv(dotenv_path)
    
    url = os.environ.get("WS_URL")
    channel = os.environ.get("WS_CHANNEL")
    token = os.environ.get("ACCESS_TOKEN")

    ws_url = url + "?" + "channel_id=" + channel + "&access_token=" + token

    ws = create_connection(ws_url)
    return ws

def WebsocketReceive(con,ws):
     while True:
        result =  ws.recv()
        db_insert(con,json.loads(result))


 
def db_connect():
    dotenv_path = join(dirname(__file__), '.env')
    load_dotenv(dotenv_path)

    # 接続する 
    con = MySQLdb.connect(
            user=os.environ.get("DB_USERNAME"),
            passwd=os.environ.get("DB_PASSWORD"),
            host='localhost',
            db=os.environ.get("DB_DATABASE"))
 
    return con

def db_insert(con,data):
    
    # カーソルを取得する
    cur= con.cursor()
     
    # クエリを実行する
    tableList = {
        "pressure":data["pressure"],
        "accelerometer_z":data["accelerometer_z"],
        "gyroscope_y":data["gyroscope_y"],
        "gyroscope_x":data["gyroscope_x"],
        "gyroscope_z":data["gyroscope_z"],
        "degrees_y":data["degrees_y"],
        "temperature":data["temperature"],
        "degrees_r":data["degrees_r"],
        "degrees_p":data["degrees_p"],
        "accelerometer_y":data["accelerometer_y"],
        "accelerometer_x":data["accelerometer_x"],
        "humidity":data["humidity"],
        "compass_x":data["compass_x"],
        "compass_y":data["compass_y"],
        "compass_z":data["compass_z"]
    }
    column = ""
    values = ""
    for k,v in tableList.items():
        column = column + k + ","
        values = values + str(v) + ","
    
    column = column[:-1]
    values = values[:-1]

    sql = "insert into sensor ("+column+") values("+values+");"
    cur.execute(sql)
    con.commit()

    print("[ Database Insert ] SUCCESS!!!")
    cur.close

if __name__ == '__main__':
    ws = WebsocketConnect()
    con = db_connect()
    WebsocketReceive(con,ws)
    con.close
    ws.close()

