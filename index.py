from flask import Flask, render_template, url_for, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from db_final import ProductInfo, HistRecord # 匯入某個 class (某個資料表)
from datetime import datetime, timedelta
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
# 必須自己設置一個安全碼
app.config['SECRET_KEY'] = 'SDFASGFSDRGDAF6G3516516A1RSDFGARE5'

# 定義表單的模型類別
class Config(object):
    """
    把要配置的參數都包在這個類別
    """
    # sqlalchemy 的配置參數: 要連去哪個資料庫
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://DB_USER:PASSWORD@HOST/DATABASE'
    POSTGRES = {
        'user': 'yuchen',
        'password': 'ilove5566',
        'db': 'flask',
        'host': 'localhost',  
        'port': '5432'
    }
    SQLALCHEMY_DATABASE_URI = 'postgresql://%(user)s:%(password)s@%(host)s:%(port)s/%(db)s' % POSTGRES
    print(SQLALCHEMY_DATABASE_URI) 
    # 令 sqlalchemy 自動追蹤資料庫
    SQLALCHEMY_TRACE_MODIFICATIONS = True

# 把設置好的參數導入 flask 網路應用 ( web app ) 中
app.config.from_object(Config)
# 創建資料庫 sqlalchemy 工具物件
db = SQLAlchemy(app)

class RegistForm(FlaskForm):
    user = StringField(u"員工編號", validators=[DataRequired(message=u"請輸入正確員工編號")])
    uname = StringField(u"員工名稱", validators=[DataRequired(message=u"請輸入正確員工編號")])
    submit = SubmitField(u"Submit")

@app.route('/', methods=['GET', 'POST'])
def login():
    form = RegistForm()
    if form.validate_on_submit():
        session['borrow_uid'] = form.user.data
        session['borrow_uname'] = form.uname.data
        return redirect(url_for('index', uid=session['borrow_uid']))
    return render_template('test_result.html', form=form)

