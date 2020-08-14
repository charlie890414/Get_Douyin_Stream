import os
import subprocess
import sys
import time
import requests
import m3u8
import aria2p
import logging

aria2 = aria2p.API(
    aria2p.Client(
        host="http://localhost",
        port=6800,
        secret="Aria2-Password"
    )
)


def download(room_id):

    url = "https://webcast-hl.amemv.com/webcast/room/reflow/info/?room_id=%s&live_id=1" % room_id
    logging.info(url)
    response = requests.get(url).json()
    hls_pull_url = response.get('data').get(
        'room').get('stream_url').get('hls_pull_url')
    rtmp_pull_url = response.get('data').get(
        'room').get('stream_url').get('rtmp_pull_url')
    logging.debug(rtmp_pull_url)
    logging.debug(hls_pull_url)

    if not os.path.exists(room_id):
        os.makedirs(room_id)

    option = aria2.get_global_options()
    option.dir = os.getcwd() + '/' +room_id + '/'

    while True:
        try:
            M3U8 = m3u8.load(hls_pull_url)
        except:
            logging.info("Video End")
            break

        for ts in M3U8.segments:
            filename = ts.uri.split('?')[0].split('/')[-1]
            if filename in map(lambda x: str(x).split('?')[0], aria2.get_downloads()):
                continue
            logging.info(ts.absolute_uri)
            aria2.add_uris([ts.absolute_uri])

        time.sleep(M3U8.target_duration)

    logging.info("Finish")


if __name__ == '__main__':
    if len(sys.argv) and int(sys.argv[1]):
        gen_download(sys.argv[1])
