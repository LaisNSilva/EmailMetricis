# -*- coding: utf-8 -*-
"""
Created on Sat May 23 14:25:40 2020

@author: Fernando
"""

from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

    
if __name__ == "__main__":
    app.debug = True
    app.run(host = '0.0.0.0', port = 25565)