from flask import Flask, request
from createCoOccurrence import WordRecommender
import json

obj = WordRecommender()
obj.loadPrecomputedStatistics()
app = Flask(__name__)

@app.route('/relatedWords', methods=['POST'])
def index():
	word = request.form['word']
	nRecom = request.form['nRecom']
	res = obj.run(word, nRecom)
	jsonRes = json.dumps(res)
	if len(res) == 0:
		return jsonRes, 404
	else:
		return jsonRes, 200

@app.route('/discardedWords', methods=['POST'])
def discardedWords():
	words = request.get_json()
	obj.updateDiscardedWords(words)
	return "OK"

@app.route('/acceptedWords', methods=['POST'])
def acceptedWords():
	words = request.get_json()
	print words
	obj.updateAcceptedWords(words)
	return "OK"

@app.route('/filterListOfWords', methods=['POST'])
def filterListOfWords():
	body = request.get_json()
	words = body['words']
	nWords = int(body['nWords'])
	words = obj.filterListOfWords(words, nWords)
	jsonRes = json.dumps(words)
	return jsonRes

if __name__ == '__main__':
	app.run(debug=True, host= '0.0.0.0')
