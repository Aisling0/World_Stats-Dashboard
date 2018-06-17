from flask import Flask
from flask import render_template
from pymongo import MongoClient
import json
import os

app = Flask(__name__)

MONGODB_URI = os.getenv('MONGODB_URI')
DBS_NAME = os.getenv('MONGO_DB_NAME')
COLLECTION_NAME = os.getenv('MONGO_COLLECTION_NAME', 'worldCountries')


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/worldStats/worldCountries")
def stat_projects():

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
    connection = MongoClient(MONGODB_URI)

    collection = connection[DBS_NAME][COLLECTION_NAME]
    projects = collection.find(projection=FIELDS, limit=55000)
    json_projects = []
    for project in projects:
        json_projects.append(project)
    json_projects = json.dumps(json_projects)
    connection.close()
    return json_projects


#   important to close the connection


if __name__ == "__main__":
    app.run(debug=True)
