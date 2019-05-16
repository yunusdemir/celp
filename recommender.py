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

        if business_id is not None:
            df = self.data.dict_to_dataframe(self.data.BUSINESSES[city], ["business_id", "categories"]) 
            matrix = self.create_similarity_matrix_categories(df)
            list_recommend = self.top_similarity(matrix, city, business_id)

            return_list = list()

            for b_id in list_recommend:
                return_list.append(self.data.get_business(city, b_id))

            return return_list
        
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

    def top_similarity(self, df: pd.DataFrame, city, business_id, n: int = 100) -> list:

        matrix = self.create_similarity_matrix_categories(self.data.dict_to_dataframe(self.data.BUSINESSES[city], ["business_id", "categories"]))

        sim_series = df.loc[business_id]
        sim_series = sim_series.sort_values(ascending = False).drop(business_id)

        sim_list = []
        
        for item in sim_series.index:
            if sim_series[item] >= 0.25:
                sim_list.append(item)

        return sim_list
