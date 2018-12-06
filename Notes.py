


__notes__ = \
"""
DB = "postgreSQL"
DB.admin = postgres
DB.pw = devPw

to use postgresql:
install > setup env param > psql > create user > create db


>> Steps to log into PostgreSQL's default DB:

cd D:/DB/PostgreSQL/11/bin/
(start db cluster server): pg_ctl -D ^"D^:^\DB^\PostgreSQL^\11^\data^\^"^" -l logfile start
(root) psql "dbname=postgres host=localhost user=postgres password=devPw port=5432 sslmode=require"
(admin) psql "dbname=postgres host=localhost user=admin password=devPw port=5432 sslmode=require"
(entered into psql shell)
(stop db server): pg_ctl -D ^"D^:^\DB^\PostgreSQL^\11^\data^\^"^"  stop




dynamic content:
p2 vs p3:
POST /biz/ma/csmh/a/csmhaDoSort.html?aaee0102_03=&field=aaee0103&sort=desc&flag=0 HTTP/1.1
POST /biz/ma/csmh/a/csmhaDoSort.html?aaee0102_03=&field=aaee0103&sort=desc&flag=0 HTTP/1.1




Cookie = "PHPStat_First_Time_10000011=1480428327337; PHPStat_Cookie_Global_User_Id=_ck16112922052713449617789740328; PHPStat_Return_Time_10000011=1480428327337; PHPStat_Main_Website_10000011=_ck16112922052713449617789740328%7C10000011%7C%7C%7C; VISITED_COMPANY_CODE=%5B%22600064%22%5D; VISITED_STOCK_CODE=%5B%22600064%22%5D; seecookie=%5B600064%5D%3A%u5357%u4EAC%u9AD8%u79D1; _trs_uv=ke6m_532_iw3ksw7h; VISITED_MENU=%5B%228451%22%2C%229055%22%2C%229062%22%2C%229729%22%2C%228528%22%5D"

url = "http://query.sse.com.cn/security/stock/getStockListData2.do?&jsonCallBack=jsonpCallback41883&isPagination=true&stockCode=&csrcCode=&areaName=&stockType=1&pageHelp.cacheSize=1&pageHelp.beginPage=3&pageHelp.pageSize=25&pageHelp.pageNo=3&pageHelp.endPage=31&_=1480431103024"

headers = {
    'User-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36',
    'Cookie': Cookie,
    'Connection': 'keep-alive',
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'Host': 'query.sse.com.cn',
    'Referer': 'http://www.sse.com.cn/assortment/stock/list/share/'
}


# Headers:

GET /biz/ma/csmh/a/csmhaDoSort.html?pageNo=1&aaee0102_03=&field=aaee0103&sort=desc%3Bguanxing_xss_in_element_event%3D5d0723256607e38157e2a944880031cd%2F%2F&flag=0&_=1543986594434 HTTP/1.1
Host: cishan.chinanpo.gov.cn
Connection: keep-alive
Accept: */*
X-Requested-With: XMLHttpRequest
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36
Referer: http://cishan.chinanpo.gov.cn/biz/ma/csmh/a/csmhaindex.html
Accept-Encoding: gzip, deflate
Accept-Language: en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,ja-JP;q=0.6,ja;q=0.5
Cookie: Hm_lvt_3adce665674fbfb5552846b40f1c3cbc=1542598485; Hm_lpvt_3adce665674fbfb5552846b40f1c3cbc=1542598499; JSESSIONID=4A380739308255900D457603E0012EB0



req = urllib.request.Request(url,None,headers)
response = urllib.request.urlopen(req)
the_page = response.read()
print(the_page.decode("utf8"))


"""

