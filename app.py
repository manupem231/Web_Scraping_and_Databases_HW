from bs4 import BeautifulSoup
import requests
import pymongo
from pymongo import MongoClient
from splinter import Browser
import time
import pandas as pd

from flask import Flask, render_template, jsonify, redirect
from flask_pymongo import PyMongo
import Mission_to_Mars

app = Flask(__name__)

mongo = PyMongo(app)


@app.route('/')
def index():
    mission_to_mars = mongo.db.mission_to_mars.find_one()
    return render_template('index.html', mars=mission_to_mars)


@app.route('/scrape')
def scrape():
    mission_to_mars = mongo.db.mission_to_mars
    data = Mission_to_Mars.scrape()
    mission_to_mars.update({}, data, upsert=True)
    return redirect("http://localhost:5000/", code=302)


if __name__ == "__main__":
    app.run(debug=True)