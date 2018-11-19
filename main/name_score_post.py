#!usr/bin/env python
# coding:utf-8

import urllib
import urllib2
from bs4 import BeautifulSoup
import re
import convertZh
import create_name
import xlwt
import datetime
import threadpool
import os
import threading


url = "https://www.meimingteng.com/Naming/Default.aspx?Tag=4"
result_file = None
count = 1

form = {
    "__EVENTTARGET": "ctl00$ContentPlaceHolder1$InputBasicInfo1$btNext",
    "__EVENTARGUMENT": "",
    "__VIEWSTATE": "/wEPDwULLTEyNjU5OTUwOTBkGAEFHl9fQ29udHJvbHNSZXF1aXJlUG9zdEJhY2tLZXlfXxYeBTtjdGwwMCRDb250ZW50UGxhY2VIb2xkZXIxJElucHV0QmFzaWNJbmZvMSRyYlNwZWNpZnlCaXJ0aGRheQU9Y3RsMDAkQ29udGVudFBsYWNlSG9sZGVyMSRJbnB1dEJhc2ljSW5mbzEkcmJTcGVjaWZ5TGluQ2hhblFpbgU9Y3RsMDAkQ29udGVudFBsYWNlSG9sZGVyMSRJbnB1dEJhc2ljSW5mbzEkcmJTcGVjaWZ5TGluQ2hhblFpbgU+Y3RsMDAkQ29udGVudFBsYWNlSG9sZGVyMSRJbnB1dEJhc2ljSW5mbzEkcmJOb3RTcGVjaWZ5QmlydGhkYXkFPmN0bDAwJENvbnRlbnRQbGFjZUhvbGRlcjEkSW5wdXRCYXNpY0luZm8xJHJiTm90U3BlY2lmeUJpcnRoZGF5BTFjdGwwMCRDb250ZW50UGxhY2VIb2xkZXIxJElucHV0QmFzaWNJbmZvMSRyYlNvbGFyBTFjdGwwMCRDb250ZW50UGxhY2VIb2xkZXIxJElucHV0QmFzaWNJbmZvMSRyYkx1bmFyBTFjdGwwMCRDb250ZW50UGxhY2VIb2xkZXIxJElucHV0QmFzaWNJbmZvMSRyYkx1bmFyBTdjdGwwMCRDb250ZW50UGxhY2VIb2xkZXIxJElucHV0QmFzaWNJbmZvMSRjYklzTGVhcE1vbnRoBTFjdGwwMCRDb250ZW50UGxhY2VIb2xkZXIxJElucHV0QmFzaWNJbmZvMSRsYnROb25lBTFjdGwwMCRDb250ZW50UGxhY2VIb2xkZXIxJElucHV0QmFzaWNJbmZvMSRsYnROb25lBTJjdGwwMCRDb250ZW50UGxhY2VIb2xkZXIxJElucHV0QmFzaWNJbmZvMSRyYnRMdW5ZdQUyY3RsMDAkQ29udGVudFBsYWNlSG9sZGVyMSRJbnB1dEJhc2ljSW5mbzEkcmJ0THVuWXUFNGN0bDAwJENvbnRlbnRQbGFjZUhvbGRlcjEkSW5wdXRCYXNpY0luZm8xJHJidFNoaUppbmcFNGN0bDAwJENvbnRlbnRQbGFjZUhvbGRlcjEkSW5wdXRCYXNpY0luZm8xJHJidFNoaUppbmcFMWN0bDAwJENvbnRlbnRQbGFjZUhvbGRlcjEkSW5wdXRCYXNpY0luZm8xJHJidFBvZW0FMWN0bDAwJENvbnRlbnRQbGFjZUhvbGRlcjEkSW5wdXRCYXNpY0luZm8xJHJidFBvZW0FMmN0bDAwJENvbnRlbnRQbGFjZUhvbGRlcjEkSW5wdXRCYXNpY0luZm8xJHJidElkaW9tBTJjdGwwMCRDb250ZW50UGxhY2VIb2xkZXIxJElucHV0QmFzaWNJbmZvMSRyYnRJZGlvbQU6Y3RsMDAkQ29udGVudFBsYWNlSG9sZGVyMSRJbnB1dEJhc2ljSW5mbzEkY2JsUGVyc29uYWxpdHkkMAU6Y3RsMDAkQ29udGVudFBsYWNlSG9sZGVyMSRJbnB1dEJhc2ljSW5mbzEkY2JsUGVyc29uYWxpdHkkMQU6Y3RsMDAkQ29udGVudFBsYWNlSG9sZGVyMSRJbnB1dEJhc2ljSW5mbzEkY2JsUGVyc29uYWxpdHkkMgU6Y3RsMDAkQ29udGVudFBsYWNlSG9sZGVyMSRJbnB1dEJhc2ljSW5mbzEkY2JsUGVyc29uYWxpdHkkMwU6Y3RsMDAkQ29udGVudFBsYWNlSG9sZGVyMSRJbnB1dEJhc2ljSW5mbzEkY2JsUGVyc29uYWxpdHkkNAU6Y3RsMDAkQ29udGVudFBsYWNlSG9sZGVyMSRJbnB1dEJhc2ljSW5mbzEkY2JsUGVyc29uYWxpdHkkNQU6Y3RsMDAkQ29udGVudFBsYWNlSG9sZGVyMSRJbnB1dEJhc2ljSW5mbzEkY2JsUGVyc29uYWxpdHkkNgU6Y3RsMDAkQ29udGVudFBsYWNlSG9sZGVyMSRJbnB1dEJhc2ljSW5mbzEkY2JsUGVyc29uYWxpdHkkNwU6Y3RsMDAkQ29udGVudFBsYWNlSG9sZGVyMSRJbnB1dEJhc2ljSW5mbzEkY2JsUGVyc29uYWxpdHkkOAU6Y3RsMDAkQ29udGVudFBsYWNlSG9sZGVyMSRJbnB1dEJhc2ljSW5mbzEkY2JsUGVyc29uYWxpdHkkOQU6Y3RsMDAkQ29udGVudFBsYWNlSG9sZGVyMSRJbnB1dEJhc2ljSW5mbzEkY2JsUGVyc29uYWxpdHkkOc+RBppac3/CXaY8AJwjzwaxBvxk",
    "__VIEWSTATEGENERATOR": "9F5AD4C7",
    "__EVENTVALIDATION": "/wEWvAICkof8EwLatoz7BAK19uvYAgKlkY7lBAKBmOYKAoCY5goCqcPP0AcCqMPP0AcCq8PP0AcCnd3BDAKVuaPyDgKV99WYCAL9kPD0BgKmsv/0AQKL2c+pBQKMlpPbCAKMloemAQKMluuBCgKMlt/sAgKMlsO3CwKMlreTBAKMlpv+DAKMls+WCgKMlrPyAgLhr8HqBQLhr7W2DgLhr5mRBwLhr438DwLhr/HHCALhr+WiAQLhr8mNCgLhr73pAgLhr+EBAuGv1ewIAvq448ULAvq416AEAvq4u4wNAvq4r9cFAvq4k7IOAvq4h50HAvq46/gPAvq438MIAvq4g/wFAvq498cOAt/RhLABAt/R6JsKAt/R3OYCAt/RwMELAt/RtK0EAt/RmIgNAt/RjNMFAt/R8L4OAt/RpNcLAt/RiLIEArDrpqsHArDrivYPArDr/tEIArDr4rwBArDr1ocKArDruuMCArDrrs4LArDrkqkEArDrxsEBArDrqq0KApWEuIYNApWErOEFApWEkMwOApWEhJcHApWE6PIPApWE3N0IApWEwLgBApWEtIQKApWE2LwHApWEzAcC7p3a8AIC7p3O2wsC7p2ypwQC7p2mgg0C7p2K7QUC7p3+yA4C7p3ikwcC7p3W/g8C7p36lw0C7p3u8gUCw7b86wgCw7bgtgECw7bUkQoCw7a4/QICw7as2AsCw7aQowQCw7aEjg0Cw7bo6QUCw7acggMCw7aA7QsC9Ny8qgEC9Nyg9QkC9NyU0AIC9Nz4uwsC9NzshgQC9NzQ4QwC9NzEzAUC9NyoqA4C9NzcwAsC9NzAqwQCyfXehAcCyfXC7w8CyfW2ywgCyfWalgECyfWO8QkCyfXy3AICyfXmpwsCyfXKggQCyfX+uwECyfXihgoCjZaL8A8CjZb/2wgCjZbjpgECjZbXgQoCjZa77QICjZavyAsCjZaTkwQCjZaH/gwCjZarlwoCjZaf8gIC5q+t6wUC5q+Rtg4C5q+FkQcC5q/p/A8C5q/dxwgC5q/BogEC5q+1jgoC5q+Z6QIC5q/NAQLmr7HtCAL7uM/FCwL7uLOhBAL7uKeMDQLyr4XtDALzr4XtDALwr4XtDALxr4XtDAL2r4XtDAL3r4XtDAL0r4XtDALlr4XtDALqr4XtDALyr8XuDALyr8nuDALyr83uDAKVwsetDgKUwsetDgKXwsetDgKWwsetDgKRwsetDgKQwsetDgKTwsetDgKCwsetDgKNwsetDgKVwoeuDgKVwouuDgKVwo+uDgKVwrOuDgKVwreuDgKVwruuDgKVwr+uDgKVwqOuDgKVwuetDgKVwuutDgKUwoeuDgKUwouuDgKUwo+uDgKUwrOuDgKUwreuDgKUwruuDgKUwr+uDgKUwqOuDgKUwuetDgKUwuutDgKXwoeuDgKXwouuDgKArtmFCAKTrpWGCAKMrpWGCAKNrpWGCAKOrpWGCAKPrpWGCAKIrpWGCAKJrpWGCAKKrpWGCAKbrpWGCAKUrpWGCAKMrtWFCAKMrtmFCAKMrt2FCAKMruGFCAKMruWFCAKMrumFCAKMru2FCAKMrvGFCAKMrrWGCAKMrrmGCAKNrtWFCAKNrtmFCAKNrt2FCAKNruGFCALCsOLeDALdsOLeDALcsOLeDALfsOLeDALesOLeDALZsOLeDALYsOLeDALbsOLeDALKsOLeDALFsOLeDALdsKLdDALdsK7dDALdsKrdDALdsJbdDALdsJLdDALdsJ7dDALdsJrdDALdsIbdDALdsMLeDALdsM7eDALcsKLdDALcsK7dDALcsKrdDALcsJbdDALcsJLdDALcsJ7dDALcsJrdDALcsIbdDALcsMLeDALcsM7eDALfsKLdDALfsK7dDALfsKrdDALfsJbdDALfsJLdDALfsJ7dDALfsJrdDALfsIbdDALfsMLeDALfsM7eDALesKLdDALesK7dDALesKrdDALesJbdDALesJLdDALesJ7dDALesJrdDALesIbdDALesMLeDALesM7eDALZsKLdDALZsK7dDALZsKrdDALZsJbdDALZsJLdDALZsJ7dDALZsJrdDALZsIbdDALZsMLeDALZsM7eDALq3rerBALCuMjbDwKi2vn0BQK1gMHLAgKy5bvtBQK236G8AQLV9/naAgKgqtmeCgLVnOXeBwL62evxBgL22aPyBgL32aPyBgL02aPyBgL12aPyBgLy2aPyBgLz2aPyBgLw2aPyBgLh2aPyBgLu2aPyBgL22ePxBgL22e/xBgL22evxBgL22dfxBgL22dPxBgL22dvxBgL22cfxBgL62e/xBgL/l8bNAwL/l8rNAwL/l77NAwL/l8LNAwL/l9bNAwL/l9rNAwL/l87NAwL/l9LNAwL/l6bNAwL/l6rNAwL9lKKdCgKWk7qbCgL1g6aRDwLXw/fkCALvyL/mDALev/OZDgLL5ZPJCAKi/N2EAQKD5eu3CwKgl5eyCgKeoZaXAwKd8qmzBALwr6/EDwLS6rKCB0qaGIvXNr+vYlP4j0BeDDn86j0L",
    "ctl00$ContentPlaceHolder1$InputBasicInfo1$tbXing": "找",
    "ctl00$ContentPlaceHolder1$InputBasicInfo1$tbMingWords": "东西",
    "ctl00$ContentPlaceHolder1$InputBasicInfo1$ddlGenders": "1",
    "ctl00$ContentPlaceHolder1$InputBasicInfo1$SPECIFY_BIRHDAY": "rbSpecifyBirthday",
    "ctl00$ContentPlaceHolder1$InputBasicInfo1$CalendarType": "rbSolar",
    "ctl00$ContentPlaceHolder1$InputBasicInfo1$ddlYear": "2018",
    "ctl00$ContentPlaceHolder1$InputBasicInfo1$ddlMonth": "10",
    "ctl00$ContentPlaceHolder1$InputBasicInfo1$ddlDay": "24",
    "ctl00$ContentPlaceHolder1$InputBasicInfo1$ddlHour": "17",
    "ctl00$ContentPlaceHolder1$InputBasicInfo1$ddlMinute": "47",
    "ctl00$ContentPlaceHolder1$InputBasicInfo1$tbCountry": "中国",
    "ctl00$ContentPlaceHolder1$InputBasicInfo1$tbProvince": "",
    "ctl00$ContentPlaceHolder1$InputBasicInfo1$tbCity": "",
    "ctl00$ContentPlaceHolder1$InputBasicInfo1$tbOtherHopes": "",
    "ctl00$ContentPlaceHolder1$InputBasicInfo1$ddlCareer": "-2",
    "ctl00$ContentPlaceHolder1$InputBasicInfo1$tbFather": "",
    "ctl00$ContentPlaceHolder1$InputBasicInfo1$tbMother": "",
    "ctl00$ContentPlaceHolder1$InputBasicInfo1$tbAvoidWords": "",
    "ctl00$ContentPlaceHolder1$InputBasicInfo1$tbAvoidSimpParts": "",
    "ctl00$ContentPlaceHolder1$InputBasicInfo1$LoginAnywhere1$tbUserName": "",
    "ctl00$ContentPlaceHolder1$InputBasicInfo1$LoginAnywhere1$tbPwd": "",
    "ctl00$ContentPlaceHolder1$InputBasicInfo1$LoginAnywhere1$tbVCode": "",
    "ctl00$ContentPlaceHolder1$InputBasicInfo1$LoginAnywhere1$loginParam": "2",
}
header = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Content-Length': '6727',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Cookie': 'Params=%26Xing%3d%e9%83%ad%26Gender%3d1%26Year%3d1990%26Month%3d2%26Day%3d8%26Hour%3d21%26Minute%3d30%26IsSolarCalendar%3d0%26IsLeapMonth%3d0%26NameType%3d2%26ReiterativeLocution%3d0%26Location%3d%e4%b8%ad%e5%9b%bd++%26Career%3d-2%26Personality%3d%26Father%3d%26Mother%3d%26SpecifiedName%3d%26SpecifiedNameIndex%3d0%26OtherHopes%3d%26AvoidWords%3d%26AvoidSimpParts%3d%26SpecifiedMing1SimpParts%3d%26SpecifiedMing2SimpParts%3d%26SpecifiedMing1Stroke%3d%26SpecifiedMing2Stroke%3d%26Tag%3d4%7c2%26LinChanQi%3dFalse%26NamingByCategoryCategoryID%3d-1%26SM1S%3d%26SM2S%3d%26SM1T%3d%26SM2T%3d%26SM1M%3d%26SM2M%3d%26RN%3d%26SpecifiedMing1Spell%3d%26SpecifiedMing2Spell%3d%26SM1Y%3d%26SM2Y%3d%26FA%3d%e6%99%9a%e4%b8%8a+%e8%8a%b3%e6%98%a5%e8%8a%82+%e6%8f%92%e8%8a%b1%e8%8a%82+++%e6%98%a5%e5%ad%a3+%e7%99%bd%e6%b1%82%e6%81%a9%e8%af%9e%e8%be%b0%e6%97%a5+%e4%ba%8c%e6%9c%88%26LOCATION_COUNTY%3d%e4%b8%ad%e5%9b%bd%26LOCATION_PROVINCE%3d%26LOCATION_CITY%3d%26MING_WORDS%3d%e8%89%ba%e5%b8%86; ASP.NET_SessionId=2cjtqg45s20f1b555tnr5aal; mmtsuser=1; ckcookie=chcookie; HELLO_USER=1; Hm_lvt_637e96da78d1c6c8f8a218c811dea5fb=1541483303; Hm_lpvt_637e96da78d1c6c8f8a218c811dea5fb=1541489644',
    'Host': 'www.meimingteng.com',
    'Origin': 'https://www.meimingteng.com',
    'Referer': 'https://www.meimingteng.com/Naming/Default.aspx?Tag=4',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'
}


