#!/usr/bin/env python
# -*- coding: utf-8 -*-

from carpenter_log_pb2 import *
import base64

rawlog = RawLog()
rawlog.type = COOKIE_MAPPING
rawlog.db_name = "ifc"
# rawlog.allyes_id = "allyes_id_1"
# rawlog.request_url = "http://idigger.allyes.com/main/adftrack?db=mso&v=3.0&r=505120417&hn=www.yougou.com&lt=i&plf=Windows%20NT%205.1&cs=utf-8&ul=zh-cn&bt=MSIE%208&bs=1280x768,32-bit,11.9%20r900,1&pt=%E8%AE%A2%E5%8D%95%E6%8F%90%E4%BA%A4%E6%88%90%E5%8A%9F%20-%20%E4%BC%98%E8%B4%AD%E7%BD%91%E4%B8%8A%E9%9E%8B%E5%9F%8E%20-%20%E4%B9%B0%E5%A5%BD%E9%9E%8B%EF%BC%8C%E4%B8%8A%E4%BC%98%E8%B4%AD&rf=&pu=%2Fpay%2FpayOnline.sc%3ForderNo%3DA631016230409%26orderRouteWay%3Duser&ncf=0&tag=&ao=T-000436-01&tsuid=&tsoid=&tst=&tkv=&ecm=%60%60A631016230409%60179.00%60%60%60product-id-1%60%60%60%60%60%60%60&ayf=%5B4%2C%22http%3A%2F%2Fwww.yougou.com%2Ftopics%2F1381298690402.html%22%5D&cct=1381938964&sc=1&nv=0"

# rawlog.z_1 = "2014-10-15 11:06:11	allyes_id_1	atc_wechat	gh_5e9ad2ac80b6|6|odmtst3B2SHb2sViLLZr4Ph29z7I		381578	183.129.194.40				http%3A%2F%2Forigin.allyes.com%2Fpixel%3Fptr%3D%26uid%3D-(%7C6%7C:9"
rawlog.z_1 = "2014-11-07 15:56:07	AMIcJ000UhE78u8c	snjz	snjz	score:13.65;recGoods_recGood_goodsScore:13.65,13.65,13.65,13.65,13.65;recGoods_recGood_goodsId:103160338,103592303,101281964,103412791,101422469;	387771	221.228.208.33		Apache-HttpClient%2F4.3.6+(java+		http%3A%2F%2Forigin.allyes.com%2Fpixel%3Fptr%3Dsnjz%26uid%3Dsnjz%26allyesid%3DEHOWrHxiVLTxESEZJSxSE%26suningid%3D141532354594024566%26data%3Dscore%253A13.65%253BrecGoods_recGood_goodsScore%253A13.67%252C13.68%252C13.64%252C13.69%252C13.66%253BrecGoods_recGood_goodsId%253A103160338%252C103592303%252C101281964%252C103412791%252C10142246"

print base64.standard_b64encode(rawlog.SerializeToString())
