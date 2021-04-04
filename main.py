from find_room import find
from download import download
from merge import merge
import asyncio
import logging
import os
from logging.handlers import TimedRotatingFileHandler

FORMAT = '%(asctime)s %(levelname)s: %(message)s'
if not os.path.exists("log"):
    os.makedirs("log")
logging.basicConfig(level=logging.DEBUG, format=FORMAT, handlers=[TimedRotatingFileHandler("./log/doyin", 'D', 1, 1)])

async def start(user_id):

    while True:
        logging.debug("Check user " + user_id + " living or not")
        response = await find(user_id)

        if response.get("status_code") != 0:
            logging.info(response.get("status_msg"))
            exit()

        if response.get('data').get('room_id').get(user_id):
            room_id = str(response.get('data').get('room_id').get(user_id))

            logging.info(f"roomid: {room_id}")
            await download(room_id)
            await merge(room_id)

        await asyncio.sleep(10)

async def main():

    user_ids = open("user_ids.txt").read().split()

    tasks = [start(user_id) for user_id in user_ids]

    await asyncio.gather(*tasks, return_exceptions=True)

if __name__ == "__main__":
    asyncio.run(main())