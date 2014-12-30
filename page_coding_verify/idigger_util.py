#!/usr/bin/env python -u
# -*- coding: utf-8 -*-

import urllib
import urlparse


class IdiggerUtil(object):

    ENUM_SITE_PAGE = 0  # sitepage
    ENUM_SKU_PAGE = 1  # skupage
    ENUM_CART_PAGE = 2  # cartpage
    ENUM_ORDER_PAGE = 3  # orderpage
    ENUM_PAID_PAGE = 4  # paidpage
    ENUM_CONVERSION_PAGE = 5  # conversionpage
    ENUM_CONVERSION_BUTTON = 6  # conversionbutton
    ENUM_EVENT_PAGE = 7  # eventpage
    ENUM_EVENT_BUTTON = 8  # eventbutton
    ENUM_MAX = 9

    PAGE_TYPES = ('sitepage',  # 0
                  'skupage',  # 1
                  'cartpage',  # 2
                  'orderpage',  # 3
                  'paidpage',  # 4
                  'conversionpage',  # 5
                  'conversionbutton',  # 6
                  'eventpage',  # 7
                  'eventbutton',  # 8
    )

    @classmethod
    def get_http_query_section(cls, url, query_key):
        """
        Args:
            url: The input http url; a string;
            query_key: Section name to be queried; a string;

        Returns:
            A string, the unquoted value of the 'query_key'; or None if the
            'query_key' not found. E.g.,
                url = http://idigger.allyes.com/main/adftrack?db=mso&v=3.0
                query_key = db, then return: mso;
                query_key = v, then return: 3.0;
                query_key = db2, then return: None.
        """

        try:
            parsed_url = urlparse.urlparse(url)
            query_params = urlparse.parse_qs(parsed_url.query)
            if query_params.has_key(query_key):
                return query_params[query_key][0]
            else:
                return None
        except:
            return None

    @classmethod
    def get_site_code(cls, url):
        return cls.get_http_query_section(url, 'ao')

    @classmethod
    def get_page_url(cls, url):
        """
        Returns: hn + pu; None if not found!
        """

        hn = cls.get_http_query_section(url, 'hn')
        if not hn: return None

        pu = cls.get_http_query_section(url, 'pu')
        if not pu: return None

        return hn + pu

    @classmethod
    def get_product_codes(cls, url):
        """
        ecm 第七列的三种格式：
            产品分类^产品名^产品ID^^产品价格
            商品id
            商品id*数量

        Returns:
            A tuple of string. E.g., ("0568022", "0568023")
            Or None if there is no product code.
        """

        ecm = cls.get_http_query_section(url, 'ecm')
        if not ecm: return None

        fields = ecm.split('`')
        if not fields: return None
        if len(fields) < 7: return None

        f7 = urllib.unquote(fields[6])
        if not f7: return None

        f7_fields = f7.split('^')

        if len(f7_fields) == 1:
            pid_and_num = f7_fields[0].split('*')
            if pid_and_num[0]:
                return (pid_and_num[0], )
        elif len(f7_fields) >= 3:
            if f7_fields[2]:
                return (f7_fields[2], )

        return None

    @classmethod
    def get_page_kinds(cls, rawlog):
        """Get page kinds.
        Args:
            rawlog: A log of kind RawLog.

        Returns:
            A tuple contains the page-kinds of input rawlog.
            E.g., ('sitepage', ...)

        Raises:
            None
        """

        ret = []

        site_code = cls.get_site_code(rawlog.request_url)
        if not site_code: return tuple(ret)

        return tuple(ret)


def _unit_test_get_http_query_section():
    test_url = 'http://idigger.allyes.com/main/adftrack'  # no query
    if IdiggerUtil.get_http_query_section(test_url, 'a') is not None:
        assert False, 'get_http_query_section(): Unit test failed: #0'

    test_url = 'http://idigger.allyes.com/main/adftrack?&cc&=&db=mso&v=3.0&pids=123%7c4%7c5%7c6'

    if IdiggerUtil.get_http_query_section(test_url, 'a') is not None:
        assert False, 'get_http_query_section(): Unit test failed: #1'

    if IdiggerUtil.get_http_query_section(test_url, 'db') != 'mso':
        assert False, 'get_http_query_section(): Unit test failed: #2'

    if IdiggerUtil.get_http_query_section(test_url, 'v') != '3.0':
        assert False, 'get_http_query_section(): Unit test failed: #3'

    if IdiggerUtil.get_http_query_section(test_url, 'pids') != '123|4|5|6':
        assert False , 'get_http_query_section(): Unit test failed: #4'

def _unit_test_get_site_code():
    url_no_sitecode = 'http://idigger.allyes.com/main/adftrack?&cc&=&db=mso&v=3.0&pids=123%7c4%7c5%7c6'

    if IdiggerUtil.get_site_code(url_no_sitecode) is not None:
        assert False, 'IdiggerUtil.get_site_code(): Unit test failed: #0'

    if IdiggerUtil.get_site_code(url_no_sitecode + '&ao=T-000032-2') != 'T-000032-2':
        assert False, 'IdiggerUtil.get_site_code(): Unit test failed: #1'