def get_score_of(label, node, soup):
    culture = node.find("span", string=label)
    if culture:
        culture_score = culture.next_sibling.b.get_text()
        print label + ": " + culture_score.encode('utf-8')
        return culture_score.encode('utf-8')
    else:
        culture_score = get_score_from_entirity(label, soup)
        if not culture_score:
            print label + ": " + "66"
            return "66"
        return culture_score


def get_score_from_entirity(label, soup):
    has_found = None
    for node in soup.find_all("span", string=label):
        if node.next_sibling and node.next_sibling.b:
            has_found = node.next_sibling.b.get_text().encode('utf-8')
            print(label + ": " + node.next_sibling.b.get_text().encode('utf-8'))
    return has_found


def compute_score_of_name(name):
    form['ctl00$ContentPlaceHolder1$InputBasicInfo1$tbMingWords'] = name
    try:
        paramsData = urllib.urlencode(form)
        request = urllib2.Request(url, paramsData)
        # print("HTTP GET")
        response = urllib2.urlopen(request, timeout=20)
        # print("Respone Successfully")
        content = response.read()
    except Exception as e:
        print("Error: " + str(e))
        return None

    soup = BeautifulSoup(content, 'html.parser')

    # print(soup)
    correct_response = False
    for node in soup.find_all("table", class_="naming2"):
        node_content = node.get_text()
        if u"评分：" in node_content:
            correct_response = True
            score_culture = get_score_of("文化印象", node, soup)
            score_bazi = get_score_of("五行八字", node, soup)
            score_shengxiao = get_score_of("生　　肖", node, soup)
            score_wuge = get_score_of("五格数理", node, soup)
            name_score = {
                            '文化印象': score_culture,
                            '五行八字': score_bazi,
                            '生　　肖': score_shengxiao,
                            '五格数理': score_wuge
                        }
            return name_score
    # TODO: 不能处理的名字
    if not correct_response:
        return None


