from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from flask_pymongo import PyMongo
# from flask_mongoengine import MongoEngine

from myflaskbackend.resources.data import UploadCsvFile, ConnectToDb
from myflaskbackend.resources.figures import PlotDataPoint
from myflaskbackend.utils.configurations import api_settings

from pathlib import Path
import json


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


class Login(Resource):
    """
    Login for registered users.

    $ curl -i -X POST -F -d "username=value1&password=value2" http://localhost:5000/login
    """
    def post(self):
        # Load users credentials to compare when login attempts
        users_data_path = Path(__file__).parent.parent.absolute() / 'users_data.json'
        with open(users_data_path) as json_file:
            users_data = json.load(json_file)

        # Test user supplied credentials
        form = request.form
        user_name = form['username']
        user_pass = form['password']
        match_list = [user_name == user['user_name'] for user in users_data['all_users']]
        login_success = False
        if any(match_list):
            # If username is correct
            user_ind = match_list.index(True)
            if user_pass == users_data['all_users'][user_ind]['password']:
                # If password is also correct
                login_success = True

        if login_success:
            msg = f'Login successful! Welcome {user_name}!'
            print(msg)
            return make_response(msg, 200)
        else:
            msg = f'Login failed for user: {user_name}')
            print(msg)
            return make_response(msg, 401)


class MultiplicateData(Resource):
    def get(self):
        data = request.form.to_dict(flat=False)
        print(data)
        # print('result: ', num*10)
        # return {'result': num*10, 'another_key': 'javaporco'}


api.add_resource(RootDir, '/')
api.add_resource(Login, '/login')
api.add_resource(PlotDataPoint, '/plotdatapoint/<int:num>')
api.add_resource(ConnectToDb, '/connecttodb')
api.add_resource(UploadCsvFile, '/uploadcsvfile')
api.add_resource(MultiplicateData, '/multiplicate/<int:num>')


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
