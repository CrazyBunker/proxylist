from proxylist import proxylist
import json
from jinja2 import Template
proxy = proxylist()
#test = {'domain1': {'ip': 1123123, 'port': 2341}}
with open('.cache.json') as cache:
     proxyForDomain = json.load(cache)
for domain in proxyForDomain:
     if not proxy.testProxy(domain, proxyForDomain[domain]['ip'], proxyForDomain[domain]['port']):
         proxy.set_type(['HTTPS'])
         proxy.excCountry(['RU'])
         answer = proxy.verify(domain)
         proxyForDomain[domain] = answer
     else:
         print('Saved proxy is done')
with open('.cache.json','w') as writeCache:
    json.dump(proxyForDomain,writeCache)

html = open('~/.proxy.pac.j2').read()
template = Template(html)
print(template.render(block=proxyForDomain))



