# app.py

from flask import flask, render_template, redirect
from flask pymongo import pymongo
import scrape_mars

app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_db"
mongo =PyMongo(app)

@app.route/
