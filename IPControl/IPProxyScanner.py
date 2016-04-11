#!/usr/bin/env python
# coding:UTF-8

import re
import threading
import urllib2
import time

# 网站地址及解析方式和说明
proxyWebsites = []
#检查线程
checkThreads = []

proxyResultList = []

#共享cookies
#cookies = urllib2.HTTPCookieProcessor()

#测试用网址
checkURL = "http://www.baidu.com/"
checkRequestString = '030173'
defaultTimeout = 5

#添加代理网站 OK-1
urls = [r'http://sockslist.net/proxy/server-socks-hide-ip-address/%d#proxylist' % i for i in xrange(1,4) ]
pattern = re.compile(r'/check\?i=(.+?):[\s\S]*?\^(\d+)\)')
proxyWebsites.append({'urls':urls,'pattern':pattern});

#添加代理网站 OK-2
urls = [r'https://www.socks-proxy.net/' ]
pattern = re.compile(r'<tr><td>(.+?)</td><td>(\d+)</td>[\s\S]*?</tr>')
proxyWebsites.append({'urls':urls,'pattern':pattern});

#添加代理网站 OK-3
urls = [r'http://www.samair.ru/proxy/socks0%d.htm' % i for i in xrange(1,6)  ]
pattern = re.compile(r'<tr><td>(.+?):(\d+)</td>[\s\S]*?</tr>')
proxyWebsites.append({'urls':urls,'pattern':pattern});

# urls = [r"http://www.proxy.com.ru/list_%d.html" % i for i in xrange(1,2) ]
# pattern = re.compile(r'<tr><b><td>(\d+)</td><td>(.+?)</td><td>(\d+)</td><td>(.+?)</td><td>(.+?)</td></b></tr>')
# proxyWebsites.append({'urls':urls,'pattern':pattern});


def urlopen(url,useProxy,protocol = 'http',proxyUrl = '127.0.0.1', proxyPort = '11888', timeout=10):
    if useProxy:
        cookies = urllib2.HTTPCookieProcessor()
        proxyHandler = urllib2.ProxyHandler({protocol: r'http://%s:%s' % (proxyUrl,proxyPort)})
        # print r'http://%s:%s' % (proxyUrl,proxyPort)
        opener = urllib2.build_opener(cookies,proxyHandler)
        opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.57 Safari/537.36')
                             ,("Referer", url)]
        req = opener.open(url,timeout=timeout)
        return req
    else:
        return urllib2.urlopen(url)


class ProxyWebsiteHandler(threading.Thread):

    def __init__(self,url,pattern):
        threading.Thread.__init__(self)
        self.url = url
        self.pattern = pattern

    def handle(self):
        print u'开始分析网站'
        # 处理过程
        try:
            request = urlopen(url,useProxy=True,proxyUrl='127.0.0.1',proxyPort='11888')
            result = request.read()
            #print '------------------------------------------------------------------------------------------------------------'
            #print result
            #print '------------------------------------------------------------------------------------------------------------'
            matchs = pattern.findall(result)
            print matchs
            for match in matchs:
                # print match
                checkJob = ProxyCheck(match[0],match[1]);
                checkThreads.append(checkJob);
                checkJob.start()
        except Exception, e:
            print e.message
            
    def run(self):
        self.handle()


class ProxyCheck(threading.Thread):
    def __init__(self,proxyUrl,proxyPort):
        threading.Thread.__init__(self)
        self.proxyUrl = proxyUrl
        self.proxyPort = proxyPort

    def checkProxy(self):
        startTime = time.time()
        try:
            request = urlopen(checkURL,useProxy=True,protocol='sock', proxyUrl=self.proxyUrl, proxyPort=self.proxyPort, timeout=defaultTimeout)
            timeUsed = time.time() - startTime
            result = request.read()
            # print result
            pos = result.find(checkRequestString)
            #print "pos is %s" %pos
            if pos > 1:
                #checkedProxyList.append((proxy[0], proxy[1], proxy[2], timeused))
                msg = u"ok ip: %s %s %s" %(self.proxyUrl,self.proxyPort,timeUsed)
                proxyResultList.append(msg)
                print msg
                print proxyResultList
            else:
                pass
        except Exception, e:
            print e.message + ">>>"

    def run(self):
        self.checkProxy();


if __name__ == "__main__":
    print "__main__";
    handleThreads = []

    for job in proxyWebsites:
        print u'开始处理。。。'
        print job
        for url in job.get('urls'):
            handleThreads.append(ProxyWebsiteHandler(url,job.get('pattern')));
            # print 'url:',url,',job:',job.get('pattern')

    for handleThread in handleThreads:
        handleThread.start()

    for checkThread in checkThreads:
        checkThread.join()

    f = open("proxy_info.txt",'w+')
    for proxyResult in proxyResultList:
        f.write(proxyResult)
    f.close()