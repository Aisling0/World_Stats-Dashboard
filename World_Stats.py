from flask import Flask
from flask import render_template
from pymongo import MongoClient
import json
import os

app = Flask(__name__)

#*** Run Locally ***#
# MONGODB_HOST = 'localhost'
# MONGODB_PORT = 27017
# DBS_NAME = 'worldStats'
# COLLECTION_NAME = 'worldCountries'
#*** END: Run Locally ***#

MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://heroku_7ssmmd91:oduotmmvrf4pvsknff12bmujn8@ds163330.mlab.com:63330/heroku_7ssmmd91')
DBS_NAME = os.getenv('MONGO_DB_NAME','heroku_7ssmmd91')
COLLECTION_NAME = os.getenv('MONGO_COLLECTION_NAME','worldCountries')

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


    # *** Run Locally ***#
    # with MongoClient(MONGODB_HOST, MONGODB_PORT) as conn:
    # *** END: Run Locally ***#

    # * Congfigure to run on heroku *#
    connection = MongoClient(MONGODB_URI)
    # * END Congfigure to run on heroku *#

    collection = connection[DBS_NAME][COLLECTION_NAME]
    projects = collection.find(projection=FIELDS, limit=20000)
    json_projects = []
    for project in projects:
        json_projects.append(project)
    json_projects = json.dumps(json_projects)
    connection.close()
    return json_projects


if __name__ == "__main__":
    app.run(debug=True)
