import asyncio
import logging
import os
import sys
import time
import re

async def merge(room_id):

    command = ["ffmpeg", "-i", f"{room_id}/index.m3u8", room_id + "/" + time.strftime("%Y_%m_%d.ts", time.localtime())]

    proc  = await asyncio.create_subprocess_exec(*command)
    await proc.wait()

    for file in re.findall("[A-z0-9]+\.ts", open(f"{room_id}/index.m3u8").read()):
        os.remove(f"{room_id}/{file}")

    logging.info("Merged")

if __name__ == '__main__':
    if len(sys.argv) and int(sys.argv[1]):
        from pymediainfo import MediaInfo
        with open(f"{sys.argv[1]}/index.m3u8", "w") as fp:
            fp.write("#EXTM3U\n#EXT-X-VERSION:3\n#EXT-X-TARGETDURATION:6\n")
            for name in sorted(os.listdir("./")):
                if name.endswith(".ts"):
                    info = MediaInfo.parse(name)
                    fp.write(f"#EXTINF:{float(info.tracks[0].duration)/1000},\n")
                    fp.write(f"{name}\n")
            fp.write("#EXT-X-ENDLIST\n")
        asyncio.run(merge(sys.argv[1]))
