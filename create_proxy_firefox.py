#!/usr/bin/env python
# -*- coding: utf-8 -*-
from proxyListThread import proxylist
from cacheJson import cacheJson
from jinja2 import Template
import argparse

parser = argparse.ArgumentParser(description='Search proxy server and update pac file for firefox.')
parser.add_argument('-u', '--url', default="https://htmlweb.ru/json/proxy/get", help="Url to proxy list api service")
parser.add_argument('-c', '--config', default=".cache.json", help="Path to config file in format json")
parser.add_argument('-p', '--pac', default=".proxy.pac", help="Path to output pac file for firefox")
parser.add_argument('-t', '--template', default="proxy.pac.j2", help="Path to templete for pac file")
parser.add_argument('-v', '--verbose', default=0, type=int, help="Verbose output")
args = parser.parse_args()

class htmlweb(proxylist):
    def converter(self, jsonData):
        # Used format : {"ip" : <ip address>, "port": <port>}
        cleaned = [{"ip": i['name'].split(":")[0], "port": i['name'].split(":")[1]} for i in [ jsonData[i] for i in jsonData ][1:-1]]
        return cleaned


isDone = False
rewrite = False
proxy = htmlweb(args.url)
proxy.verbose = args.verbose
cache = cacheJson(args.config)
cache.domain = list(cache.json)[0]
proxy.oldwinner = cache.data()
proxy.listForService = ["51.727.744.802:04863", "178.219.172.9:59967", "85.237.57.198:41594", "92.55.59.38:36415", "92.255.188.159:53281", "77.236.76.74:55087", "188.68.16.195:55465"]
for domain in cache.json:
      cache.domain = domain
      proxy.url = domain
      if not proxy.testProxy(cache.data()):
          proxy.set_type(['HTTPS'])
          proxy.exc = ['RU']
          answer = proxy.verify()
          cache.writeItem(answer)
          isDone = True
if isDone or rewrite:
     cache.saveToCacheFile()
     html = open(args.template).read()
     template = Template(html)
     pacFile = template.render(block=cache.json)
     with open(args.pac,'w') as pac:
         pac.write(pacFile)





