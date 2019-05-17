from recommender import Recommender

rec = Recommender()


def mse(predicted_ratings):
    """Computes the mean square error between actual ratings and predicted ratings

    Arguments:
    predicted_ratings -- a dataFrame containing the columns rating and predicted rating
    """
    diff = predicted_ratings['stars'] - predicted_ratings['predicted stars']
    return (diff ** 2).mean()


def item_based_filtered(user_id):
    return rec.predict_rating(user_id, 4)


def mse_item_based():
    for city in rec.data.CITIES:
        mse_list = [mse(item_based_filtered(user["user_id"])) for user in rec.data.USERS[city]]
        print(min(mse_list), max(mse_list), sum(mse_list)/len(sum_list))


mse_item_based()
