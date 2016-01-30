from flask import Flask
from createCoOccurrence import WordRecommender

app = Flask(__name__)

@app.route('/')
def index():
	obj = WordRecommender()
	obj.run()

if __name__ == '__main__':
	app.run(debug=True)