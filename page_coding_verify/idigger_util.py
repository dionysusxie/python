#!/usr/bin/env python -u

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
        ret.append(cls.PAGE_TYPES[0])
        ret.append(cls.PAGE_TYPES[1])
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

def _unit_test():
    _unit_test_get_http_query_section()
    _unit_test_get_site_code()
    _unit_test_get_page_url()

_unit_test()
