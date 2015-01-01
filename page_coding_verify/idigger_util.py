#!/usr/bin/env python -u
# -*- coding: utf-8 -*-

import urllib
import urlparse

"""
线上 yougou 的一个订单提交页面(未付款)产生的 idigger.allyes.com 的代码：

完整URL:
http://idigger.allyes.com/main/adftrack?db=mso&v=3.0&r=2136346819&hn=www.yougou.com&lt=i&plf=Mac%20OS%20X&cs=UTF-8&ul=zh-cn&bt=Safari&bs=1280x800,24-bit,16.0%20r0,1&pt=%E8%AE%A2%E5%8D%95%E6%8F%90%E4%BA%A4%E6%88%90%E5%8A%9F%20-%20%E4%BC%98%E8%B4%AD%E7%BD%91%E4%B8%8A%E9%9E%8B%E5%9F%8E%20-%20%E4%B9%B0%E5%A5%BD%E9%9E%8B%EF%BC%8C%E4%B8%8A%E4%BC%98%E8%B4%AD&rf=http%3A%2F%2Fwww.yougou.com%2FcontinueOrder.jhtml%3FtradeCurrency%3DCNY&pu=%2Fpay%2FpayOnline.sc%3FonlinePayStyleNo%3D1001%26uname%3D2BF29E89E039D2E485326C5C1CA806E7%26skuid%3D99967948%26orderNo%3DA641231151522&ncf=0&tag=&ao=T-000436-01&tsuid=&tsoid=&tst=&tkv=&ecm=4ec3bcaba90844cc86f0ce4f6badee26%60%60A641231151522%60199.00%6099967948%60%60%60%60%60%60%60%601%60&ayf=&cct=1419846516&sc=34&nv=0

查询字符串：
db=mso&v=3.0&r=2136346819&hn=www.yougou.com&lt=i&plf=Mac%20OS%20X&cs=UTF-8&ul=zh-cn&bt=Safari&bs=1280x800,24-bit,16.0%20r0,1&pt=%E8%AE%A2%E5%8D%95%E6%8F%90%E4%BA%A4%E6%88%90%E5%8A%9F%20-%20%E4%BC%98%E8%B4%AD%E7%BD%91%E4%B8%8A%E9%9E%8B%E5%9F%8E%20-%20%E4%B9%B0%E5%A5%BD%E9%9E%8B%EF%BC%8C%E4%B8%8A%E4%BC%98%E8%B4%AD&rf=http%3A%2F%2Fwww.yougou.com%2FcontinueOrder.jhtml%3FtradeCurrency%3DCNY&pu=%2Fpay%2FpayOnline.sc%3FonlinePayStyleNo%3D1001%26uname%3D2BF29E89E039D2E485326C5C1CA806E7%26skuid%3D99967948%26orderNo%3DA641231151522&ncf=0&tag=&ao=T-000436-01&tsuid=&tsoid=&tst=&tkv=&ecm=4ec3bcaba90844cc86f0ce4f6badee26%60%60A641231151522%60199.00%6099967948%60%60%60%60%60%60%60%601%60&ayf=&cct=1419846516&sc=34&nv=0

pu:
/pay/payOnline.sc?onlinePayStyleNo=1001&uname=2BF29E89E039D2E485326C5C1CA806E7&skuid=99967948&orderNo=A641231151522

ecm:
4ec3bcaba90844cc86f0ce4f6badee26``A641231151522`199.00`99967948````````1`
"""

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

    assert len(PAGE_TYPES) == ENUM_MAX

    @classmethod
    def get_splited_item(cls, src_str, item_index, sep=None, unquote=False):
        """
        Args:
            src_str: A string, the source string to be splited.
            item_index: A integer, item index wanted; can be negative.
            sep: A string, the string used to split the 'src_str'.
            unquote: A bool value.

        Returns:
            A string;
            Or None if 'item_index' out of index.
        """

        item_list = src_str.split(sep)
        if not item_list: return None
        try:
            if unquote:
                return urllib.unquote(item_list[item_index])
            else:
                return item_list[item_index]
        except IndexError:
            return None

    @classmethod
    def parse_qs(cls, qs, sep1='&', sep2='=', keep_blank_values=False,
                 strict_parsing=False):
        """Parse a query given as a string argument with the given separators.

        Arguments:
            qs: string to be parsed

            sep1: The primary separator.

            sep2: The secondary separator.

            keep_blank_values: flag indicating whether blank values in
                percent-encoded queries should be treated as blank strings.  A
                true value indicates that blanks should be retained as blank
                strings.  The default false value indicates that blank values
                are to be ignored and treated as if they were  not included.

            strict_parsing: flag indicating what to do with parsing errors. If
                false (the default), errors are silently ignored. If true,
                errors raise a ValueError exception.

        Returns:
            A dict where the value of each key is a list of string.
        """

        pairs = [s for s in qs.split(sep1)]
        r = {}
        for name_value in pairs:
            if not name_value and not strict_parsing:
                continue
            nv = name_value.split(sep2, 1)
            if len(nv) != 2:
                if strict_parsing:
                    raise ValueError, "bad query field: %r" % (name_value,)
                # Handle case of a control-name with no equal sign
                if keep_blank_values:
                    nv.append('')
                else:
                    continue
            if len(nv[1]) or keep_blank_values:
                name = nv[0]
                value = nv[1]
                if name in r:
                    r[name].append(value)
                else:
                    r[name] = [value]
        return r

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
    def get_site_code(cls, url=None, query_params=None):
        """Return a string or None"""
        TXT_AO = 'ao'
        if url:
            return cls.get_http_query_section(url, TXT_AO)
        elif query_params:
            if query_params.has_key(TXT_AO):
                return query_params[TXT_AO][0]
            else:
                return None
        else:
            assert False

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
    def get_skuid_list_in_shopcart(cls, url):
        """Get tuple of products in shop-cart.

        日志的三种格式：
            event-id@产品类别^产品名^产品ID|产品类别^产品名^产品ID|...
            event-id@产品ID|产品ID|...
            产品ID|产品ID|...

        Returns:
            A tuple of string, maybe empty.
            E.g., ("0568022", "0568023").
        """

        ecm = cls.get_http_query_section(url, 'ecm')
        if not ecm: return ()

        fields = ecm.split('`')
        if len(fields) < 9: return ()

        shopcart = urllib.unquote(fields[8])
        if not shopcart: return ()

        shopcart_fields = shopcart.split('@')
        if len(shopcart_fields) > 2: return ()

        product_list = shopcart_fields[-1].split('|')
        skuid_list = []
        for p in product_list:
            skuid = p.split('^')[-1]
            if skuid: skuid_list.append(skuid)

        return tuple(skuid_list)

    @classmethod
    def orderpage_or_paidpage(cls, query_params):
        """
        Args:
            query_params: A dict returned form urlparse.parse_qs().
                E.g., { 'ecm': ['````````````'] }

        Returns:
            ENUM_ORDER_PAGE or
            ENUM_PAID_PAGE or
            None
        """

        if not query_params: return None
        if not query_params.has_key('ecm'): return None

        ecm = query_params['ecm'][0]

        orderstatus = cls.get_splited_item(ecm, 12, '`', True)
        if orderstatus in ('2', '3'):
            return cls.ENUM_PAID_PAGE

        orderid = cls.get_splited_item(ecm, 2, '`')
        ordermoney = cls.get_splited_item(ecm, 3, '`')
        if orderid and ordermoney:
            return cls.ENUM_ORDER_PAGE
        else:
            return None

    @classmethod
    def get_query_param_value(cls, query_params, key):
        """
        Args:
            query_params: A dict returned form urlparse.parse_qs().
                E.g., { 'ecm': ['````````````'] }

        Returns: query_params[key][0] or None if there is any exception.
        """

        try:
            return query_params[key][0]
        except:
            return None

    @classmethod
    def conversionpage_or_conversionbutton(cls, query_params):
        """
        Args:
            query_params: A dict returned form urlparse.parse_qs().
                E.g., { 'ecm': ['````````````'] }

        Returns:
            ENUM_CONVERSION_PAGE or
            ENUM_CONVERSION_BUTTON or
            None
        """

        if 'ec' in query_params:
            if '1' in query_params['ec'] or '$conversion' in query_params['ec']:
                pass
            else:
                return None
        else:
            return None

        ea = cls.get_query_param_value(query_params, 'ea')  # event action
        el = cls.get_query_param_value(query_params, 'el')  # event label
        ev = cls.get_query_param_value(query_params, 'ev')  # event value
        if not (ea or el or ev): return None

        ctd = cls.get_query_param_value(query_params, 'ctd')
        if ctd:
            ctd_key_values = cls.parse_qs(ctd, ';', '|')
            if (('convpage' in ctd_key_values) and
                ('1' in ctd_key_values['convpage'])):
                return cls.ENUM_CONVERSION_PAGE

        return cls.ENUM_CONVERSION_BUTTON

    @classmethod
    def get_page_kinds(cls, rawlog):
        """Get page kinds.
        Args:
            rawlog: A log of kind RawLog.

        Returns:
            A tuple contains the page-kinds of input rawlog;
            E.g., ('sitepage', ...)

        Raises:
            None
        """

        try:
            url = rawlog.request_url
            parsed_url = urlparse.urlparse(url)
            query_params = urlparse.parse_qs(parsed_url.query)
            if not query_params: return ()
        except:
            return ()

        site_code = cls.get_site_code(query_params=query_params)
        if not site_code: return ()  # empty tuple

        # ENUM_SKU_PAGE = 1
        pids = cls.get_product_codes(url)
        if pids: return (cls.PAGE_TYPES[cls.ENUM_SKU_PAGE], )

        # ENUM_CART_PAGE = 2
        pids_in_cart = cls.get_skuid_list_in_shopcart(url)
        if pids_in_cart: return (cls.PAGE_TYPES[cls.ENUM_CART_PAGE], )

        # ENUM_ORDER_PAGE = 3  &  ENUM_PAID_PAGE = 4
        r = cls.orderpage_or_paidpage(query_params=query_params)
        if r in (cls.ENUM_ORDER_PAGE, cls.ENUM_PAID_PAGE):
            return (cls.PAGE_TYPES[r], )

        # ENUM_CONVERSION_PAGE = 5  # conversionpage

        # ENUM_CONVERSION_BUTTON = 6  # conversionbutton

        # ENUM_EVENT_PAGE = 7  # eventpage

        # ENUM_EVENT_BUTTON = 8  # eventbutton

        # ENUM_SITE_PAGE = 0  # sitepage
        return (cls.PAGE_TYPES[cls.ENUM_SITE_PAGE], )


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

    query_params = {
        'ao': ['234']
    }
    if IdiggerUtil.get_site_code(query_params=query_params) != '234':
        assert False, 'IdiggerUtil.get_site_code(): Unit test failed: #2'

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

