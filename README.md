### Finding a proxy and creating a proxy.pac file

The script searches for a suitable proxy from the proxy list and creates a pac file for firefox.

At startup, checks the availability of the site through the saved proxy in the json file, if the site is not available, then a search is performed, and if json is found, the file is updated.