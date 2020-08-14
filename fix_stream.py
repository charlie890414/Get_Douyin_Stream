import os
import subprocess
import sys
import time
import logging


def fix(room_id):
    if not os.path.exists(room_id + "/fixed"):
        os.makedirs(room_id + "/fixed")

    for name in os.listdir(room_id):
        if name.endswith(".ts"):
            command = ["ffmpeg", "-n", "-hwaccel", "cuda", "-i", room_id + "/" + name, "-c:v", "libx264", '-r', '15',
                       '-c:a', 'aac', '-strict', '2', '-b:a', '64k', '-ar', '44100', '-ac', '2', '-async', '1', room_id + "/fixed/" + name]
            subprocess.run(command)

    logging.info("fixed")


if __name__ == '__main__':
    if len(sys.argv) and int(sys.argv[1]):
        fix(sys.argv[1])
