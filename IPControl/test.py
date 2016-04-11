#!/usr/bin/env python
# coding:UTF-8

import urllib2


if __name__ == '__main__':
    proxyUrl = '127.0.0.1'
    cookies = urllib2.HTTPCookieProcessor()
    proxyHandler = urllib2.ProxyHandler({"http": r'http://%s:%s' % (proxyUrl,proxyPort)})
    # print r'http://%s:%s' % (proxyUrl,proxyPort)
    opener = urllib2.build_opener(cookies,proxyHandler)
    opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.57 Safari/537.36')]
    req = opener.open(url,timeout=timeout)