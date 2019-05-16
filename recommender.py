import random

import numpy as np
import pandas as pd

from data import Data


class Recommender:

    def __init__(self, data_directory="data"):
        self.data = Data(data_directory)

    def recommend(self, user_id=None, business_id=None, city=None, n=10):
        """
        Returns n recommendations as a list of dicts.
        Optionally takes in a user_id, business_id and/or city.
        A recommendation is a dictionary in the form of:
            {
                business_id:str
                stars:str
                name:str
                city:str
                adress:str
            }
        """
        if not city:
            city = random.choice(self.data.CITIES)
        return random.sample(self.data.BUSINESSES[city], n)

    def create_similarity_matrix_categories(self, df_categories: pd.DataFrame) -> pd.DataFrame:
        """Create a similarity matrix for categories"""

        df = self.data.extract_categories(df_categories)
        df_utility_categories = self.data.pivot_categories(df)

        npu = df_utility_categories.values
        m1 = npu @ npu.T
        m2 = m1 / np.diag(m1)
        m3 = np.minimum(m2, m2.T)
        return pd.DataFrame(m3, index=df_utility_categories.index,
                            columns=df_utility_categories.index)

    # def business_logged_in(self, user_id, business_id, city):
