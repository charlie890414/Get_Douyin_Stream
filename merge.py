import os
import subprocess
import sys
import time
import logging
import asyncio


async def merge(room_id):

    filename = "%s.txt" % room_id

    with open(filename, "w") as fp:
        for name in os.listdir(room_id + "/fixed"):
            if name.endswith(".ts"):
                fp.write("file " + room_id + '/fixed/' + name + '\n')

    command = ["ffmpeg", "-y", "-f", "concat", "-i",
               filename, "-c", "copy", room_id + "/" + time.strftime("%Y_%m_%d.mp4", time.localtime())]

    proc  = await asyncio.create_subprocess_exec(*command)
    await proc.wait()

    if not proc.returncode:
        os.remove(filename)

    logging.info("Merged")


if __name__ == '__main__':
    if len(sys.argv) and int(sys.argv[1]):
        asyncio.run(merge(sys.argv[1]))
