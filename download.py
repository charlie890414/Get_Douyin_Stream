import os
import sys
import re
import requests
import m3u8
import aria2p
import logging
import asyncio

aria2 = aria2p.API(
    aria2p.Client(
        host="http://localhost",
        port=6800,
        secret="Aria2-Password"
    )
)

async def download(room_id):

    room_url = f"https://webcast.amemv.com/webcast/room/ping/audience/?room_id={room_id}&only_status=1&aid=1128"
    url = f'https://webcast.amemv.com/webcast/reflow/{room_id}'
    logging.info(url)
    response = requests.get(url).text
    hls_pull_url = re.search(r'"hls_pull_url":"(.*?m3u8)"', response).group(1)
    rtmp_pull_url = re.search(r'"rtmp_pull_url":"(.*?flv)"', response).group(1)
    logging.debug(rtmp_pull_url)
    logging.debug(hls_pull_url)

    if not os.path.exists(room_id):
        os.makedirs(room_id)

    fp = open(f"{room_id}/index.m3u8", "w")
    fp.write("#EXTM3U\n#EXT-X-VERSION:3\n#EXT-X-TARGETDURATION:6\n")
                        
    while True:
        status = requests.get(room_url).json()['data']['room_status']
        if status == 4:
            logging.info("Video end")
            break
        elif status != 2:
            continue

        try:
            M3U8 = m3u8.load(hls_pull_url)
        except:
            continue

        for ts in M3U8.segments:
            filename = ts.uri.split('?')[0].split('/')[-1]
            if filename in map(lambda x: str(x).split('?')[0], aria2.get_downloads()):
                continue
            logging.debug(room_id)
            logging.info(ts.absolute_uri)
            aria2.add_uris([ts.absolute_uri], {"dir": os.getcwd() + '/' +room_id + '/'})
            fp.write(f"#EXTINF:{ts.duration},\n")
            fp.write(f"{filename}\n")      

        await asyncio.sleep(M3U8.target_duration)

    fp.write("#EXT-X-ENDLIST\n")
    fp.close()

    logging.info("Finish")


if __name__ == '__main__':
    if len(sys.argv) and int(sys.argv[1]):
        asyncio.run(download(sys.argv[1]))
