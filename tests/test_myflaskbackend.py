from myflaskbackend import myflaskbackend
import pytest
import json
import os


@pytest.fixture
def client():
    myflaskbackend.app.config['TESTING'] = True
    with myflaskbackend.app.test_client() as client:
        # with flaskr.app.app_context():
        #     flaskr.init_db()
        yield client


def test_get_root_dir(client):
    """GET app root directory"""

    rv = client.get('/')
    data_string = rv.data.decode('utf8')
    data_json = json.loads(data_string)

    assert data_json['my_root_resource'] == "root node"
