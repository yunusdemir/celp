# let the file import files from upper folder
import inspect
import os
import sys

import pandas as pd

# get absolute path
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from data import Data

TEST_DATA_DIR = os.path.dirname(os.path.abspath(__file__)) + "/data/"
CITIES = ["faketown"]

data = Data(TEST_DATA_DIR)


def test_load_cities():
    assert data.load_cities(), CITIES


def test_load():
    assert data.load(CITIES, "business")[CITIES[0]][0]["business_id"], "-MsRvdPnuw6QuLn5Vxjruw"
    assert data.load(CITIES, "checkin")[CITIES[0]][0]["business_id"], "-ak1fx5L9cNjUE56as12MA"
    assert data.load(CITIES, "review")[CITIES[0]][0]["review_id"], "yO9uwcDlzcFBpp6xSq_wOg"
    assert data.load(CITIES, "tip")[CITIES[0]][0]["user_id"], "xtwoOTTOuZrXj4GQtsueuA"
    assert data.load(CITIES, "user")[CITIES[0]][0]["user_id"], "NfU0zDaTMEQ4-X9dbQWd9A"


def test_get_business():
    assert data.get_business(CITIES[0], "-MsRvdPnuw6QuLn5Vxjruw")["name"], "Brian's Furniture"


def test_get_reviews():
    assert len(data.get_reviews(CITIES[0], n=1)[0]["review_id"]), len("ZrQ6PqgZZOcaH8pDlil1ww")
    assert data.get_reviews(CITIES[0], business_id="9jgZh0zCchGlMTKMh_ZV2Q", n=1)[0][
        "review_id"], "_8S9VPiyg2nar6IAU7n2xw"
    assert data.get_reviews(CITIES[0], user_id="b4M0dRgS26N4iH8agQ-3Nw", n=1)[0]["review_id"], \
        "nicnl-hHiH7Wcv3XQc6JAQ"
    assert data.get_reviews(CITIES[0], business_id="KR2kRmHnRCaNzOUEGoB25w",
                            user_id="bJ1ir7YZ-e-cigMahFLEIw", n=1)[0]["review_id"], \
        "HzD24-WZ8pzGGOZeN_ktIA"


def test_get_user():
    assert data.get_user("Cara")["user_id"], "NfU0zDaTMEQ4-X9dbQWd9A"
    assert data.get_user("Cara")["useful"], 10719


def test_dict_to_dataframe():
    assert type(data.dict_to_dataframe(data.USERS)), dict
    assert type(data.dict_to_dataframe(data.USERS)[data.CITIES[0]]), pd.DataFrame

    df_data = data.dict_to_dataframe(data.USERS, ["user_id", "name"])[data.CITIES[0]]
    assert df_data[df_data.name == "Cara"].user_id.to_string(), "NfU0zDaTMEQ4-X9dbQWd9A"

    test_cities = [city for city in data.CITIES if city.lower() == "faketown"]
    assert CITIES[0], test_cities[0]

    df_data = data.dict_to_dataframe(data.USERS, cities=test_cities)[test_cities[0]]
    assert df_data[df_data.name == "Richard"].user_id.to_string(), "zr2ARlz9CnCi3NKKjs12Jw"
