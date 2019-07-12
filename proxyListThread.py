#!/usr/bin/env python
# # -*- coding: utf-8 -*-
import requests
import sys
from time import time
import threading
import queue


class Worker(threading.Thread):

    def __init__(self, work_queue, proxyList):
        super(Worker, self).__init__()
        self.work_queue = work_queue
        self.proxyList = proxyList
        self.timing = {}
    def run(self):
        try:
            proxyData = self.work_queue.get()
            self.process(proxyData)
        finally:
            pass

    def process(self, proxyData):
        ip = proxyData['ip']
        port = proxyData['port']
        proxies = {'https': '%s:%s' % (ip, port)}
        t0 = time()
        answer = self.proxyList.__getRequest__(self.proxyList.url, "", proxies, 20)
        try:
            if answer.status_code == 200:
                t1 = time()
                self.timing[int(t1 - t0)] = {'ip': str(ip), 'port': str(port)}
                print("%s - %s" % (proxies, self.proxyList.url))
        except AttributeError:
            print(answer)

class proxylist():
    def __init__(self, listurl="http://api.foxtools.ru/v2/Proxy"):
        self.listurl = listurl
        self.args = {}
        self.type = {'None':0,'HTTP':1,'HTTPS':2,'SOCKS4':4, 'SOCKS5': 8,'All':15 }
        self.url = ""
        self.work_queue = queue.Queue()
    def __getRequest__(self,url, args={}, proxies={},timeout=3):
        try:
            if len(args) == 0:
                req = requests.get(url, proxies=proxies, timeout=timeout, verify=False)
            else:
                req = requests.post(url, data=args, timeout=timeout)
        except requests.exceptions.SSLError as e:
            error = "SSL Error for proxy list service"
        except requests.exceptions.ConnectTimeout as e:
            error = "Connection timeout for proxy list service"
        except requests.exceptions.ConnectionError as e:
            error = "Connection error for proxy list service"
        except requests.exceptions.ReadTimeout:
            error = "Connection timeout for proxy list service"
        else:
            return req
        return error

    def set_paramer(self, param):
        for i in param:
            self.args[i] = param[i]

    def set_type(self, types):
        summarizedType = 0
        for type in types:
           summarizedType+=self.type[type]
           self.set_paramer({ 'type' :summarizedType})

    def __getProxyList(self):
        try:
            answer = self.__getRequest__(self.listurl,self.args)
            response=answer.json()
        except:
            print(answer)
            sys.exit(1)
        return response

    def __excludeFromResponse(self):
        jsonData = self.__getProxyList()['response']['items']
        cleaned = [ i for i in jsonData if not i['country']['iso3166a2'] in self.exc ]
        return cleaned

    def verify(self):
        proxyList = self.__excludeFromResponse()
        workerthreadlist = []
        proxyVerifedList = {}
        for proxyData in proxyList:
            self.work_queue.put(proxyData)
        for _ in proxyList:
            worker = Worker(self.work_queue, self)
            workerthreadlist.append(worker)
            worker.start()
        for x in range(len(proxyList)):
            workerthreadlist[x].join()
        for x in range(len(proxyList)):
            proxyVerifedList.update(workerthreadlist[x].timing)

        winner = sorted(proxyVerifedList)[0]
        print("Proxy for use %s" % (proxyVerifedList[winner]))
        return proxyVerifedList[winner]

    def testProxy(self, proxy):
        proxies = {'https': '%s:%s' % (proxy['ip'], proxy['port'])}
        answer = self.__getRequest__(self.url, "", proxies, 20)
        try:
             if answer.status_code == 200:
                print("Check is done, used proxy from cache file")
                return True
        except AttributeError:
            print(answer)
        print("Check is failed, start searchinng new proxy")
        return False

