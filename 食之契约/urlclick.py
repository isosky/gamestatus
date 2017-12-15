#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017-12-15 10:44
# @Author  : wtr
# @File    : urlclick.py

import random
import requests
import time

url = 'http://p1.66m.in/Recommend/set/106509'

USER_AGENT = [
    'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
    'Mozilla/5.0 (compatible; Bingbot/2.0; +http://www.bing.com/bingbot.htm)',
    'Mozilla/5.0 (compatible; Yahoo! Slurp; http://help.yahoo.com/help/us/ysearch/slurp)',
    'DuckDuckBot/1.0; (+http://duckduckgo.com/duckduckbot.html)',
    'Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)',
    'Mozilla/5.0 (compatible; YandexBot/3.0; +http://yandex.com/bots)',
    'ia_archiver (+http://www.alexa.com/site/help/webmasters; crawler@alexa.com)'
]

headers = {'User-Agent': random.choice(USER_AGENT)}


r = requests.get(url)
r.encoding = 'utf-8'