def create_excel(result_file):
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Baby_Names')
    ws.write(0, 0, '姓名')
    ws.write(0, 1, '文化印象')
    ws.write(0, 2, '五行八字')
    ws.write(0, 3, '生　　肖')
    ws.write(0, 4, '五格数理')
    ws.write(0, 5, '来   源')
    row = 1
    with open(result_file, 'r') as results:
        for line in results:
            subs = line.split()
            if len(subs) > 5:
                ws.write(row, 0, subs[0])
                ws.write(row, 1, subs[1])
                ws.write(row, 2, subs[2])
                ws.write(row, 3, subs[3])
                ws.write(row, 4, subs[4])
                ws.write(row, 5, subs[5] + ' ' + subs[6])
                row += 1
        # ws.write(count, 0, n)
        # ws.write(count, 1, name_score['文化印象'])
        # ws.write(count, 2, name_score['五行八字'])
        # ws.write(count, 3, name_score['生　　肖'])
        # ws.write(count, 4, name_score['五格数理'])
    wb_name = result_file.replace(".txt", ".xls")
    if os.path.isfile(wb_name):
        os.remove(wb_name)
    wb.save(wb_name)


lock = threading.Lock()
def write_names_score(name_score, line):
    global result_file
    if not name_score:
        return
    lock.acquire(5)
    subs = line.split()
    new_name_with_source = ""
    if len(subs) > 2:
        with open(result_file, 'a') as result:
            name = subs[0]
            source = subs[1] + ' ' + subs[2]
            new_name_with_source = name + ' '
            for item in name_score:
                score = name_score[item]
                # all_score = score + ' '
                new_name_with_source = new_name_with_source + ' ' + score
            new_name_with_source = new_name_with_source + ' ' + source
            result.write(new_name_with_source + '\n')
    lock.release()

