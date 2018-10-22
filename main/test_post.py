#!usr/bin/env python
# coding:GB18030

import urllib
import urllib2
from bs4 import BeautifulSoup


url = "http://life.httpcn.com/xingming.asp"

params = {}

# 日期类型，0表示公历，1表示农历
params['data_type'] = "0"
params['year'] = "%s" % str(1985)
params['month'] = "%s" % str(12)
params['day'] = "%s" % str(24)
params['hour'] = "%s" % str(22)
params['minute'] = "%s" % str(23)
params['pid'] = "%s" % str("北京")
params['cid'] = "%s" % str("海淀")
# 喜用五行，0表示自动分析，1表示自定喜用神
params['wxxy'] = "0"
params['xing'] = "%s" % "任"
params['ming'] = "志强"
# 表示女，1表示男
params['sex'] = "1"
params['act'] = "submit"
params['isbz'] = "1"

paramsData = urllib.urlencode(params)
request = urllib2.Request(url, paramsData)
response = urllib2.urlopen(request)
content = response.read()

soup = BeautifulSoup(content, 'html.parser')
print(soup)