def _unit_test_get_skuid_list_in_shopcart():
    test_url_no_ecm = "http://idigger.allyes.com/main/adftrack?db=mso&v=3.0&r=802029047&hn=www.yougou.com&lt=i&plf=Linux&cs=UTF-8&ul=en-us&bt=Chrome&bs=1366x768,24-bit,11.8%20r800,1&pt=%E3%80%90DickiesDickies%20031581%20%E6%B7%B1%E6%B5%B7%E5%86%9B%E8%93%9D%E6%9D%A1%E7%BA%B9%E3%80%91Dickies%E5%B8%9D%E5%AE%A2%20%E7%94%B7%E5%A3%AB%E6%B7%B1%E6%B5%B7%E5%86%9B%E8%93%9D%E6%9D%A1%E7%BA%B9%E7%89%9B%E4%BB%94%E8%A3%A4%20031581&rf=http%3A%2F%2Fwww.yougou.com%2Ff-dickies-1LTFA-0-0.html&pu=%2Fc-dickies%2Fsku-031581-99919909.shtml&ncf=0&tag=&ao=T-000436-01&tsuid=&tsoid=&tst=&tkv=&ayf=&cct=1382351003&sc=11&nv=1"

    # 0, no ecm
    skuid_list = IdiggerUtil.get_skuid_list_in_shopcart(test_url_no_ecm)
    if skuid_list:
        assert False, 'get_skuid_list_in_shopcart(): Unit test failed: #0'

    # 1,
    ecm_without_shopcart = '&ecm=%60%60%60%60%60%6099919909%60%60%60%60%60%60%60'
    skuid_list = IdiggerUtil.get_skuid_list_in_shopcart(
        test_url_no_ecm + ecm_without_shopcart)
    if skuid_list:
        assert False, 'get_skuid_list_in_shopcart(): Unit test failed: #1'

    # 2,
    ecm = '&ecm=%60%60%60%60%60%60%60%6099919909%60%60%60%60%60'
    skuid_list = IdiggerUtil.get_skuid_list_in_shopcart(test_url_no_ecm + ecm)
    if skuid_list and len(skuid_list) == 1 and skuid_list[0] == '99919909':
        pass
    else:
        assert False, 'get_skuid_list_in_shopcart(): Unit test failed: #2'

    # 3,
    ecm = '&ecm=%60%60%60%60%60%60%60%60%257Cp9928%60%60%60%60%60'
    skuid_list = IdiggerUtil.get_skuid_list_in_shopcart(test_url_no_ecm + ecm)
    if skuid_list and len(skuid_list) == 1 and skuid_list[0] == 'p9928':
        pass
    else:
        assert False, 'get_skuid_list_in_shopcart(): Unit test failed: #3'

    # 4,
    ecm = '&ecm=%60%60%60%60%60%60%60%60%257Cp9928%257C123%257C%60%60%60%60%60'
    skuid_list = IdiggerUtil.get_skuid_list_in_shopcart(test_url_no_ecm + ecm)
    if (skuid_list and len(skuid_list) == 2 and
        skuid_list[0] == 'p9928' and skuid_list[1] == '123'):
        pass
    else:
        assert False, 'get_skuid_list_in_shopcart(): Unit test failed: #4'

    # 5,
    ecm = '&ecm=%60%60%60%60%60%60%60%60%257Cp9928%257Cabc^de^123%257C%60%60%60%60%60'
    skuid_list = IdiggerUtil.get_skuid_list_in_shopcart(test_url_no_ecm + ecm)
    if (skuid_list and len(skuid_list) == 2 and
        skuid_list[0] == 'p9928' and skuid_list[1] == '123'):
        pass
    else:
        assert False, 'get_skuid_list_in_shopcart(): Unit test failed: #5'

    # 6, 1@a^b^2|c^d^33|
    ecm = ('&ecm=%60%60%60%60%60%60%60%60' +
           urllib.quote(urllib.quote('1@a^b^2|c^d^33|')) +
           '%60%60%60%60%60')
    skuid_list = IdiggerUtil.get_skuid_list_in_shopcart(test_url_no_ecm + ecm)
    if (skuid_list and len(skuid_list) == 2 and
        skuid_list[0] == '2' and skuid_list[1] == '33'):
        pass
    else:
        assert False, 'get_skuid_list_in_shopcart(): Unit test failed: #6'

    # 7,
    ecm = '&ecm=%60%60%60%60%60%60%60%60%257Cp11744%257Cp16730%257Cp7521%257Cp8115%60%60%60%60%60'
    skuid_list = IdiggerUtil.get_skuid_list_in_shopcart(test_url_no_ecm + ecm)
    if (skuid_list and len(skuid_list) == 4 and
        skuid_list[0] == 'p11744' and skuid_list[1] == 'p16730' and
        skuid_list[2] == 'p7521' and skuid_list[3] == 'p8115'):
        pass
    else:
        assert False, 'get_skuid_list_in_shopcart(): Unit test failed: #7'

