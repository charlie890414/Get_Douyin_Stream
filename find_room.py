import time

import requests
import logging

from download import download
from fix_stream import fix
from merge import merge
from tools import clear

logging.basicConfig(level=logging.DEBUG)

url = "https://webcast3.amemv.com/webcast/room/live_room_id/?aid=1128"

user_id = "97682711563"

payload = "user_id={}%2C".format(user_id)
headers = {
    'Host': 'webcast3.amemv.com',
    'sdk-version': '1',
    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'user-agent': 'com.ss.android.ugc.aweme/960 (Linux; U; Android 6.0.1; zh_TW; D6653; Build/23.5.A.0.575; Cronet/77.0.3844.0)',
    'accept-encoding': 'gzip, deflate, br'
}

while True:
    response = requests.request(
        "POST", url, headers=headers, data=payload).json()

    if response.get("status_code") != 0:
        logging.info(response.get("status_msg"))
        exit()

    logging.debug(time.strftime("%H:%M:%S", time.localtime()))

    if response.get('data').get('room_id').get(user_id):
        clear()
        room_id = str(response.get('data').get('room_id').get(user_id))

        logging.info(f"roomid: {room_id}")
        download(room_id)
        fix(room_id)
        merge(room_id)
        clear()

    time.sleep(10)
