from flask import Flask, render_template, make_response
from flask_restful import Api, Resource
from flask_pymongo import PyMongo
from flask_redis import FlaskRedis
from flask_login import LoginManager
# from flask_mongoengine import MongoEngine

# Globally accessible libraries
api = Api()
redis_store = FlaskRedis()
login_manager = LoginManager()
mongo = PyMongo()
# mongo = MongoEngine(app)


def create_app():
    """Construct the core application."""

    app = Flask(__name__)

    # Set configuration keys
    app.config.from_object('myflaskbackend.config.Config')
    if app.config['FLASK_ENV'] == 'testing':
        app.config.from_object('myflaskbackend.config.TestingConfig')
    elif app.config['FLASK_ENV'] == 'development':
        app.config.from_object('myflaskbackend.config.DevelopmentConfig')
    elif app.config['FLASK_ENV'] == 'production':
        app.config.from_object('myflaskbackend.config.ProductionConfig')

    # This will run at the start of Flask application
    with app.app_context():
        # Import resources
        from myflaskbackend.resources.forms import RegistrationPage, LoginPage
        from myflaskbackend.resources.misc import MultiplicateData
        from myflaskbackend.resources.data import UploadCsvFile, ConnectToDb
        from myflaskbackend.resources.auth import Login, Logout
        from myflaskbackend.resources.figures import PlotDataPoint

        # Set globally accessible values
        redis_store.app_config = app.config

        # Add some routes
        api.add_resource(RootDir, '/')
        api.add_resource(RegistrationPage, '/signup')
        api.add_resource(Login, '/login')
        api.add_resource(Logout, '/logout')
        api.add_resource(PlotDataPoint, '/plotdatapoint/<int:num>')
        api.add_resource(ConnectToDb, '/connecttodb')
        api.add_resource(UploadCsvFile, '/uploadcsvfile')
        api.add_resource(MultiplicateData, '/multiplicate/<int:num>')

        # Initialize plugins
        # mongo.init_app(app)
        login_manager.init_app(app)
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


class RootDir(Resource):
    def get(self):
        # redis_store = current_app.extensions['redis']
        # print(f'Hi! Current app env is: {redis_store.app_config["ENV"]}')
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('home.html'), 200, headers)
