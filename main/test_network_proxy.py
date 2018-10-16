#!/usr/bin/env python
# coding=utf-8

import urllib
import  urllib2
import  re


# # The proxy address and port:
# proxy_info = {'host': 'dev-proxy.oa.com', 'port': 8080}
#
# # We create a handler for the proxy
# proxy_support = urllib2.ProxyHandler({"http": "http://%(host)s:%(port)d" % proxy_info})
#
# # We create an opener which uses this handler:
# opener = urllib2.build_opener(proxy_support)
#
# # Then we install this opener as the default opener for urllib2:
# urllib2.install_opener(opener)

url = "http://tieba.baidu.com/p/2460150866"
request = urllib2.Request(url)
page = urllib2.urlopen(url)
html = page.read()
print html