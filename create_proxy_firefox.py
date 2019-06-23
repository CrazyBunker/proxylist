#!/usr/bin/env python
# -*- coding: utf-8 -*-
from proxylist import proxylist
from cacheJson import cacheJson
from jinja2 import Template
import argparse

parser = argparse.ArgumentParser(description='Search proxy server and update pac file for firefox.')
parser.add_argument('-u', '--url', default="http://api.foxtools.ru/v2/Proxy", help="Url to proxy list api service")
parser.add_argument('-c', '--config', default=".cache.json", help="Path to config file in format json")
parser.add_argument('-p', '--pac', default=".proxy.pac", help="Path to output pac file for firefox")
parser.add_argument('-t', '--template', default="proxy.pac.j2", help="Path to templete for pac file")
parser.add_argument('-v', '--verbose', default=0, type=int, help="Verbose output")
args = parser.parse_args()

isDone = True
rewrite = False
proxy = proxylist(args.url)
proxy.verbose = args.verbose
if proxy.verbose > 5:
    proxy.verbose = 5
cache = cacheJson(args.config)
for domain in cache.json:
      cache.domain = domain
      proxy.url = domain
      if not proxy.testProxy(cache.data()):
          proxy.set_type(['HTTPS'])
          proxy.excCountry(['RU'])
          answer = proxy.verify()
          cache.writeItem(answer)
      else:
          isDone = False
if isDone or rewrite:
     cache.saveToCacheFile()
     html = open(args.template).read()
     template = Template(html)
     pacFile = template.render(block=cache.json)
     with open(args.pac,'w') as pac:
         pac.write(pacFile)





