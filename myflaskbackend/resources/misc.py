from flask import request
from flask_restful import Resource


class MultiplicateData(Resource):
    def get(self):
        data = request.form.to_dict(flat=False)
        print(data)
        # print('result: ', num*10)
        # return {'result': num*10, 'another_key': 'javaporco'}
