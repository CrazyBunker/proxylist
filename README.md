### Finding a proxy and creating a proxy.pac file

The script searches for a suitable proxy from the proxy list and creates a pac file for firefox.

At startup, checks the availability of the site through the saved proxy in the json file, if the site is not available, then a search is performed, and if json is found, the file is updated.

##### Proxy Sheet Source
by default, proxy sheets are taken from the service http://api.foxtools.ru/v2/Help/Proxy

#### Parameters
- -u url:  proxy service - sites whis api for get proxy lists, default _http://api.foxtools.ru/v2/Proxy_
- -c config:  path to cache file - keep configurations domains and used proxy server, format json, default _.cache.json_
- -p packfile: path to pac file for firefox, default _./proxy.pac_
- -t template: path to template file for pac, default _./proxy.pac.j2_
- -v verbose: 0-5 verbose level output, default 0

#### Format json file configuration
```
{"https://www.domain.com": {"ip": "127.0.0.1", "port": "8080"}}
```

Be sure to specify 3rd level domains


### Installing dependent libraries
```
pip install -r requirements.txt --upgrade
```

### Running script
* Via cron:
```
30 */3 * * * python /home/user/git/proxylist/create_proxy_firefox.py --template /home/user/git/proxylist/proxy.pac.j2 --config /home/user/git/proxylist/.cache.json --pac /home/user/.proxy.pac
```
* Manually:
 ```
 python /home/user/git/proxylist/create_proxy_firefox.py --template /home/user/git/proxylist/proxy.pac.j2 --config /home/user/git/proxylist/.cache.json --verbose 5 --pac /home/user/.proxy.pac
 ```