import json
class cacheJson ():
    def __init__(self,cacheFile):
        self.cacheFile = cacheFile
        with open(self.cacheFile) as cache:
            self.json = json.load(cache)

    def saveToCacheFile(self):
        with open(self.cacheFile, 'w') as writeCache:
            json.dump(self.json, writeCache)

    def data(self):
        return self.json[self.domain]

    def writeItem(self,item):
        self.json[self.domain] = item