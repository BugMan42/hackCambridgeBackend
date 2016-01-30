import json
import urllib2

key = "trnsl.1.1.20160130T213138Z.61f3d3183a7aea66.576cd55ad6fca5eebf5c5cb9a97c8249f897f142"

requestWord = "casa"
req = 'https://translate.yandex.net/api/v1.5/tr.json/translate?' + 'key=' + key + '&text=' + requestWord + '&lang=es-en'
data = json.load(urllib2.urlopen(req))
print requestWord + "\t" + data['text'][0]


