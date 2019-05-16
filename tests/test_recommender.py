# let the file import files from upper folder
import inspect
import os
import sys

# get absolute path
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from recommender import Recommender

TEST_DATA_DIR = os.path.dirname(os.path.abspath(__file__)) + "/data/"
CITIES = ["faketown", "mocktown"]


def test_recommender_exists():
    Recommender.testing = True
    assert Recommender


recommender = Recommender(TEST_DATA_DIR)
data = recommender.data


def test_create_similarity_matrix_categories():
    df = data.dict_to_dataframe(data.BUSINESSES[CITIES[0]], ["business_id", "categories"])
    df_sim = recommender.create_similarity_matrix_categories(df)

    test_column = df_sim[df_sim.columns[0]].name

    assert df_sim.loc[test_column, test_column], 1.0
