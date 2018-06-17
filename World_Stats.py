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

@app.route("/")
def index():
    """
    A Flask view to serve the main dashboard page.
    """
    return render_template("index.html")


@app.route("/worldStats/worldCountries")
def stat_projects():
    """
    A Flask view to serve the project data from
    MongoDB in JSON format.
    """

    # A constant that defines the record fields that we wish to retrieve.
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

    # Open a connection to MongoDB using a with statement such that the
    # connection will be closed as soon as we exit the with statement
    # *** Run Locally ***#
    # with MongoClient(MONGODB_HOST, MONGODB_PORT) as conn:
    # *** END: Run Locally ***#
    with MongoClient(MONGO_URI) as conn:
        # Define which collection we wish to access
        collection = conn[DBS_NAME][COLLECTION_NAME]
        # Retrieve a result set only with the fields defined in FIELDS
        # and limit the the results to 55000
        projects = collection.find(projection=FIELDS, limit=20000)
        # Convert projects to a list in a JSON object and return the JSON data
        return json.dumps(list(projects))


if __name__ == "__main__":
    app.run(debug=True)
