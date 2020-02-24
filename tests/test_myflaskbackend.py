from myflaskbackend import myflaskbackend
import pytest
import json
import os


# fixture function to only be invoked once per test module (the default is to invoke once per test function)
@pytest.fixture(scope='module')
def client():
    myflaskbackend.app.config['TESTING'] = True
    with myflaskbackend.app.test_client() as client:
        # with flaskr.app.app_context():
        #     flaskr.init_db()
        yield client
    # Anything after yield will be executed at the end of tests
    # close processes...
    #delete temporary files...


def test_get_root_dir(client):
    """GET app root directory"""
    rv = client.get('/')
    data_string = rv.data.decode('utf8')
    data_json = json.loads(data_string)

    assert data_json['my_root_resource'] == "root node"
