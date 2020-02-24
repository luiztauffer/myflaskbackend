from flask import request
from flask_restful import Resource


ALLOWED_DATA_EXTENSIONS = ['csv']


class StoreCsvData(Resource):
    def __init__(self):
        self.resource_name = 'store_csv_file'

    def post(self):
        f = request.files['data_file']
        # Test if file type is allowed
        if not self.allowed_file(f.filename):
            return "File extension not allowed. Currently allowed file extensions are: " + ", ".join(ALLOWED_DATA_EXTENSIONS)

        f.save(f.filename)
        msg = f"File '{f.filename}' stored in directory ''"
        return msg

    def allowed_file(self, filename):
        is_allowed = '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_DATA_EXTENSIONS
        return is_allowed