def _unit_test_get_splited_item():
    # 0
    src_str = 'a b c\td\ne\t\n f'
    assert (IdiggerUtil.get_splited_item(src_str, 0) == 'a' and
            IdiggerUtil.get_splited_item(src_str, 1) == 'b' and
            IdiggerUtil.get_splited_item(src_str, 2) == 'c' and
            IdiggerUtil.get_splited_item(src_str, 3) == 'd' and
            IdiggerUtil.get_splited_item(src_str, 4) == 'e' and
            IdiggerUtil.get_splited_item(src_str, 5) == 'f' and
            IdiggerUtil.get_splited_item(src_str, 6) == None and
            IdiggerUtil.get_splited_item(src_str, -1) == 'f')

    # 1
    src_str = "`a%7Cb`c%7Cd`"
    assert (IdiggerUtil.get_splited_item(src_str, 0, '`') == '' and
            IdiggerUtil.get_splited_item(src_str, 1, '`') == 'a%7Cb' and
            IdiggerUtil.get_splited_item(src_str, 2, '`') == 'c%7Cd' and
            IdiggerUtil.get_splited_item(src_str, 3, '`') == '' and
            IdiggerUtil.get_splited_item(src_str, 4, '`') == None)

    # 2
    src_str = "`a%7Cb`c%7Cd`"
    assert (IdiggerUtil.get_splited_item(src_str, 0, '`', True) == '' and
            IdiggerUtil.get_splited_item(src_str, 1, '`', True) == 'a|b' and
            IdiggerUtil.get_splited_item(src_str, 2, '`', True) == 'c|d' and
            IdiggerUtil.get_splited_item(src_str, 3, '`', True) == '' and
            IdiggerUtil.get_splited_item(src_str, 4, '`', True) == None)

    # 3
    src_str = 'abcdefg'
    assert (IdiggerUtil.get_splited_item(src_str, 0, '|') == 'abcdefg' and
            IdiggerUtil.get_splited_item(src_str, 1, '|') == None)