pool = threadpool.ThreadPool(3)



def core_func(line):
    global count
    global result_file
    # global pool
    # if count >= 10:
    #     pool.dismissWorkers(1)
    #     return
    ns = line.split()
    n = line.split()[0]
    new_source = ""
    if n.startswith('来源'):
        new_source = n
        lock.acquire(5)
        with open(result_file, 'a') as result:
            result.write(new_source + '\n')
        lock.release()
    if not n.startswith('来源') and len(n.strip()) != 0:
        name_score = compute_score_of_name(n)
        write_names_score(name_score, line)
        if name_score:
            count += 1


def create_name_excel_from(file_path):
    global result_file
    t_start = datetime.datetime.now()
    target_path = create_name.find_target_names(file_path)
    file_path = create_name.attach_pre_name_to('withSrc_postive_', target_path)
    dir_name, base_name = os.path.split(file_path)
    result_file = dir_name + '/result_' + base_name

    name_list = []
    if os.path.exists(result_file):
        os.remove(result_file)
    with open(file_path, 'r') as names:
        for n in names:
            name_list.append(n)
    reqs = threadpool.makeRequests(core_func, name_list)
    [pool.putRequest(req) for req in reqs]
    pool.wait()

    t_end = datetime.datetime.now()
    create_excel(result_file)
    print "cost %s  to create names from %s" % ((t_end - t_start), os.path.split(result_file)[1])

if __name__ == '__main__':
    create_name_excel_from(convertZh.tang_300_peom)



