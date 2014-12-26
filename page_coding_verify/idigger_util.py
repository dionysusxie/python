#!/usr/bin/env python -u

import urlparse


class IdiggerUtil(object):

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

def _unit_test():
    _unit_test_get_http_query_section()
    _unit_test_get_site_code()

_unit_test()
