from flask import Flask, render_template, redirect, url_for, session
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo

app = Flask(__name__)

# app.config["SECRET_KEY"] = 'SDFBUIOFAFDIUAV'

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/search")
def search():
    return render_template("search.html")

@app.route("/borrow")
def borrow():
    return render_template("borrow.html")

@app.route("/borrow_submit")
def borrow_submit():
    return render_template("borrow_submit.html")

@app.route("/borrow_result")
def borrow_result():
    return render_template("borrow_result.html")

@app.route("/return")
def returnobj():
    return render_template("return.html")

@app.route("/return_submit")
def return_submit():
    return render_template("return_submit.html")

@app.route("/return_result")
def return_result():
    return render_template("return_result.html")

@app.route("/login")
def login():
    return render_template("login.html")

if __name__=="__main__":
    app.run(debug=True)
