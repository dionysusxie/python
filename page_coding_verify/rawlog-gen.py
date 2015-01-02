#!/usr/bin/env python -u
# -*- coding: utf-8 -*-

from carpenter_log_pb2 import *
import base64
import time

rawlog = RawLog()
rawlog.type = COOKIE_MAPPING
rawlog.db_name = "ifc"
rawlog.request_url = "http://idigger.allyes.com/main/adftrack?db=mso&v=3.0&r=505120417&hn=www.yougou.com&lt=i&plf=Windows%20NT%205.1&cs=utf-8&ul=zh-cn&bt=MSIE%208&bs=1280x768,32-bit,11.9%20r900,1&pt=%E8%AE%A2%E5%8D%95%E6%8F%90%E4%BA%A4%E6%88%90%E5%8A%9F%20-%20%E4%BC%98%E8%B4%AD%E7%BD%91%E4%B8%8A%E9%9E%8B%E5%9F%8E%20-%20%E4%B9%B0%E5%A5%BD%E9%9E%8B%EF%BC%8C%E4%B8%8A%E4%BC%98%E8%B4%AD&rf=&pu=%2Fpay%2FpayOnline.sc%3ForderNo%3DA631016230409%26orderRouteWay%3Duser&ncf=0&tag=&ao=T-000436-01&tsuid=&tsoid=&tst=&tkv=&ecm=%60%60A631016230409%60179.00%60%60%60product-id-1%60%60%60%60%60%60%60&ayf=%5B4%2C%22http%3A%2F%2Fwww.yougou.com%2Ftopics%2F1381298690402.html%22%5D&cct=1381938964&sc=1&nv=0"
rawlog.timestamp = int(time.time())

print base64.standard_b64encode(rawlog.SerializeToString())
