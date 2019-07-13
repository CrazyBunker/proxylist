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
                self.timing[int((t1 - t0)*100)] = {'ip': str(ip), 'port': str(port)}
                if self.proxyList.verbose > 2:
                    print("%s - %s" % (proxies, self.proxyList.url))
        except AttributeError:
            if self.proxyList.verbose > 3:
                print(answer)

class proxylist():
    def __init__(self, listurl):
        self.listurl = listurl
        self.args = {}
        self.type = {'None':0,'HTTP':1,'HTTPS':2,'SOCKS4':4, 'SOCKS5': 8,'All':15 }
        self.url = ""
        self.work_queue = queue.Queue()
        self.listForService = []
        self.oldwinner = {"ip": "127.0.0.1", "port": "3128"}
        self.answer = ""
        self.verbose = 0
    def __getRequest__(self,url, args={}, proxies={},timeout=3):
        try:
            if len(args) == 0:
                req = requests.get(url, proxies=proxies, timeout=timeout)
            else:
                req = requests.post(url, data=args, proxies=proxies, timeout=timeout)
        except requests.exceptions.SSLError as e:
            error = "SSL Error for proxy list service"
        except requests.exceptions.ConnectTimeout as e:
            error = "Connection timeout for proxy list service"
        except requests.exceptions.ConnectionError as e:
            error = "Connection error for proxy list service"
        except requests.exceptions.ReadTimeout:
            error = "Connection timeout for proxy list service"
        except requests.exceptions.InvalidURL:
            error = "InvalidURL"
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

    def getProxyList(self):
        for i in self.listForService:
            if type(self.answer) == str:
                if self.verbose > 2:
                    print("Update proxy cache, used proxy %s" % (i))
                self.answer = self.__getRequest__(self.listurl,self.args, {"https": i},10)
            try:
                response = self.answer.json()
                return response
            except:
                if self.verbose > 2:
                    print("Update is false")
        sys.exit(1)

    def converter(self):
        jsonData = self.getProxyList()['response']['items']
        cleaned = [ i for i in jsonData if not i['country']['iso3166a2'] in self.exc ]
        return cleaned

    def verify(self):
        proxyList = self.converter(self.getProxyList())
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
        winner = "Cache"
        if len(proxyVerifedList) > 0:
            winner = sorted(proxyVerifedList)[0]
            self.oldwinner = proxyVerifedList[winner]
        if self.verbose > 0:
            print("Proxy for use %s - timeout: %s" % (self.oldwinner, winner))
        return self.oldwinner

    def testProxy(self, proxy):
        proxies = {'https': '%s:%s' % (proxy['ip'], proxy['port'])}
        answer = self.__getRequest__(self.url, "", proxies, 5)
        try:
             if answer.status_code == 200:
                if self.verbose > 1:
                    print("Check is done, used proxy from cache file")
                return True
        except AttributeError:
            print(answer)
        if self.verbose > 1:
            print("Check is failed, start searchinng new proxy")
        return False

