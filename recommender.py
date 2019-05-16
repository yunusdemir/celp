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

        city = random.choice(self.data.CITIES) if not city else city

        if business_id is None:
            return_best = list()

            for _ in range(9):
                best_of_all = list()

                city = random.choice(self.data.CITIES)
                all_data = self.data.BUSINESSES[city]

                for item in all_data:
                    if item['stars'] >= 4 and item['review_count'] >= 15:
                        best_of_all.append(item)

                return_best.append(random.choice(best_of_all))
            return return_best

        elif business_id is not None:
            df = self.data.dict_to_dataframe(self.data.BUSINESSES[city],
                                             ["business_id", "categories"])
            matrix = self.create_similarity_matrix_categories(df)
            list_recommend = self.top_similarity(matrix, business_id)

            return_list = list()

            for b_id in list_recommend:
                return_list.append(self.data.get_business(city, b_id))

            return return_list

        return random.sample(self.data.BUSINESSES[city], n)

    def create_similarity_matrix_categories(self, df_data: pd.DataFrame) -> pd.DataFrame:
        """Create a similarity matrix for categories"""

        df = self.data.extract_categories(df_data)
        df_utility_categories = self.data.pivot_categories(df)

        npu = df_utility_categories.values
        m1 = npu @ npu.T
        m2 = m1 / np.diag(m1)
        m3 = np.minimum(m2, m2.T)
        return pd.DataFrame(m3, index=df_utility_categories.index,
                            columns=df_utility_categories.index)

    @staticmethod
    def top_similarity(df: pd.DataFrame, business_id: str, n: int = 10) -> list:
        sim_series = df.loc[business_id]
        sim_series = sim_series.sort_values(ascending=False).drop(business_id)

        sim_list = [item for item in sim_series.index if sim_series[item] >= 0.25]

        if len(sim_list) > n:
            sim_list = random.sample(sim_list, n)

        return sim_list
