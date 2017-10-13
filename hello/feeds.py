# -*- coding: utf-8 -*-

import os, json
import codecs
from datetime import datetime

import requests

from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Rss201rev2Feed 
from django.utils.encoding import force_text
from django.utils.html import escape
from django.utils import feedgenerator
from django.http import Http404

BASE_DIR = os.path.dirname(__file__)

CHANNELS_FILE_PATH = os.path.join(BASE_DIR, "news_topics.json")

CHANNELS = []

with codecs.open(CHANNELS_FILE_PATH, encoding="utf-8") as fi:
    CHANNELS = json.loads(fi.read())
    CHANNELS = CHANNELS["tList"]

class NeteaseChannelFeed(Feed):
    feed_type = Rss201rev2Feed
    title = "网易新闻栏目"
    link = "http://3g.163.com/touch/news"
    feed_url = "/feed/163"
    description = "网易新闻栏目订阅源"
    categories = None
    feed_copyright = "Copyright 2017"
    title_template = None
    description_template = None

    def get_object(self, request):
        return CHANNELS

    def items(self, obj):
        return CHANNELS

    def item_title(self, item):
        return escape(force_text(item.get("tname")))

    def item_description(self, item):
        return force_text(item.get("alias"))

    def item_link(self, item):
        return "/feed/163/%s" % item.get("tid")

class NeteaseFeed(Feed):
    feed_type = Rss201rev2Feed
    title = "网易新闻"
    link = "http://3g.163.com/touch/news"
    feed_url = "/feed/163"
    description = "网易新闻订阅源"
    categories = None
    feed_copyright = "Copyright 2017"
    title_template = None
    description_template = None

    def get_object(self, request, tid):
        for ch in CHANNELS:
            if ch.get("tid") == tid:
                categories = (ch.get("tname"), )
                return ch
        raise Http404("Not found channel")

    def items(self, obj):
        ch_url = "http://c.m.163.com/nc/article/headline/%s/0-100.html" % obj.get("tid")
        headers = {'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_0 like Mac OS X) AppleWebKit/602.1.38 (KHTML, like Gecko) Version/10.0 Mobile/14A5297c Safari/602.1'}
        r = requests.get(ch_url, headers=headers)        
        if r is not None and r.status_code == 200:
            ch_list = r.json()
            ch_list = ch_list.get(obj.get("tid"))
            return ch_list
        return []

    def item_title(self, item):
        return escape(force_text(item.get("title")))

    def item_description(self, item):
        return force_text(item.get("digest"))

    def item_link(self, item):
        return force_text(item.get("url"))

    def item_pubdate(self, item):
        return datetime.strptime(item.get("mtime"), "%Y-%m-%d %H:%M:%S")

    def item_updateddate(self, item):
        return datetime.strptime(item.get("lmodify"), "%Y-%m-%d %H:%M:%S")

    def item_guid(self, item):
        return item.get("docid")

    def item_copyright(self, item):
        return item.get("source")      

    def item_enclosures(self, item):
        enc_url = item.get("imgsrc")
        if enc_url:
            enc = feedgenerator.Enclosure(
                url=force_text(enc_url),
                length=force_text(1000),
                mime_type=force_text("image/*"),
            )
            return [enc]
        return []