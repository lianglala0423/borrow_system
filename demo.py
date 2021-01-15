from flask import Flask, render_template, redirect, url_for, session, request
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField
from wtforms.validators import DataRequired, EqualTo, InputRequired, Length, Optional, NumberRange
from flask_babel import Babel
from flask_babel import format_datetime, get_locale
from datetime import datetime, timedelta

app = Flask(__name__)

# session設定
app.config['SECRET_KEY'] = 'development' # 加密金鑰
# 時間格式設定
app.config['BABEL_DEFAULT_LOCALE'] = 'zh_TW'
app.config['BABEL_DEFAULT_TIMEZONE']='UTC'

babel = Babel(app)

class BorrowForm(FlaskForm):
    return_dt = IntegerField("借用天數", validators=[
                    Optional(), 
                    NumberRange(1, 7, "借用天數: %(min)s 至 %(max)s 天")])
    item_code = PasswordField("物品條碼", validators=[InputRequired()])
    submit = SubmitField("Submit")

class RegistForm(FlaskForm):
    user = StringField(u"員工編號", validators=[DataRequired(message=u"請輸入正確員工編號")])
    item_no = StringField(u"物品編號", validators=[DataRequired(message=u"請輸入正確物品編號")])
    item_name = StringField(u"物品名稱", validators=[DataRequired(message=u"請輸入正確物品名稱")])
    submit = SubmitField(u"Submit")

@app.route("/", methods=['POST', 'GET'])
def index():
    form = RegistForm()
    print ("here")
    if form.validate_on_submit():
        print('if')
        session['username'] = form.user.data
        session['item_no'] = form.item_no.data
        session['item_name'] = form.item_name.data
        return redirect(url_for("borrow_submit"))
    return render_template("test_result.html", form=form)

@app.route("/search")
def search():
    return render_template("search.html")

@app.route("/borrow")
def borrow():
    return render_template("borrow.html")

@app.route("/borrow_submit", methods=['GET', 'POST'])
def borrow_submit():
    session['borrow_dt'] = datetime.now()
    dt = format_datetime(session['borrow_dt'])
    warning = ''
    if request.method == 'POST':
        day = request.values['borrow_days']
        item_code = request.values['item_code']
        if day != "":
            if item_code == session['item_no']:
                session['return_dt_tmp'] = session['borrow_dt'] + timedelta(days=int(day))
                return redirect(url_for("borrow_result"))
            else:
                warning = '物品編號不正確，請確認您借用的物品。'
        else:
            warning = '請確實輸入借用天數。'
    return render_template("borrow_submit.html", borrow_dt_info=dt, warn=warning)

@app.route("/borrow_result")
def borrow_result():
    dt = format_datetime(session['return_dt_tmp'])
    return render_template("borrow_result.html", return_dt=dt)

@app.route("/return")
def returnobj():
    return render_template("return.html")

@app.route("/return_submit")
def return_submit():
    return render_template("return_submit.html")

@app.route("/return_result")
def return_result():
    return render_template("return_result.html")

@app.route("/login", methods=['POST', 'GET'])
def login():
    form = RegisterForm()
    if form.validate_on_submit():
        return redirect(url_for("index"))
    return render_template("login.html", form=form)

if __name__=="__main__":
    app.run(debug=True)
