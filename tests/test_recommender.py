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


def test_top_similarity():
    df = data.dict_to_dataframe(data.BUSINESSES[CITIES[0]], ["business_id", "categories"])
    business_id = df.business_id.head(1)[0]
    df = recommender.create_similarity_matrix_categories(df)

    assert len(recommender.top_similarity(df, business_id, 2)), 2
    assert recommender.top_similarity(df, business_id, 20), ['6nLb4ePbL2c7AeZDTckmxg',
                                                             '8GKs0ZQTD9m1ITausv4FFA',
                                                             '8x3rDQCKUJfnJSdsU_6Y3g',
                                                             'BKtpv_Fx7Z578bkG-voKKA',
                                                             'H1xnw6h6K7jP4lQfvI-jLg',
                                                             'K2wi5V-Ab9aYIGcl7AXCRQ',
                                                             'My2pi-5HgQVwdNbtRSzcXQ',
                                                             'SIdA020Wagb_3zeed7d7Cg',
                                                             'U5-jFBtvoxdQ0vrxeg3jvw',
                                                             'WF09vP1_hsxXYNoOaJrzOQ',
                                                             'a-dy79pezdj0bZeeDxdsnA',
                                                             'a8_n_O5Hk2mWkNfz47NfMA',
                                                             'czxvydFY73S95HZqOOK2uQ',
                                                             'kTe4nTTPZb6SODnxs1QXDg',
                                                             'mrQ60tOt_YGquGE2eIS7yw',
                                                             'pIBX_IBixagX-2AzFPl77g',
                                                             'vWzfFvSxZCjSWPoVFn6idw']
