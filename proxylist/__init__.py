import requests
class proxylist():
    def __init__(self,url="http://api.foxtools.ru/v2/Proxy"):
        self.url = url
        self.args = {}
        self.type = {'None':0,'HTTP':1,'HTTPS':2,'SOCKS4':4, 'SOCKS5': 8,'All':15 }
        self.exc = {}
    def __get_request__(self):
        self.args['available'] =  1
        self.req = requests.post(self.url, data=self.args)
        print('Get request')
        return self.req

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

    def excCountry(self, country):
        self.exc = country

    def __excludeFromResponse(self):
        jsonData = self.response()['response']['items']
        cleaned = [ i for i in jsonData if not i['country']['iso3166a2'] in self.exc ]
        return cleaned
    def verify(self, url="https://www.linkedin.com", timeout=0.1):
        verifyList = {}
        proxyList = self.__excludeFromResponse()
        while True:
             for proxyData in proxyList:
                ip = proxyData['ip']
                port = proxyData['port']
                if proxyData['free'] == 'Yes' and proxyData['anonymity'] == 'HighKeepAlive':
                    proxies = {'https':'%s:%s'%(ip,port)}
                    try:
                        response = requests.get(url=url, proxies=proxies, timeout=timeout)
                    except requests.exceptions.ProxyError:
                        continue
                    except requests.exceptions.SSLError:
                        continue
                    except requests.exceptions.ConnectTimeout:
                        continue
                    if response.status_code == 200:
                        verifyList[proxyData['uptime']] = {'ip': str(ip),'port': str(port)}
             if len(verifyList) == 0:
                timeout+=0.1
                print(timeout)
             else:
                winner = sorted(verifyList)[0]
                break
        return verifyList[winner]

    def testProxy(self,url,ip,port):
        proxies = {'https': '%s:%s' % (ip, port)}
        try:
            response = requests.get(url=url, proxies=proxies)
        except requests.exceptions.ProxyError:
            return False
        except requests.exceptions.SSLError:
            return False
        except requests.exceptions.ConnectTimeout:
            return False
        if response.status_code == 200:
            return True


