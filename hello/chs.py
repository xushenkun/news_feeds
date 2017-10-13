# -*- coding: utf-8 -*-

import json
import codecs

with codecs.open("news_topics.json", encoding="utf-8") as fi:
        li=json.loads(fi.read())
        li=li.get("tList")
        for ch in li:
            print("('网易-%s', 'https://xskfeed.herokuapp.com/feed/163/%s'),"%(ch.get("tname"),ch.get("tid")))
