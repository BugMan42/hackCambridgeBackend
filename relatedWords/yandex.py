import json
import urllib2
import sys

def translate(requestWord, sourceLang, targetLang):
	key = "trnsl.1.1.20160130T213138Z.61f3d3183a7aea66.576cd55ad6fca5eebf5c5cb9a97c8249f897f142"
	req = 'https://translate.yandex.net/api/v1.5/tr.json/translate?key={}&text={}&lang={}-{}'.format(key, requestWord, sourceLang, targetLang)
	data = json.load(urllib2.urlopen(req))
	return requestWord + "\t" + data['text'][0]

if __name__ == "__main__":
	sys.exit()
