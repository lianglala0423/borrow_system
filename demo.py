from flask import Flask, render_template, redirect, url_for, session, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, SelectField
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

class Config(object):
    """
        把要配置的參數都包在這個類別
    """
    # sqlalchemy 的配置參數: 要連去哪個資料庫
    POSTGRES = {
        'user': 'yuchen',
        'password': 'ilove5566',
        'db': 'flask',
        'host': 'localhost',  
        'port': '5432'
    }
    SQLALCHEMY_DATABASE_URI = 'postgresql://%(user)s:%(password)s@%(host)s:%(port)s/%(db)s' % POSTGRES
    
    # 令 sqlalchemy 自動追蹤資料庫
    # SQLALCHEMY_TRACE_MODIFICATIONS = True
    SQLALCHEMY_ECHO = True

# 把設置好的參數導入 flask 網路應用 ( web app ) 中
app.config.from_object(Config)

# 創建資料庫 sqlalchemy 工具物件
db = SQLAlchemy(app)

# 建立資料庫模型類
# 繼承 db.Model   
class ProductInfo(db.Model):
    """ 
        借用品項資訊
        表名: product_info
        schema: flask_borrow_system 
        欄位:
            product_id（pk): str
            product_name: str
            product_category: str
            status: boolean
            rate: float
            borrow_uid: str
            borrow_uname: str
            borrow_time: DateTime
    """
    __tablename__ = 'product_info' # 指名資料庫table名稱
    
    __table_args__ = {
        'schema': 'flask_demo' # 指定資料庫schema 
    }

    product_id = db.Column(db.String(64), primary_key=True)
    product_name = db.Column(db.String(64), nullable=False)
    product_category = db.Column(db.String(64), nullable=False)
    status = db.Column(db.Boolean)
    rate = db.Column(db.Float)
    
    borrow_uid = db.Column(db.String(16), primary_key=True)
    borrow_uname = db.Column(db.String(16))
    borrow_time = db.Column(db.DateTime, primary_key=True)
    return_time_pre = db.Column(db.DateTime)
    return_time = db.Column(db.DateTime)
    comment = db.Column(db.String(500))
    
class RegistForm(FlaskForm):
    user = StringField(u"員工編號", validators=[DataRequired(message=u"請輸入正確員工編號")])
    uname = StringField(u"員工名稱", validators=[DataRequired(message=u"請輸入正確員工編號")])
    item_no = StringField(u"物品編號", validators=[DataRequired(message=u"請輸入正確物品編號")])
    item_name = StringField(u"物品名稱", validators=[DataRequired(message=u"請輸入正確物品名稱")])
    item_cat = SelectField(u"物品類別", choices=[(1,'電腦'), (2,'投影機')])
    submit = SubmitField(u"Submit")

@app.route("/", methods=['POST', 'GET'])
def index():
    form = RegistForm()
    if form.validate_on_submit():
        session['borrow_uid'] = form.user.data
        session['borrow_uname'] = form.uname.data
        session['product_id'] = form.item_no.data
        session['product_name'] = form.item_name.data
        session['product_category'] = form.item_cat.data
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
    session['borrow_time'] = datetime.now()
    dt = format_datetime(session['borrow_time'])
    warning = ''
    if request.method == 'POST':
        day = request.values.get('borrow_days')
        item_code = request.values.get('item_code')
        if day != "":
            if item_code == session['product_id']:
                session['return_time_pre'] = session['borrow_time'] + timedelta(days=int(day))
                session['status'] = True
                # 寫入資料庫
                data = ProductInfo(
                    product_id = session['product_id'],
                    product_name = session['product_name'],
                    product_category = session['product_category'],
                    status = session['status'],
                    borrow_uid = session['borrow_uid'],
                    borrow_uname = session['borrow_uname'],
                    borrow_time = session['borrow_time'],
                    return_time_pre = session['return_time_pre']
                )
                db.session.add(data)
                db.session.commit()
                return redirect(url_for("borrow_result"))
            else:
                warning = '物品編號不正確，請確認您借用的物品。'
        else:
            warning = '請確實輸入借用天數。'
    return render_template("borrow_submit.html", borrow_dt_info=dt, warn=warning)

@app.route("/borrow_result")
def borrow_result():
    dt = format_datetime(session['return_time_pre'])
    return render_template("borrow_result.html", return_dt=dt)

@app.route("/return")
def returnobj():
    return render_template("return.html")

@app.route("/return_submit", methods=['POST', 'GET'])
def return_submit():
    # 測試用
    borrow = db.session.query(ProductInfo).\
        order_by(ProductInfo.borrow_time).\
        filter(ProductInfo.borrow_uid == session['borrow_uid']).\
        filter(ProductInfo.status == True).first()
    if borrow:
        session['product_id'] = borrow.product_id
        session['product_name'] = borrow.product_name
        session['borrow_uid'] = borrow.borrow_uid
        session['borrow_uname'] = borrow.borrow_uname
        session['borrow_time'] = borrow.borrow_time
        session['return_time_pre'] = borrow.return_time_pre
        dt = format_datetime(session['borrow_time'])
        rdt = format_datetime(session['return_time_pre'])
        warning = ''
        if request.method == 'POST':
            item_code = request.values.get('item_code_r')
            if session['product_id'] == item_code:
                session['return_time'] = datetime.now()
                # update database
                borrow.return_time = session['return_time']
                borrow.status = False
                borrow.rate = request.values['rate']
                borrow.comment = request.values['comment']
                db.session.commit()
                return redirect(url_for("return_result", result='valid'))
            else:
                warning = '物品編號不正確，請確認您歸還的物品。'
        return render_template("return_submit.html", borrow_dt_info=dt, return_dt_info=rdt, warn=warning)
    else:
        return redirect(url_for("return_result", result='no_borrow'))

@app.route("/return_result/<result>", methods=['POST', 'GET'])
def return_result(result):
    res = []
    if result == 'valid':
        # print結果
        rdt_res = format_datetime(session['return_time'])
        res.append(f"{session['borrow_uid']} {session['borrow_uname']} 恭喜您歸還成功！")
        res.append(f"歸還時間為：{rdt_res}")
    else:
        res.append(f"{session['borrow_uid']} {session['borrow_uname']} 您好")
        res.append(f"您沒有須歸還的物品")
    return render_template("return_result.html", result=res)

@app.route("/login", methods=['POST', 'GET'])
def login():
    return render_template("login.html")

if __name__=="__main__":
    app.run(debug=True)
    # db.drop_all()
    # db.create_all()
