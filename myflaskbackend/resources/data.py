from flask import request, current_app
from flask_restful import Resource
from myflaskbackend.utils.configurations import api_settings
from werkzeug.utils import secure_filename
from pathlib import Path
import pandas as pd
import pymongo
import json

ALLOWED_DATA_EXTENSIONS = ['csv']


def mongo_import_csv(csv_path, collection):
    """
    Imports a csv file to a mongo colection
    returns: count of the documants in the new collection
    """
    data = pd.read_csv(csv_path)
    payload = json.loads(data.to_json(orient='records'))
    collection.remove()
    collection.insert(payload)
    return collection.count()


class ConnectToDb(Resource):
    """
    POST to this resource to connect to Mongodb database.

    $ curl -i -X POST -d "username=value1&password=value2" http://localhost:5000/connecttodb
    """
    def post(self):
        form = request.form
        auth_msg = 'mongodb+srv://' + str(form['username']) + ':' + str(form['password']) + '@cluster0-sahac.mongodb.net/test?retryWrites=true&w=majority'
        client = pymongo.MongoClient(auth_msg)
        db = client.test_database
        collections_list = db.list_collection_names()
        # Store database on redis
        redis_store = current_app.extensions['redis']
        redis_store.db = db
        # with api.app_context():
        #     client = pymongo.MongoClient(auth_msg)
        #     db = client.test_database
        #     collections_list = db.list_collection_names()
        #     #birds = db.birds
        #
        print(f'Connected to database: {db.name}')
        print(f'{db.name} has the following collections: {collections_list}')
        # print(f'In birds collection, there is this entry: {birds.find_one()}')


class UploadCsvFile(Resource):
    """
    POST to this resource to upload a CSV file to the server.

    Test from command line:
    $ curl -i -X POST -F "client_file=@example.csv" -F "collection_name=example" http://localhost:5000/uploadcsvfile
    """
    def __init__(self):
        self.resource_name = 'store_csv_file'
        if api_settings['RUNNING_LOCATION'] == 'local':
            self.base_dir = Path(api_settings['MONGO_DB_PATH'])
        elif api_settings['RUNNING_LOCATION'] == 'remote':
            self.base_dir = Path('')

    def post(self):
        collection_name = request.form['collection_name']
        f = request.files['client_file']
        # Test if file type is allowed
        file_name = Path(f.filename).name
        if not self.allowed_file(file_name):
            return "File extension not allowed. Currently allowed file extensions are: " + ", ".join(ALLOWED_DATA_EXTENSIONS)

        # Save file on base_dir
        file_path_server = str(self.base_dir / secure_filename(file_name))
        f.save(file_path_server)
        msg = f"File '{f.filename}' stored in directory {self.base_dir}"

        # Save data to collection
        redis_store = current_app.extensions['redis']
        db = redis_store.db
        # if collection_name not in db.list_collection_names():
        #     return print(f'{collection_name} is not a collection in current database.')
        # else:
        n_items = mongo_import_csv(file_path_server, getattr(db, collection_name))
        return print(f'{n_items} items stored in collection {collection_name}')

    def allowed_file(self, filename):
        is_allowed = '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_DATA_EXTENSIONS
        return is_allowed
