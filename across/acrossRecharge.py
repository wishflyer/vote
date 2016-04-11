#!/usr/bin/env python
# coding:UTF-8

import urllib
import urllib2
import re
import json
import time
import sys

#设置编码
reload(sys)
sys.setdefaultencoding('utf-8')

#设置日志路径
logFile = r'H:/backup/across/log.txt'

#登录URL
loginUrl = "https://across.cm/i/_login.php"
loginData = {'email':'13377688576@189.cn', 'passwd':'dd112233'}
#登录后主页URL
indexUrl = 'https://across.cm/i/index.php'

#opener 启用Cookie
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())

def login():
    #登录
    request = urllib2.Request(loginUrl)
    data = urllib.urlencode(loginData)
    response = opener.open(request, data)
    #检查是否登录成功
    result =  response.read()
    # print result
    # 成功：{"code":"1","ok":"1","msg":"\u6b22\u8fce\u56de\u6765"}
    # 失败：{"code":"0","msg":"\u90ae\u7bb1\u6216\u8005\u5bc6\u7801\u9519\u8bef\u3002\u82e5\u60a8\u5fd8\u8bb0\u5bc6\u7801\uff0c\u60a8\u53ef\u80fd\u9700\u8981\u91cd\u65b0\u6ce8\u518c"}
    status = json.loads(result)["code"]
    if status == '1':
        #print "登录成功"
        return True
    else:
        #print "登录失败"
        return False

def getInfo():
    # 登录成功
    response = opener.open(indexUrl)
    result = response.read()
    pattern = re.compile(r'已用流量： (.+?)GB[\s\S]*?可用流量： (.+?)GB[\s\S]*?剩余流量： (.+?)GB',re.S);
    matches = pattern.findall(result);
    #已用流量
    trafficUsed = matches[0][0]
    #可用流量
    trafficTotal = matches[0][1]
    #剩余流量
    trafficAvailable=matches[0][2]
    #print u'剩余流量为：',trafficAvailable,'GB'

    resultInfo = {'result':result,'trafficUsed':trafficUsed,'trafficTotal':trafficTotal,'trafficAvailable':trafficAvailable}

    return resultInfo

def getPackage():
    #添加流量包
    getPackageUrl = 'https://across.cm/i/gettransfers.php'
    response = opener.open(getPackageUrl)

if __name__ == '__main__':

    f = open(logFile, 'a')
    if login():
        resultInfo = getInfo()
        trafficAvailable = resultInfo['trafficAvailable']
        if float(trafficAvailable) >= 0.5:
            msg = time.strftime('%Y-%m-%d %X',time.localtime()) + u' >> 目前剩余流量为：'+ trafficAvailable + u"GB,大于500MB,不需要加流量包\n"
            #无论如何都要抽个流量包
            pattern = re.compile(r'领取本次加油包',re.S);
            matches = pattern.findall(resultInfo['result']);
            if len(matches) > 0:
                getPackage()
                resultInfo = getInfo()
                newTrafficAvailable = resultInfo['trafficAvailable']
                msg = time.strftime('%Y-%m-%d %X',time.localtime()) + u' >> 当前剩余流量为：'+ trafficAvailable + u"GB,大于500MB,抽个流量包碰碰运气，抽到"+str(float(newTrafficAvailable)-float(trafficAvailable))+u"GB流量,目前剩余流量：" + newTrafficAvailable + "GB\n"
        else:
            #加流量包
            pattern = re.compile(r'领取本次加油包',re.S);
            matches = pattern.findall(resultInfo['result']);
            if len(matches)  == 0:
                msg = time.strftime('%Y-%m-%d %X',time.localtime()) + u' >> 当前剩余流量为：'+ trafficAvailable + u'GB,但未到领取流量包时间，不做处理\n'
            else:
                getPackage()
                resultInfo = getInfo()
                newTrafficAvailable = resultInfo['trafficAvailable']
                msg = time.strftime('%Y-%m-%d %X',time.localtime()) + u' >> 当前剩余流量为：'+ trafficAvailable + u"GB,小于500MB,程序已自动添加流量包，目前剩余流量：" + newTrafficAvailable + "GB\n"
        print msg
    else:
        msg = time.strftime('%Y-%m-%d %X',time.localtime()) + u' >> 登录失败，请检查程序！'
        print msg
    f.write(msg)
    f.close()