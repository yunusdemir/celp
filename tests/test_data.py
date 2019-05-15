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
CITIES = ["faketown", "mocktown"]


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


def test_pivot_stars_duplicate_data():
    df = data.pivot_stars(data.CITIES[0])
    assert df[df.duplicated()].empty

def test_get_city():
    assert data.get_city("CeA_KfaDZq1huASNRe_MAg"), ['faketown', 'mocktown']
    assert data.get_city("Vsp7ncZY-sm1gzkyNcld_A"), ['mocktown']
    assert data.get_city("8KeHUYvc5HVzex6XhP6Fug"), ['faketown']

def test_get_friends():
   assert data.get_friends("Vsp7ncZY-sm1gzkyNcld_A"), ['KbduTqKt1AuQ-YJaKD_C7A', 'cgG1Gf8nhS2WlVCe-EUVMQ', 'u-F1PfnPgWbVBzQe4a3DNA', 'UieSEe9S5e9OOrwZkeXQNQ', 'YOQFZW4L_6U98gIu_MiPOA', 'EZ1xB7-tNA9Rk0UwYR6jrw', 'P9SzYFU_gsb2kz9gs6gZIQ', 'zMuoIkLntiVGKR0oGWxhCg', 'TVMhp7IZmG-yk6bZo5LlxQ', 'lDCdZzcWuIbGa3D18Lvmsg', 'ybsVt_8I5scPdXU_DTvzWg', 'i12QU950hek3ReJoWcq3jg', 'sO0c1oNjaESBdnVbkLzQ9A', 'WWBpma7wXT64tH1MWMIpQg', '48GKxvCCE0AVM1CFMhxs6Q', 'ZlwaW1me_3iq8uHzdgYIdg', 'oF_1LC0zuzXD_ef-C7wLYg', 'Xtif85mmu024k34PxUpmuA', '7aNFwP5QJZYU-vKPf55myQ', 'XkJQwZIGikBZn9_zqW1wDw', 'ucPd8XDHTvtFLZYg7ZJ6Hg', 'rbEcEj3B0ghF6zjHkExBFw', '3_jU6ulXkdQckSwQJjYUnw', 'AocCwPeEvpEQ6_D6cEyooA', 'GAmNZcD_WMT42ZRFM6JKAA', 'TuBywMpiJbEix5b5j6bgkA', 'Q030a12hDz_j0xnIpF5F-A', 'DA7LdReRpZ4PO3MkcKyBNQ', 'wiexA3xfvRkniy-4_5uQVg', '6uNn2ApBB_rTUK8JrHA4BQ', 'ikBp8rXvo1yEcrHnixDP7A', 'D0X0Gvr5Va7LvNAxbrOm2w', 'K3MvRJ3Erk1qMRA7bi0u-g', '8b6_gjxPG_yo8GsEwWDegQ', 'ZsP1qLUKc4EeGSkCnDkB_w', 'sdgk2YP5YLYfTamjqS0NGA', 'Xk3g8xYP_9N03j0vuZMCcQ', 'Av8KQ40S7yUSwwH4xAGbxw', 'qt5_SUXXvsoi0ifuabVscg', 'vPjbf6jyKP8eJUMtVg2IhQ', 'xn2Hx_PRyvOdtD1nIGe21w', 'eaw1c9XK9z1Ush3RlbNXBw', 'xZpQEd-dmwP9Skc-64YTgQ', 'UY-ZR1euTr131Mc3M-dRyw', 'D96hPkulOXSAaCEJkG8Uug', '66O30REf4Lyx7Ge0x9M_qA', 'vdjvOXMnQii5RG0XqO0rMA', '2VJgxZ-uyggq2slogYbzPA', 'BgO5JP4IYCUOjN5aZoStnQ', 'pSfQYCwXWuyo2bvWe4847w', 'Znmjg0FaPHxk2UimZG4QQg', '4l97YDkTBwZ2XLsw9wRVfQ', 'LGi6LhMW4LOkE2lawTdKIQ', 'BWEZfoESq3aq5pPjHMDhFQ', 'VGY69c67ZYeQyTjI-4GJqg', 'btNEUpTHccwBgLg6_nj7fA', 'plBE7mfqzRG03gQL3n4UBw', '6_D8QeQ2FCFM2vWF-jvseQ', 'iR3b537ndNGp7Fjf6M1ssg', 'jeSBtVyzZ1sGDdSDB2Nqyw', 'lk69FV78gL25Gp71MZFzFQ', 'N__pLD26scz-GRnzgXNiCg', 'nUiMyCjYvbXvDg3CBFpE2Q', 'ZH0OnSKSOq3kVKpfLjPmzw', '23NwM0rU7FESoYtvR9KwRg', 'UggUpylkigOE8ZYiX2VENQ', 'zqhaZe9Nd0fRPimOoiYdzA', 'ApRbVjWyAqAVFPefTLrZoQ', 'gNmWgMJjd_QntFBRND2r3w', 'RNmX7dhUThe0zNtfN9kzIA', 'XLIFaJTIVpAWgToOIiLKmQ', 'qWf07kJCWUpvEe7-GNROLQ', 'xpcJ6ABw4yoz4qLipDIkeg', 'qrYUr9zj59t5csIv30qv7w', 'mVlr9b3L3MWX2JD8GYtRmA', 'JRhpBCPgBq9ORHRaQj1gGA', 'ITDnrN4fmd9aSmGBytpOVA', 'ZhOANc7XlVP20Jcp53N4Gw', 'ruATaByZAE0Vl6fLRVb0fw', 'hexAkBNzS_L6-6rDX67faQ', 'I13MZ0TwwPHbQ2SkA5qQ0g', 'F1HnUUaAvo_skt3PtS2e8g', 'qv3udgDrFmsuYC5DkX4oRg', 'uJcFyGOeHkfxhNqMG5NLqg', 'auSvhRLIWVq_3Q6xPrS-Vw', 'cm5OSNHki5vTSPiYd5Hymw', 'EzimoALb-6Z7zFIkyBFSww', 'bJlbZ2n5G3wxQ_nh2CYNhw', 'a0BZL6agnLJR1DbjiXMp7Q', 'VGP36NFedUTHLPW_pD52Rg', 'Ct6nj9oBEZ9p-24nvS2uvQ', 'vc6DilDAGnB34_ULQyVfXQ', 'G_AKAgQIzPp0otTcDWPW-Q', 'c087QJ_STLC-lT2vHLaj_A', 'zVvK5nBRxgHfwQzOf21VhQ', 'QjqPqD0gnLsDw3WUDNSM_w', '9zttF7hHAFwzGklK2U-BhQ', 'Kt1wk6XGCSK0JNgU24rmfw', '4XLzw3DeQO72fejOuZ_QiA', 'Ni0VZ6gay_6c1xQrOmcjnw']
   assert data.get_friends("ITb61jq8zJZiXoZYB5wK2Q"), ['MQnhILGY3p4ptpmKytq0PA', 'bD2mQE0AFv8At9IFUfuXwA', '-VzKNDa6_Jxw7GBjYBAc3g']

def test_pivot_stars_newest_review():
    """Uses a manufactured review, errors with normal dataset"""
    df = data.pivot_stars(data.CITIES[0])
    assert df.loc["KR2kRmHnRCaNzOUEGoB25w", "CnEBX4feg_Tlsyk3QlHC7w"], 2.0