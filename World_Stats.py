from flask import Flask
from flask import render_template
from pymongo import MongoClient
import json
import os

app = Flask(__name__)

MONGO_URI = os.getenv('MONGODB_URI', 'mongodb://root:tqksgzQ!@8a6fv2,@ds163330.mlab.com:63330/heroku_7ssmmd91')
DBS_NAME = os.getenv('MONGO_DB_NAME', 'heroku_7ssmmd91')
COLLECTION_NAME = os.getenv('MONGO_COLLECTION_NAME', 'worldCountries')

FIELDS = {
    '_id': False,
    'country': True,
    'capital': True,
    'population': True,
    'languages': True,
    'area': True,
    'currency': True,
    'continent': True,
    'drive': True
}


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/worldStats/worldCountries")
def stat_projects():

    with MongoClient(MONGO_URI) as conn:
        collection = conn[DBS_NAME][COLLECTION_NAME]
        projects = collection.find(projection=FIELDS, limit=20000)
        return json.dumps(list(projects))


if __name__ == "__main__":
    app.run(debug=True)