@app.route('/index', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/search/<uid>', methods=['GET','POST'])
def search(uid):
    # 要從 form 表單拿到資料，進行資料庫查詢操作。
    name = request.form.get('name')  #需要查詢的內容, 傳回來的東西為 .html 中 attribute 為 name 的那個輸入框之值
    if name is None:
        name = " "
    #查詢跟 product_category 有關的資料，返回結果為列表
    quotes = ProductInfo.query.filter(ProductInfo.product_category.like("%"+name+"%") if name is not None else "").all()
    if request.method == "POST":
        submit = request.values.get('btn')
        session['product_id'] = request.values.get('product_id')
        session['product_category'] = request.values.get('product_category')
        session['product_name'] = request.values.get('product_name')
        # 如果值為null 會回傳""
        session['cur_rate'] = request.values.get('rate') \
                                if request.values.get('rate') != "" else None
        print(session)
        # if submit == "借用":
        #     # 確認登入狀態
        #     if len(session) != 0:
        #         return redirect(url_for('borrow_submit', warn='submit', count=0))
        #     else:
        #         return redirect(url_for('login', action='borrow'))
        # elif submit == "歸還":
        #     if len(session) != 0:
        #         return redirect(url_for('sendback_submit', warn='submit', count=0))
        #     else:
        #         return redirect(url_for('login', action='return'))
        if submit == "借用":
            return redirect(url_for('borrow_submit', uid=uid, warn='submit', count=0))
        elif submit == "歸還":
            return redirect(url_for('sendback_submit', uid=uid, warn='submit', count=0))
    return render_template('search.html', quotes=quotes) # 將查詢結果返回到前端

@app.route('/borrow/<uid>', methods=['GET','POST'])
def borrow(uid):
    quotes = ProductInfo.query.filter_by(in_store=True).all()
    if request.method == "POST":
        session['product_id'] = request.values.get('product_id')
        session['product_category'] = request.values.get('product_category')
        session['product_name'] = request.values.get('product_name')
        session['cur_rate'] = request.values.get('rate') \
                                if request.values.get('rate') != "" else None
        # # 確認登入狀態
        # if 'borrow_uid' in session.keys() or session['borrow_uid']:
        #     return redirect(url_for('borrow_submit', warn='submit', count=0))
        # else:
        #     return redirect(url_for('login', action='borrow'))
            return redirect(url_for('borrow_submit', warn='submit', count=0))
        else:
            return redirect(url_for('login', action='borrow'))
    return render_template('borrow.html', quotes=quotes)

@app.route('/sendback', methods=['GET', 'POST'])
def sendback():
    # borrow_uid = 'esb001' # borrow_uid = 要去接 session 帶入的員編
    # quotes = ProductInfo.query.filter_by(borrow_uid=borrow_uid).all()
    quotes = ProductInfo.query.filter_by(borrow_uid=session['borrow_uid']).all()
    if request.method == "POST":
        session['product_id'] = request.values.get('product_id')
        session['product_category'] = request.values.get('product_category')
        session['product_name'] = request.values.get('product_name')
        session['cur_rate'] = request.values.get('rate') \
                                if request.values.get('rate') != "" else None
        return redirect(url_for('sendback_submit', warn='submit', count=0))
    return render_template('return.html', quotes=quotes)
    # return render_template('return.html')

# @app.route('/borrow_submit', methods=['GET', 'POST'])
@app.route('/borrow_submit/<int:count>/<warn>', methods=['GET', 'POST'])
def borrow_submit(warn, count):
    session['borrow_time'] = datetime.now()
    # dedault 顯示預計歸還日期為借用日 + 1 day ---> 傳到前端
    exp_time = str(session['borrow_time'] + timedelta(days=1))[:11]
    if warn == 'submit':
        warning = ''
    else:
        warning = warn

    if request.method == 'POST':
        session['expected_time'] = datetime.strptime(request.values.get('expected_time'), '%Y-%m-%d')
        code = request.values.get('barcode')
        # 失敗三次則跳轉failed頁面
        if count < 2:
            # 預計歸還日期需大於等於借用日期
            if session['expected_time'] >= session['borrow_time']:
                if code == session['product_id']:
                    session['in_store'] = False
                    # 寫入資料庫
                    # record
                    data_record = HistRecord(
                        product_id = session['product_id'],
                        product_name = session['product_name'],
                        product_category = session['product_category'],
                        in_store = session['in_store'],
                        borrow_uid = session['borrow_uid'],
                        borrow_uname = session['borrow_uname'],
                        borrow_time = session['borrow_time'],
                        expected_time = session['expected_time'],
                        ave_rate = session['cur_rate']
                    )
                    db.session.add(data_record)
                    db.session.commit()

                    return redirect(url_for("borrow_result", result='success'))
                else:
                    warning = '物品編號不正確，請確認您借用的物品。'
                    return redirect(url_for("borrow_submit", warn=warning, count=count+1))
            else:
                warning = '歸還日期不可小於借用日期，請確實輸入預計歸還時間。'
                session['expected_time'] = None
                return redirect(url_for("borrow_submit", warn=warning, count=count+1))
        else:
            return redirect(url_for("borrow_result", result='failed'))
    return render_template("borrow_submit.html", exp_time=exp_time, warn=warning)

@app.route('/sendback_submit/<int:count>/<warn>', methods=['GET', 'POST'])
def sendback_submit(warn, count):
    if warn == 'submit':
        warning = ''
    else:
        warning = warn
    # search hist record
    record = db.session.query(HistRecord).filter(HistRecord.borrow_uid == session['borrow_uid']).\
                                            filter(HistRecord.product_id == session['product_id']).\
                                            filter(HistRecord.in_store == False).first()
    session['borrow_time'] = record.borrow_time
    session['expected_time'] = record.expected_time
    if request.method == 'POST':
        return_code = request.values.get('barcode_r')
        if count < 2:
            if return_code == session['product_id']:
                session['return_time'] = datetime.now()
                # update recorded database
                record.return_time = session['return_time']
                record.in_store = True
                record.rate = request.values.get('rate')
                record.comment = request.values.get('comment')
                db.session.commit()
                return redirect(url_for("sendback_result", result='valid'))
            else:
                warning = '物品編號不正確，請確認您歸還的物品。'
                return redirect(url_for("sendback_submit", count=count+1, warn=warning))
        else:
            return redirect(url_for("sendback_result", result='failed'))
        
    # return render_template("return_submit.html", borrow_dt_info=dt, return_dt_info=rdt, warn=warning)
    return render_template('return_submit.html')

@app.route('/borrow_result/<result>', methods=['GET'])
def borrow_result(result):
    res = []
    if result == 'success':
        # info: update in_store True > False
        data_info = db.session.query(ProductInfo).\
                        filter(ProductInfo.product_id == session['product_id']).first()
        data_info.borrow_uid = session['borrow_uid']
        data_info.borrow_uname = session['borrow_uname']
        data_info.in_store = False
        data_info.borrow_time = session['borrow_time']
        db.session.commit()
        # print結果
        exp_time = str(session['expected_time'])[:11]
        res.append(f"{session['borrow_uid']} {session['borrow_uname']} 恭喜您借用成功！")
        res.append(f"預計歸還日期為：{exp_time}")
    else:
        res.append(f"{session['borrow_uid']} {session['borrow_uname']} 您好")
        res.append(f"錯誤次數已達３次，請確認您的借用流程是否正確。")
    session.clear()
    return render_template("borrow_result.html", result=res)
    # return render_template('borrow_result.html')

@app.route('/sendback_result/<result>', methods=['GET'])
def sendback_result(result):
    res = []
    if result == 'valid':
        # count average rate
        ave_rate = HistRecord.query.with_entities(func.avg(HistRecord.rate)).\
                            filter(HistRecord.product_id == session['product_id']).all()[0][0]
        # update product info database
        info = db.session.query(ProductInfo).\
                            filter(ProductInfo.product_id == session['product_id']).first()
        info.in_store = True
        info.borrow_uid = None
        info.borrow_uname = None
        info.borrow_time = None
        info.rate = ave_rate
        db.session.commit()
        # print結果
        return_time = str(session['return_time'])
        res.append(f"{session['borrow_uid']} {session['borrow_uname']} 恭喜您歸還成功！")
        res.append(f"歸還時間為：{return_time}")
    else:
        res.append(f"{session['borrow_uid']} {session['borrow_uname']} 您好")
        res.append(f"錯誤次數已達３次，請確認您的歸還流程是否正確。")
    session.clear()
    return render_template("return_result.html", result=res)
if __name__ == "__main__":
    app.run(debug=True)