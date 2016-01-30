from flask import Flask, request
from createCoOccurrence import WordRecommender

app = Flask(__name__)

@app.route('/', methods=['POST'])
def index():
	word = request.form['word']
	nRecom = request.form['nrecom']
	obj = WordRecommender()
	obj.run()

if __name__ == '__main__':
	app.run(debug=True)