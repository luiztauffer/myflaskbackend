from flask import request
from flask_restful import Resource
#from myflaskbackend.my_app import api_settings
from werkzeug.utils import secure_filename
from pathlib import Path


api_settings = {
    'RUNNING_LOCATION': "local",  # ['local', 'remote']
    'MONGOD_EXEC_PATH': "C:\\Program Files\\MongoDB\\Server\\4.2\\bin\\mongod.exe",
    'MONGO_DB_PATH': "C:\\Users\\Luiz\\Desktop\\mymongodb",
    'DB_IS_RUNNING': False,
}

ALLOWED_DATA_EXTENSIONS = ['csv']


class StoreCsvData(Resource):
    """
    POST to this recource to save a CSV file in the server.

    Test from command line:
    $ curl -i -X POST -F "client_file=@example.csv" http://localhost:5000/storecsvdata
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
        if not self.allowed_file(f.filename):
            return "File extension not allowed. Currently allowed file extensions are: " + ", ".join(ALLOWED_DATA_EXTENSIONS)

        # Save file on base_dir
        f.save(str(self.base_dir / secure_filename(f.filename)))
        msg = f"File '{f.filename}' stored in directory {self.base_dir}"
        return msg

    def allowed_file(self, filename):
        is_allowed = '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_DATA_EXTENSIONS
        return is_allowed
