from proxylist import proxylist
import json
from jinja2 import Template
proxy = proxylist()
isDone = True
rewrite = False


with open('.cache.json') as cache:
     proxyForDomain = json.load(cache)
for domain in proxyForDomain:
     if not proxy.testProxy(domain, proxyForDomain[domain]['ip'], proxyForDomain[domain]['port']):
         proxy.set_type(['HTTPS'])
         proxy.excCountry(['RU'])
         answer = proxy.verify(domain)
         proxyForDomain[domain] = answer
     else:
         isDone = False
         print('Saved proxy is done')
if isDone or rewrite:
    with open('.cache.json','w') as writeCache:
        json.dump(proxyForDomain,writeCache)
    html = open('proxy.pac.j2').read()
    template = Template(html)
    pacFile = template.render(block=proxyForDomain)
    with open('/home/qq/.proxy.pac','w') as pac:
        pac.write(pacFile)





