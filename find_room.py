import sys
import asyncio
import requests

async def find(user_id):
    url = "https://webcast3.amemv.com/webcast/room/live_room_id/?aid=1128"

    payload = "user_id={}%2C".format(user_id)
    headers = {
        'Host': 'webcast3.amemv.com',
        'sdk-version': '1',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'user-agent': 'com.ss.android.ugc.aweme/960 (Linux; U; Android 6.0.1; zh_TW; D6653; Build/23.5.A.0.575; Cronet/77.0.3844.0)',
        'accept-encoding': 'gzip, deflate, br'
    }

    return requests.request("POST", url, headers=headers, data=payload).json()

if __name__ == '__main__':
    if len(sys.argv) and int(sys.argv[1]):
        print(asyncio.run(find(sys.argv[1])))