from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from flask_pymongo import PyMongo
# from flask_mongoengine import MongoEngine

from myflaskbackend.resources.data import UploadCsvFile
from myflaskbackend.resources.figures import PlotDataPoint
from myflaskbackend.utils.configurations import api_settings

import threading
import os


app = Flask(__name__)
# app.config.from_pyfile('the-config.cfg')
# mongo = PyMongo(app)
# mongo = MongoEngine(app)
api = Api(app)

# # This will run at the start of Flask application
# with app.app_context():
#     # Runs MongoDB on a separate Thread
#     def thread_function(dbpath):
#         os.system('mongod ' + '--dbpath ' + '"' + dbpath + '"')
#
#     mongo_thread = threading.Thread(target=thread_function, args=(api_settings['MONGO_DB_PATH'], ), daemon=True)
#     print("Main    : before running thread")
#     mongo_thread.start()
#     print("Main    : wait for the thread to finish")


class RootDir(Resource):
    def get(self):
        return jsonify({'my_root_resource': "root node"})


class MultiplicateData(Resource):
    def get(self):
        data = request.form.to_dict(flat=False)
        print(data)
        # print('result: ', num*10)
        # return {'result': num*10, 'another_key': 'javaporco'}


api.add_resource(RootDir, '/')
api.add_resource(PlotDataPoint, '/plotdatapoint/<int:num>')
api.add_resource(UploadCsvFile, '/uploadcsvfile')
api.add_resource(MultiplicateData, '/multiplicate/<int:num>')


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
