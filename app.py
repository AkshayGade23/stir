from flask import Flask, render_template,jsonify
from scrape import fetch_trending_topics,fetch_data_mongo

app = Flask(__name__)

data = []
fetchdata = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run_script', methods=['GET'])
def run_script():
    data = fetch_trending_topics()
    return data

@app.route('/run_queury', methods=['GET'])
def run_query():
    fetchdata = jsonify(fetch_data_mongo())
    return fetchdata

if __name__ == "__main__":
    app.run(debug=True)




