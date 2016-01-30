from flask import Flask, request
from createCoOccurrence import WordRecommender
import json

obj = WordRecommender()
obj.loadPrecomputedStatistics()
app = Flask(__name__)

@app.route('/', methods=['POST'])
def index():
	word = request.form['word']
	nRecom = request.form['nRecom']
	return json.dumps(obj.run(word, nRecom))

if __name__ == '__main__':
	app.run(debug=False, host= '0.0.0.0')