def _unit_test_orderpage_or_paidpage():
    # 0
    q = {
         'ecm': ['````````````1`'],
    }
    assert IdiggerUtil.orderpage_or_paidpage(q) == None

    # 1
    q = {
         'ecm': ['````````````2`'],
    }
    assert IdiggerUtil.orderpage_or_paidpage(q) == IdiggerUtil.ENUM_PAID_PAGE

    # 2
    q = {
         'ecm': ['````````````3`'],
    }
    assert IdiggerUtil.orderpage_or_paidpage(q) == IdiggerUtil.ENUM_PAID_PAGE

    # 3
    q = {
         'ecm': ['```````'],
    }
    assert IdiggerUtil.orderpage_or_paidpage(q) == None

    # 4
    q = {
         'ecmx': ['````````````3`'],
    }
    assert IdiggerUtil.orderpage_or_paidpage(q) == None

    # 5
    q = {
         'ecm': ["4ec3bcaba90844cc86f0ce4f6badee26``A641231151522`199.00`99967948````````1`"],
    }
    assert IdiggerUtil.orderpage_or_paidpage(q) == IdiggerUtil.ENUM_ORDER_PAGE

    # 6
    q = {
         'ecm': ["4ec3bcaba90844cc86f0ce4f6badee26``A641231151522`199.00`99967948````````2`"],
    }
    assert IdiggerUtil.orderpage_or_paidpage(q) == IdiggerUtil.ENUM_PAID_PAGE

    # 7
    q = {
         'ecm': ["4ec3bcaba90844cc86f0ce4f6badee26``A641231151522`199.00`99967948````````3`"],
    }
    assert IdiggerUtil.orderpage_or_paidpage(q) == IdiggerUtil.ENUM_PAID_PAGE

    # 8
    q = {
         'ecm': ["4ec3bcaba90844cc86f0ce4f6badee26``A641231151522``99967948````````1`"],
    }
    assert IdiggerUtil.orderpage_or_paidpage(q) == None

    # 9
    q = {
         'ecm': ["4ec3bcaba90844cc86f0ce4f6badee26```199.00`99967948````````1`"],
    }
    assert IdiggerUtil.orderpage_or_paidpage(q) == None

