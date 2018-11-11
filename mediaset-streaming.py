#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import time
import subprocess
from selectmenu import SelectMenu


RTI_LIST = ("https://feed.entertainment.tv.theplatform.eu/f/PR1GhC/mediaset-pr"
            "od-all-listings?byListingTime={ts}~{ts}&byCallSign=#callSign#")

RTI_CHANNEL = ("https://api-ott-prod-fe.mediaset.net/PROD/play/alive/nownext/v"
               "1.0?channelId={ch}")


def get_mediaset_channels():
    r = requests.get(RTI_LIST.format(ts=int(time.time() * 1000)))
    chdata = r.json()
    result = []
    for ch in chdata["entries"]:
        result.append((ch["guid"], ch["title"]))
    return result


def open_mediaset_streaming(channel_id):
    r = requests.get(RTI_CHANNEL.format(ch=channel_id))
    stdata = r.json()
    url = (stdata["response"]["tuningInstruction"]
                 ["urn:theplatform:tv:location:any"][0]["publicUrls"][0])
    subprocess.call(["open", "-a", "QuickTime Player", url])


chmap = {v: k for k, v in get_mediaset_channels()}
menu = SelectMenu()
menu.add_choices(list(chmap.keys()))
result = menu.select("Scegli il canale che vuoi guardare:")
open_mediaset_streaming(chmap[result])
