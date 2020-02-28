from flask import Flask
from flask_restful import Api
from flask_pymongo import PyMongo
from flask_redis import FlaskRedis
# from flask_mongoengine import MongoEngine

from myflaskbackend.resources.data import UploadCsvFile, ConnectToDb
from myflaskbackend.resources.misc import RootDir, Login, MultiplicateData
from myflaskbackend.resources.figures import PlotDataPoint
from myflaskbackend.utils.configurations import api_settings


def create_app():
    """Construct the core application."""

    app = Flask(__name__)
    # app = Flask(__name__, instance_relative_config=False)
    # app.config.from_object('config.Config')
    # app.config.from_pyfile('the-config.cfg')

    # mongo = PyMongo(app)
    # mongo = MongoEngine(app)
    # api = Api(app)

    # Set globals
    api = Api()
    mongo = PyMongo()
    redis_store = FlaskRedis()

    # This will run at the start of Flask application
    with app.app_context():
        # Set global values
        redis_store.app_config = app.config
        # print(app.config)

        # Add some routes
        api.add_resource(RootDir, '/')
        api.add_resource(Login, '/login')
        api.add_resource(PlotDataPoint, '/plotdatapoint/<int:num>')
        api.add_resource(ConnectToDb, '/connecttodb')
        api.add_resource(UploadCsvFile, '/uploadcsvfile')
        api.add_resource(MultiplicateData, '/multiplicate/<int:num>')

        # Initialize globals
        # mongo.init_app(app)
        redis_store.init_app(app)
        api.init_app(app)

    return app

    #     # Runs MongoDB on a separate Thread
    #     def thread_function(dbpath):
    #         os.system('mongod ' + '--dbpath ' + '"' + dbpath + '"')
    #
    #     mongo_thread = threading.Thread(target=thread_function, args=(api_settings['MONGO_DB_PATH'], ), daemon=True)
    #     print("Main    : before running thread")
    #     mongo_thread.start()
    #     print("Main    : wait for the thread to finish")
