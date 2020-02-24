from flask import Flask, request, jsonify
from flask_restful import Resource, Api

from myflaskbackend.resources.data import StoreCsvData
from myflaskbackend.resources.figures import PlotDataPoint


app = Flask(__name__)
api = Api(app)


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
api.add_resource(StoreCsvData, '/storecsvdata')
api.add_resource(MultiplicateData, '/multiplicate/<int:num>')


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