def _unit_test_parse_qs():
    # 0
    qs = 'k1=v1&k2=v2'
    r = IdiggerUtil.parse_qs(qs)
    assert r['k1'] == ['v1'] and r['k2'] == ['v2']

    # 1
    qs = 'k1|v1;k2|v2'
    r = IdiggerUtil.parse_qs(qs, ';', '|')
    assert r['k1'] == ['v1'] and r['k2'] == ['v2']

    # 2
    qs = 'k1|v1;k2|v2;k1|v1.1;k2|v2.1'
    r = IdiggerUtil.parse_qs(qs, ';', '|')
    assert r['k1'] == ['v1', 'v1.1'] and r['k2'] == ['v2', 'v2.1']

    # 3
    qs = 'k1|v1;k2|v2;k3|'
    r = IdiggerUtil.parse_qs(qs, ';', '|')
    assert r['k1'] == ['v1'] and r['k2'] == ['v2'] and ('k3' not in r)

    # 4
    qs = 'k1|v1;k2|v2;k3|;k4'
    r = IdiggerUtil.parse_qs(qs, ';', '|', True)
    assert (r['k1'] == ['v1'] and r['k2'] == ['v2'] and r['k3'] == [''] and
            r['k4'] == [''])

    # 5
    qs = '|v1;;|'
    r = IdiggerUtil.parse_qs(qs, ';', '|', True)
    assert r[''] == ['v1', '']

