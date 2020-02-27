from flask import request
from flask_restful import Resource
from myflaskbackend.utils.configurations import api_settings
from werkzeug.utils import secure_filename
from pathlib import Path
import pymongo

ALLOWED_DATA_EXTENSIONS = ['csv']


class ConnectToDb(Resource):
    """
    POST to this resource to connect to Mongodb database.

    $ curl -i -X POST -F -d "username=value1&password=value2" http://localhost:5000/connecttodb
    """
    def post(self):
        form = request.form
        auth_msg = 'mongodb+srv://' + str(form['username']) + ':' + str(form['password']) + '@cluster0-sahac.mongodb.net/test?retryWrites=true&w=majority'
        client = pymongo.MongoClient(auth_msg)
        db = client.test_database
        collections_list = db.list_collection_names()
        birds = db.birds

        print(f'Connected to database: {db.name}')
        print(f'{db.name} has the following collections: {collections_list}')
        print(f'In birds collection, there is this entry: {birds.find_one()}')


class UploadCsvFile(Resource):
    """
    POST to this resource to upload a CSV file to the server.

    Test from command line:
    $ curl -i -X POST -F "client_file=@example.csv" http://localhost:5000/uploadcsvfile
    """
    def __init__(self):
        self.resource_name = 'store_csv_file'
        if api_settings['RUNNING_LOCATION'] == 'local':
            self.base_dir = Path(api_settings['MONGO_DB_PATH'])
        elif api_settings['RUNNING_LOCATION'] == 'remote':
            self.base_dir = Path('')

    def post(self):
        f = request.files['client_file']
        # Test if file type is allowed
        file_name = Path(f.filename).name
        if not self.allowed_file(file_name):
            return "File extension not allowed. Currently allowed file extensions are: " + ", ".join(ALLOWED_DATA_EXTENSIONS)
        # Save file on base_dir
        f.save(str(self.base_dir / secure_filename(file_name)))
        msg = f"File '{f.filename}' stored in directory {self.base_dir}"
        return msg

    def allowed_file(self, filename):
        is_allowed = '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_DATA_EXTENSIONS
        return is_allowed
