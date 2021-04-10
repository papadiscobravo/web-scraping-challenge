# app.py

from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_db"
mongo =PyMongo(app)

# create route that renders index.html template
@app.route("/")
def index():
    mars = mongo.db.facts.find_one()
    return render_template("index.html", mars=mars)

@app.route("/scrape")
def scrape():
    # connect collection
    collection = mongo.db.facts
    results = scrape_mars.scrape_all()
    collection.update({}, results, upsert = True)
    return "success"

if __name__ == "__main__":
    app.run(debug=True)