def _unit_test_conversionpage_or_conversionbutton():
    # 0
    q = {
         'ec': ['1'],
         'ea': ['xxx'],
         'ctd': ['convpage|1;convtype|xxx'],
    }
    assert (IdiggerUtil.conversionpage_or_conversionbutton(q) ==
            IdiggerUtil.ENUM_CONVERSION_PAGE)

    # 1
    q = {
         'ec': ['2', '$conversion'],
         'ea': ['xxx'],
         'ctd': ['convpage|1;convtype|xxx'],
    }
    assert (IdiggerUtil.conversionpage_or_conversionbutton(q) ==
            IdiggerUtil.ENUM_CONVERSION_PAGE)

    # 2
    q = {
         'ec': ['2', '$conversion'],
         'ea': ['xxx'],
         'ctd': ['convpage|2;convtype|xxx'],
    }
    assert (IdiggerUtil.conversionpage_or_conversionbutton(q) ==
            IdiggerUtil.ENUM_CONVERSION_BUTTON)

    # 3
    q = {
         'ec': ['1'],
         'ctd': ['convpage|1;convtype|xxx'],
    }
    assert IdiggerUtil.conversionpage_or_conversionbutton(q) == None

    # 4
    q = {
         'ec': ['2', '$conversion'],
         'ea': ['xxx'],
         'el': ['xxx'],
         'ev': ['xxx'],
         'ctd': ['convpage|2;convtype|xxx;convpage|1'],
    }
    assert (IdiggerUtil.conversionpage_or_conversionbutton(q) ==
            IdiggerUtil.ENUM_CONVERSION_PAGE)

def _unit_test():
    print '*** Idigger Unit Test Begin'

    _unit_test_get_http_query_section()
    _unit_test_get_site_code()
    _unit_test_get_page_url()
    _unit_test_get_product_codes()
    _unit_test_get_skuid_list_in_shopcart()
    _unit_test_get_splited_item()
    _unit_test_orderpage_or_paidpage()
    _unit_test_parse_qs()
    _unit_test_conversionpage_or_conversionbutton()

    print '*** Idigger Unit Test End'

_unit_test()
