#-*- coding:utf-8 -*-

from websocket import create_connection
import sys
import os
import time
from os.path import join, dirname
from dotenv import load_dotenv


if __name__ == '__main__':
    dotenv_path = join(dirname(__file__), '.env')
    load_dotenv(dotenv_path)
    
    url = os.environ.get("WS_URL")
    channel = os.environ.get("WS_CHANNEL")
    token = os.environ.get("ACCESS_TOKEN")

    ws_url = url + "?" + "channel_id=" + channel + "&access_token=" + token

    ws = create_connection(ws_url)
    while True:
        result =  ws.recv()
        print(result)

    ws.close()

