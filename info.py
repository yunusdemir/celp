from data import Data
import matplotlib.pyplot as plt
import numpy as np

class Info:
    
    def reviews_density(self, city) -> int:
        """
        Calculates the density of reviews in given city
        """
        return len(Data().REVIEWS[city]) / (len(Data().BUSINESSES[city]) * len(Data().USERS[city]))

    def review_graph(self, city):
        """
        Plots graph with user_id on x-axis and number of 
        reviews on y-axis
        """
        review_count_sorted = sorted(Data().USERS[city], key=lambda i: i['review_count'])
        value_dict = {user['user_id']:user['review_count'] for user in review_count_sorted}
        plt.bar(value_dict.keys(), value_dict.values())
        plt.ylim([0, 1500])
        return plt.show()

    