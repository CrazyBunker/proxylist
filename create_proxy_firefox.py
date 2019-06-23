from proxylist import proxylist
from cacheJson import cacheJson
from jinja2 import Template

isDone = True
rewrite = False

proxy = proxylist()
cache = cacheJson('.cache.json')
proxy.verbose = 5
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
     html = open('proxy.pac.j2').read()
     template = Template(html)
     pacFile = template.render(block=cache.json)
     with open('/home/qq/.proxy.pac','w') as pac:
         pac.write(pacFile)





