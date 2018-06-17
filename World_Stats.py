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
    # Open a connection to MongoDB using a with statement such that the
    # connection will be closed as soon as we exit the with statement
    # The MONGO_URI connection is required when hosted using a remote mongo db.
    with MongoClient(MONGO_URI) as conn:
        # Define which collection we wish to access
        collection = conn[DBS_NAME][COLLECTION_NAME]
        # Retrieve a result set only with the fields defined in FIELDS
        # and limit the the results to a lower limit of 20000
        projects = collection.find(projection=FIELDS, limit=20000)
        # Convert projects to a list in a JSON object and return the JSON data
        return json.dumps(list(projects))


if __name__ == "__main__":
    app.run(debug=True)