from recommender import Recommender

rec = Recommender()


def mse(predicted_ratings):
    """Computes the mean square error between actual ratings and predicted ratings

    Arguments:
    predicted_ratings -- a dataFrame containing the columns rating and predicted rating
    """
    diff = predicted_ratings['rating'] - predicted_ratings['predicted rating']
    return (diff ** 2).mean()


def item_based_filtered():
    return rec.predict_rating("Vsp7ncZY-sm1gzkyNcld_A", "westlake")


def mse_item_based():
    return mse(item_based_filtered())


print(mse_item_based())
