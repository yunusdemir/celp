# let the file import files from upper folder
import inspect
import os
import sys

# get absolute path
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from data import Data

TEST_DATA_DIR = os.path.dirname(os.path.abspath(__file__)) + "/data/"
CITIES = ["faketown"]


def test_data_exists():
    Data.testing = True
    assert Data


data = Data(TEST_DATA_DIR)


def test_load_cities():
    assert data.load_cities(), CITIES


def test_load_business():
    assert data.load(CITIES, "business")[CITIES[0]][0]["business_id"], "-MsRvdPnuw6QuLn5Vxjruw"


def test_load_checkin():
    assert data.load(CITIES, "checkin")[CITIES[0]][0]["business_id"], "-ak1fx5L9cNjUE56as12MA"


def test_load_review():
    assert data.load(CITIES, "review")[CITIES[0]][0]["review_id"], "yO9uwcDlzcFBpp6xSq_wOg"


def test_load_tip():
    assert data.load(CITIES, "tip")[CITIES[0]][0]["user_id"], "xtwoOTTOuZrXj4GQtsueuA"


def test_load_user():
    assert data.load(CITIES, "user")[CITIES[0]][0]["user_id"], "NfU0zDaTMEQ4-X9dbQWd9A"


def test_get_business():
    assert data.get_business(CITIES[0], "-MsRvdPnuw6QuLn5Vxjruw")["name"], "Brian's Furniture"


def test_get_reviews_length():
    assert len(data.get_reviews(CITIES[0], n=1)[0]["review_id"]), len("ZrQ6PqgZZOcaH8pDlil1ww")


def test_get_reviews_by_business_id():
    assert data.get_reviews(CITIES[0], business_id="9jgZh0zCchGlMTKMh_ZV2Q", n=1)[0][
        "review_id"], "_8S9VPiyg2nar6IAU7n2xw"


def test_get_reviews_by_user_id():
    assert data.get_reviews(CITIES[0], user_id="b4M0dRgS26N4iH8agQ-3Nw", n=1)[0]["review_id"], \
        "nicnl-hHiH7Wcv3XQc6JAQ"


def test_get_reviews_by_user_id_and_business_id():
    assert data.get_reviews(CITIES[0], business_id="KR2kRmHnRCaNzOUEGoB25w",
                            user_id="bJ1ir7YZ-e-cigMahFLEIw", n=1)[0]["review_id"], \
        "HzD24-WZ8pzGGOZeN_ktIA"


def test_get_user():
    assert data.get_user("Cara")["user_id"], "NfU0zDaTMEQ4-X9dbQWd9A"
    assert data.get_user("Cara")["useful"], 10719
