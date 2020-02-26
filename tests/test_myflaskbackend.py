from myflaskbackend import my_app
import pytest
import json
from pathlib import Path
import os


# fixture function to only be invoked once per test module (the default is to invoke once per test function)
@pytest.fixture(scope='module')
def client():
    my_app.app.config['TESTING'] = True
    with my_app.app.test_client() as client:
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


# The request fixture is a special fixture providing information of the requesting test function
def test_upload_csv_file(client, request):
    """POST csv file to backend"""
    file_path = Path(request.fspath).parent / 'data_tests/dummy_data.csv'
    with open(str(file_path), 'rb') as f:
        rv = client.post(
            '/uploadcsvfile',
            data={'client_file': f},
        )

    assert rv.status == "200 OK"
    assert rv.status_code == 200
    assert 'dummy_data.csv' in rv.data.decode()
