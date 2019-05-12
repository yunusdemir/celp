import inspect
import os
import sys

# get absolute path
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from app import app

TEST_DATA_DIR = os.path.dirname(os.path.abspath(__file__)) + "/data/"
CITIES = ["faketown"]


def test_app_exists():
    app.testing = True
    assert app

# def test_index():
#     with app.test_request_context():
#         client = app.test_client()
#         assert client.get(url_for('index')).status_code == 200
#
