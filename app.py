import data
from recommend import recommend

from copy import deepcopy
from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/business/<city>/<id>")
def business(city, id):
    business = deepcopy(data.get_business(city.lower(), id))
    business["stars"] = int(float(business["stars"]) * 2)

    reviews = deepcopy(data.get_reviews(city=business["city"].lower(), business_id=business["business_id"]))
    for review in reviews:
        review["stars"] = int(float(review["stars"]) * 2)

    recommendations = deepcopy(recommend(business_id=id, n=10))
    for recommendation in recommendations:
        assert "business_id" in recommendation
        assert "stars" in recommendation
        recommendation["stars"] = int(float(recommendation["stars"]) * 2)
        assert "name" in recommendation
        assert "city" in recommendation
        assert "address" in recommendation

    return render_template("business.html", business=business, recommendations=recommendations, reviews=reviews)

@app.route("/static/<path:path>")
def send_static(path):
    return send_from_directory("static", path)

if __name__ == "__main__":
    app.run(debug=True)