def _unit_test_get_page_url():
    url = 'http://idigger.allyes.com/main/adftrack?db=mso&v=3.0&r=1315018823&hn=www.yougou.com&lt=i&plf=Windows%20NT%205.1&cs=UTF-8&ul=zh-cn&bt=Chrome&bs=1152x864,24-bit,11.6%20r602,1&pt=%E3%80%90%E6%96%B0%E7%99%BE%E4%BC%A6New%20Balance%20ML515%20%E8%93%9D%E8%89%B2%E3%80%91New%20Balance%E6%96%B0%E7%99%BE%E4%BC%A6%202014%E5%B9%B4%E6%96%B0%E6%AC%BE%E7%94%B7%E5%AD%90%E5%A4%8D%E5%8F%A4%E9%9E%8BML515OB&rf=http%3A%2F%2Fwww.yougou.com%2Ff-newbalance-0-0-1-1.html&pu=%2Fc-newbalance%2Fsku-ml515-100061692.shtml&ncf=0&tag=&ao=T-000436-01&tsuid=&tsoid=&tst=&tkv=&ecm=66364734346e41f7aa4eef4af5749079%60%60%60%60%60%60100061692%60%60%60%60%60%60%60&ayf=&cct=1418359803&sc=690&nv=0'
    if IdiggerUtil.get_page_url(url) != 'www.yougou.com/c-newbalance/sku-ml515-100061692.shtml':
        assert False, 'IdiggerUtil.get_page_url(): Unit test failed: #0'

def _unit_test_get_product_codes():
    test_url_no_ecm = 'http://idigger.allyes.com/main/adftrack?db=mso&v=3.0&r=802029047&hn=www.yougou.com&lt=i&plf=Linux&cs=UTF-8&ul=en-us&bt=Chrome&bs=1366x768,24-bit,11.8%20r800,1&pt=%E3%80%90DickiesDickies%20031581%20%E6%B7%B1%E6%B5%B7%E5%86%9B%E8%93%9D%E6%9D%A1%E7%BA%B9%E3%80%91Dickies%E5%B8%9D%E5%AE%A2%20%E7%94%B7%E5%A3%AB%E6%B7%B1%E6%B5%B7%E5%86%9B%E8%93%9D%E6%9D%A1%E7%BA%B9%E7%89%9B%E4%BB%94%E8%A3%A4%20031581&rf=http%3A%2F%2Fwww.yougou.com%2Ff-dickies-1LTFA-0-0.html&pu=%2Fc-dickies%2Fsku-031581-99919909.shtml&ncf=0&tag=&ao=T-000436-01&tsuid=&tsoid=&tst=&tkv=&ayf=&cct=1382351003&sc=11&nv=1'

    # 0
    ecm = '&ecm=%60%60%60%60%60%6099919909%60%60%60%60%60%60%60'
    pcodes = IdiggerUtil.get_product_codes(test_url_no_ecm + ecm)
    if pcodes and len(pcodes) == 1 and pcodes[0] == '99919909':
        pass
    else:
        assert False, 'IdiggerUtil.get_product_codes(): Unit test failed: #0'

    # 1.1, product id
    ecm = '&ecm=``````99919907```````'
    pcodes = IdiggerUtil.get_product_codes(test_url_no_ecm + ecm)
    if pcodes and len(pcodes) == 1 and pcodes[0] == '99919907':
        pass
    else:
        assert False, 'get_product_codes(): Unit test failed: #1.1'

    # 1.2, pid*number
    ecm = '&ecm=``````99919907*3```````'
    pcodes = IdiggerUtil.get_product_codes(test_url_no_ecm + ecm)
    if pcodes and len(pcodes) == 1 and pcodes[0] == '99919907':
        pass
    else:
        assert False, 'get_product_codes(): Unit test failed: #1.2'

    # 3, No ecm
    pcodes = IdiggerUtil.get_product_codes(test_url_no_ecm)
    if pcodes:
        assert False, 'get_product_codes(): Unit test failed: #3'

    # 4, No product
    ecm = '&ecm=%60%60%60%60%60%60%60%60%60%60%60%60%60'
    pcodes = IdiggerUtil.get_product_codes(test_url_no_ecm + ecm)
    if pcodes:
      assert False, 'get_product_codes(): Unit test failed: #4'

    #
    # 5, catrgory^pname^pid^^price
    #

    # 5.1
    ecm = u'&ecm=``````153^韩国SKINFOOD黑豆双头眉笔0.2g 5号 灰褐色 进口^A010262^^22```````'
    pcodes = IdiggerUtil.get_product_codes(test_url_no_ecm + ecm)
    if pcodes and len(pcodes) == 1 and pcodes[0] == 'A010262':
        pass
    else:
        assert False, 'get_product_codes(): Unit test failed: #5.1'

    # 5.2
    ecm = u'&ecm=``````153^韩国SKINFOOD黑豆双头眉笔0.2g 5号 灰褐色 进口^^^22```````'
    pcodes = IdiggerUtil.get_product_codes(test_url_no_ecm + ecm)
    if pcodes:
        assert False, 'get_product_codes(): Unit test failed: #5.2'

    # 5.3
    ecm = u'&ecm=``````153^韩国SKINFOOD黑豆双头眉笔0.2g 5号 灰褐色 进口```````'
    pcodes = IdiggerUtil.get_product_codes(test_url_no_ecm + ecm)
    if pcodes:
        assert False, 'get_product_codes(): Unit test failed: #5.3'

    # 5.4
    ecm = '&ecm=``````153^```````'
    pcodes = IdiggerUtil.get_product_codes(test_url_no_ecm + ecm)
    if pcodes:
        assert False, 'get_product_codes(): Unit test failed: #5.4'

def _unit_test():
    _unit_test_get_http_query_section()
    _unit_test_get_site_code()
    _unit_test_get_page_url()
    _unit_test_get_product_codes()

_unit_test()
