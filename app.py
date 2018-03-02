from bs4 import BeautifulSoup
import requests
import pymongo
from pymongo import MongoClient
from splinter import Browser
import time
import pandas as pd

from flask import Flask, render_template, jsonify, redirect
import pymongo
from flask_pymongo import PyMongo
import Mission_to_Mars


app = Flask(__name__)

mongo = PyMongo(app)


@app.route('/')
def index():
    mars = mongo.db.mars.find_one()
    return render_template('index.html', mars=mars)


@app.route('/scrape')
def scrape():
    mars = mongo.db.mars
    data = Mission_to_Mars.scrape()
    mars.update({}, data, upsert=True)
    return redirect("http://localhost:5000/", code=302)


if __name__ == "__main__":
    app.run(debug=True)