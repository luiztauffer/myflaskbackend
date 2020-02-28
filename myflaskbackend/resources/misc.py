from flask import request, jsonify, make_response, current_app
from flask_restful import Resource


class RootDir(Resource):
    def get(self):
        redis_store = current_app.extensions['redis']
        print(f'Hi! Current app env is: {redis_store.app_config["ENV"]}')
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
            msg = f'Login failed for user: {user_name}'
            print(msg)
            return make_response(msg, 401)


class MultiplicateData(Resource):
    def get(self):
        data = request.form.to_dict(flat=False)
        print(data)
        # print('result: ', num*10)
        # return {'result': num*10, 'another_key': 'javaporco'}
