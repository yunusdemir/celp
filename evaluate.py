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
    return rec.predict_rating(user_id, "westlake", 4)


def mse_item_based():
    for city in rec.data.CITIES:
        for user in rec.data.USERS[city]:
            print(mse(item_based_filtered(user["user_id"])))


mse_item_based()
