#!/usr/bin/env python
# # -*- coding: utf-8 -*-
import requests
import sys
from time import time
class proxylist():
    def __init__(self,listurl="http://api.foxtools.ru/v2/Proxy"):
        self.error = [ True for _ in range(6) ]
        self.error[0] = ''
        self.listurl = listurl
        self.args = {}
        self.type = {'None':0,'HTTP':1,'HTTPS':2,'SOCKS4':4, 'SOCKS5': 8,'All':15 }
        self.exc = {}
        self.oldwinner = {}
        self.verbose = 0
    def __get_request__(self):
        self.args['available'] =  1
        self.error[2] = "Get request %s" % (self.listurl)
        if self.verbose >= 2:
            print(self.error[2])
        try:
            self.req = requests.post(self.listurl, data=self.args, timeout=3)
        except requests.exceptions.SSLError as e:
            self.error[3] = "SSL Error for proxy list service"
        except requests.exceptions.ConnectTimeout as e:
            self.error[3] = "Connection timeout for proxy list service"
        except requests.exceptions.ConnectionError as e:
            self.error[3] = "Connection error for proxy list service"
        else:
            return self.req
        if self.verbose >= 3:
            print(self.error[3])
        sys.exit(1)

    def response(self):
        resp = self.__get_request__()
        return resp.json()

    def set_paramer(self, param):
        for i in param:
            self.args[i] = param[i]

    def set_type(self, types):
        summarizedType = 0
        for type in types:
           summarizedType+=self.type[type]
           self.set_paramer({ 'type' :summarizedType})

    def __excludeFromResponse(self):
        jsonData = self.response()['response']['items']
        cleaned = [ i for i in jsonData if not i['country']['iso3166a2'] in self.exc ]
        return cleaned
    def verify(self):
        verifyList = {}
        proxyList = self.__excludeFromResponse()
        for proxyData in proxyList:
           if self.verbose >= 5:
               print(self.error[5])
           ip = proxyData['ip']
           port = proxyData['port']
           if proxyData['free'] == 'Yes':  # and proxyData['anonymity'] == 'HighKeepAlive'
               proxies = {'https':'%s:%s'%(ip,port)}
               try:
                   t0 = time()
                   response = requests.get(url=self.url, proxies=proxies, timeout=10,verify=False)
               except requests.exceptions.ProxyError as e:
                   self.error[5] = "%s - %s" % (proxies['https'],e)
               except requests.exceptions.SSLError as e:
                   self.error[5] = "%s - %s" % (proxies['https'],e)
               except requests.exceptions.ConnectTimeout as e:
                   self.error[5] = "%s - %s" % (proxies['https'],e)
               except requests.exceptions.ConnectionError as e:
                   self.error[5] = "%s - %s" % (proxies['https'],e)
               except requests.exceptions.ReadTimeout:
                   self.error[5] = "%s - %s" % (proxies['https'], e)
               else:
                   if response.status_code == 200:
                       t1 = time()
                       verifyList[int(t1-t0)] = {'ip': str(ip),'port': str(port)}
        if len(verifyList) == 0:
             if self.verbose >= 2:
                print(self.error[2])
        else:
             winner = sorted(verifyList)[0]
             self.error[1] = "Proxy for use %s" % (verifyList[winner])
             if self.verbose >= 1:
                print(self.error[1])
                self.oldwinner = verifyList[winner]
             return self.oldwinner
        return self.oldwinner

    def testProxy(self, proxy):
        proxies = {'https': '%s:%s' % (proxy['ip'], proxy['port'])}
        try:
            response = requests.get(url=self.url, proxies=proxies, timeout=3)
        except requests.exceptions.ProxyError as e:
            self.error[4] = "%s - %s" % (proxies['https'],e)
        except requests.exceptions.SSLError as e:
            self.error[4] = "%s - %s" % (proxies['https'],e)
        except requests.exceptions.ConnectTimeout as e:
            self.error[4] = "%s - %s" % (proxies['https'],e)
        else:
            if response.status_code == 200:
                self.error[1] = "Check is done, used proxy from cache file"
                if self.verbose >= 1:
                    print(self.error[1])
                return True
        self.error[1] = "Check is failed, start searchinng new proxy"
        if self.verbose >= 1:
            print(self.error[1])
        if self.verbose >= 4:
            print(self.error[4])
        return False


