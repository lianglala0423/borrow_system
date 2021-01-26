#!/usr/bin/python
# -*- coding: utf-8 -*-

# db_demo.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from datetime import datetime, timedelta
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)

class Config(object):
    """
        把要配置的參數都包在這個類別
    """
    # sqlalchemy 的配置參數: 要連去哪個資料庫
    POSTGRES = {
        'user': 'postgres',
        'password': 'postgres',
        'db': 'postgres',
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
            in_store: boolean
            rate: float
            borrow_uid: str
            borrow_uname: str
            borrow_time: DateTime
            expected_time: DateTime
    """
    __tablename__ = 'product_info' # 指名資料庫table名稱
    
    __table_args__ = {
        'schema': 'flask_borrow_system' # 指定資料庫schema 
    }

    product_id = db.Column(db.String(64), primary_key=True)
    product_name = db.Column(db.String(64), nullable=False)
    product_category = db.Column(db.String(64), nullable=False)
    in_store = db.Column(db.Boolean)
    rate = db.Column(db.Float) # x
    
    borrow_uid = db.Column(db.String(16))
    borrow_uname = db.Column(db.String(16))
    borrow_time = db.Column(db.DateTime)
    expected_time = db.Column(db.DateTime)

class HistRecord(db.Model):
    """ 
        借用歷史紀錄
        表名: hist_record
        schema: flask_borrow_system
        欄位:
            id（pk)
            roduct_id: str
            product_name: str
            product_category: str
            in_store: boolean
            rate: float
            ave_rate: float
            note: str
            comment: str
            borrow_uid: str
            borrow_uname: str
            borrow_time: DateTime
            return_time: DateTime
            expected_time: DateTime
    """
    
    __tablename__ = 'hist_record' # 指名資料庫table名稱
    
    __table_args__ = {
        'schema': 'flask_borrow_system' # 指定資料庫schema 
    }

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.String(64), nullable=False)
    product_name = db.Column(db.String(64), nullable=False)
    product_category = db.Column(db.String(64), nullable=False)
    in_store = db.Column(db.Boolean)
    rate = db.Column(db.Float)
    ave_rate = db.Column(db.Float)
    comment = db.Column(db.String(512))
    
    borrow_uid = db.Column(db.String(16), nullable=False)
    borrow_uname = db.Column(db.String(16), nullable=False)
    borrow_time = db.Column(db.DateTime)
    return_time = db.Column(db.DateTime)
    expected_time = db.Column(db.DateTime)

class AdminList(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.String(16), nullable=False)
    uname = db.Column(db.String(16), nullable=False)

class RegistForm(FlaskForm):
    user = StringField(u"員工編號", validators=[DataRequired(message=u"請輸入正確員工編號")])
    uname = StringField(u"員工名稱", validators=[DataRequired(message=u"請輸入正確員工編號")])
    submit = SubmitField(u"Submit")

if __name__ == '__main__':
    db.drop_all() # 清除資料庫所有資料
    db.create_all() # 建立所有表

    # 寫入資料
    row_0 = ProductInfo(product_id='301010103B0042', product_category='筆記型電腦', product_name='LC170W034', in_store=True, rate=98 ,borrow_uid=None, borrow_uname=None, borrow_time=None)
    row_1 = ProductInfo(product_id='條碼值002', product_category='轉接頭', product_name='vga2hdmi_02', in_store=False, rate=4.65 ,borrow_uid='esb004', borrow_uname='wonder_woman', borrow_time='2021-1-9') 
    row_2 = ProductInfo(product_id='條碼值003', product_category='簡報筆', product_name='logi_01', in_store=True, rate=4.85 ,borrow_uid=None, borrow_uname=None, borrow_time=None)
    row_3 = ProductInfo(product_id='條碼值004', product_category='投影機', product_name='12b_01', in_store=False, rate=4.95 ,borrow_uid='esb002', borrow_uname='spyderman', borrow_time='2021-1-16')
    row_4 = ProductInfo(product_id='301010103B1909', product_category='筆記型電腦', product_name='LC170W149',  in_store=True, rate=93 ,borrow_uid=None, borrow_uname=None, borrow_time=None)
    row_5 = ProductInfo(product_id='條碼值006', product_category='投影機', product_name='12b_02', in_store=True, rate=4.65 ,borrow_uid=None, borrow_uname=None, borrow_time=None)
    row_6 = ProductInfo(product_id='條碼值007', product_category='簡報筆', product_name='logi_02', in_store=False, rate=3.65 ,borrow_uid='esb001', borrow_uname='superman', borrow_time='2021-1-6')
    row_7 = ProductInfo(product_id='301010103A5402', product_category='筆記型電腦', product_name='LC170W069',  in_store=True, rate=99 ,borrow_uid=None, borrow_uname=None, borrow_time=None)
    row_8 = ProductInfo(product_id='301010103B6679', product_category='筆記型電腦', product_name='LC170W193',  in_store=True, rate=92 ,borrow_uid=None, borrow_uname=None, borrow_time=None)
    row_9 = ProductInfo(product_id='條碼值010', product_category='轉接頭', product_name='vga2hdmi_01', in_store=True, rate=4.65 ,borrow_uid=None, borrow_uname=None, borrow_time=None)

    db.session.add_all([row_0, row_1, row_2, row_3, row_4, row_5, row_6, row_7, row_8, row_9])
    db.session.commit()
    
    # 寫入資料
    nb1 = ProductInfo(product_id="nb001", product_name="公用筆電1", product_category="公用電腦", in_store=False, rate="5", borrow_uid="21126", borrow_uname="zy", borrow_time="Jan-18-2021 23:58:22", expected_time="Jan-31-2021")
    nb2 = ProductInfo(product_id="nb002", product_name="公用筆電2", product_category="公用電腦", in_store=True)   
    nb3 = ProductInfo(product_id="nb003", product_name="公用筆電3", product_category="公用電腦", in_store=False, rate="5", borrow_uid="21153", borrow_uname="Lala Queen", borrow_time="Jan-18-2021 23:58:22", expected_time="Jan-31-2021")   

    pd1 = ProductInfo(product_id="pd001", product_name="平板電腦1", product_category="平板電腦", in_store=False, rate="5", borrow_uid="21153", borrow_uname="Lala Queen", borrow_time="Jan-25-2021 23:58:22", expected_time="Jan-27-2021")   
    pd2 = ProductInfo(product_id="pd002", product_name="平板電腦2", product_category="平板電腦", in_store=True)   
    
    p1 = ProductInfo(product_id="p001", product_name="投影筆1", product_category="投影筆", in_store=False, rate="5", borrow_uid="19692", borrow_uname="昱齊", borrow_time="Jan-22-2021 23:58:22", expected_time="Jan-31-2021 23:58:22")
    p2 = ProductInfo(product_id="p002", product_name="投影筆2", product_category="投影筆", in_store=True)
    
    m1 = ProductInfo(product_id="m001", product_name="投影機1", product_category="投影機", in_store=False, rate="5", borrow_uid="21125", borrow_uname="昱辰", borrow_time="Jan-23-2021 23:58:22", expected_time="Jan-27-2021 23:58:22")
    
    t1 = ProductInfo(product_id="t001", product_name="轉接頭1", product_category="轉接頭", in_store=True)
    t2 = ProductInfo(product_id="t002", product_name="轉接頭2", product_category="轉接頭", in_store=True)
    t3 = ProductInfo(product_id="t003", product_name="轉接頭3", product_category="轉接頭", in_store=False, rate="5", borrow_uid="16875", borrow_uname="Kevin", borrow_time="Jan-21-2021 23:58:22", expected_time="Jan-31-2021 23:58:22")
    # db.session.add(nb1) # 新增單筆
    db.session.add_all([nb1, nb2, nb3, pd1, pd2, p1, p2, m1, t1, t2, t3]) # session 紀錄多筆
    db.session.commit() # commit 至資料庫

    h1 = HistRecord(product_id="nb001", product_name="公用筆電1", product_category="公用電腦", in_store=True, rate="2", comment="有點舊...而且比較想用mac", borrow_uid="21126", borrow_uname="zy", borrow_time="Jan-11-2021 23:58:22", return_time="Jan-12-2021 23:58:22", expected_time="Jan-15-2021")
    h2 = HistRecord(product_id="nb001", product_name="公用筆電1", product_category="公用電腦", in_store=True, rate="3", comment="髒髒der~", borrow_uid="21126", borrow_uname="zy", borrow_time="Jan-16-2021 23:58:22", return_time="Jan-17-2021 23:58:22", expected_time="Jan-17-2021")
    h3 = HistRecord(product_id="nb001", product_name="公用筆電1", product_category="公用電腦", in_store=False, borrow_uid="21126", borrow_uname="zy", borrow_time="Jan-18-2021 23:58:22", expected_time="Jan-31-2021")
    h4 = HistRecord(product_id="nb002", product_name="公用筆電3", product_category="公用電腦", in_store=True, rate="5", comment="hi", borrow_uid="21126", borrow_uname="zy", borrow_time="Jan-18-2021 23:58:22", return_time="Jan-20-2021 23:58:22", expected_time="Jan-20-2021")
    h5 = HistRecord(product_id="nb002", product_name="公用筆電3", product_category="公用電腦", in_store=True, rate="5", comment="開機開得很快，而且不會當機", borrow_uid="21126", borrow_uname="zy", borrow_time="Jan-09-2021 23:58:22", return_time="Jan-10-2021 23:58:22", expected_time="Jan-11-2021")
    h6 = HistRecord(product_id="nb002", product_name="公用筆電3", product_category="公用電腦", in_store=True, rate="4", comment="還行啦～", borrow_uid="21153", borrow_uname="Lala Queen", borrow_time="Jan-12-2021 23:58:22", return_time="Jan-16-2021 23:58:22", expected_time="Jan-16-2021")
    h7 = HistRecord(product_id="nb002", product_name="公用筆電3", product_category="公用電腦", in_store=True, rate="5", comment="好用好用！！！", borrow_uid="21125", borrow_uname="昱辰", borrow_time="Jan-16-2021 23:58:22", return_time="Jan-17-2021 23:58:22", expected_time="Jan-18-2021")
    h8 = HistRecord(product_id="nb002", product_name="公用筆電3", product_category="公用電腦", in_store=False, borrow_uid="21153", borrow_uname="Lala Queen", borrow_time="Jan-18-2021 23:58:22", expected_time="Jan-31-2021")
    
    h9 = HistRecord(product_id="pd001", product_name="平板電腦1", product_category="平板電腦", in_store=True, rate="1", comment="都連不太到網路... 而且觸空不太靈敏，也沒辦法搭配apple觸空筆，該換了啦！！！", borrow_uid="21126", borrow_uname="zy", borrow_time="Jan-17-2021 23:58:22", return_time="Jan-18-2021 23:58:22", expected_time="Jan-19-2021")
    h10 = HistRecord(product_id="pd001", product_name="平板電腦1", product_category="平板電腦", in_store=True, rate="1.2", comment="總務 該換囉～～～", borrow_uid="21126", borrow_uname="zy", borrow_time="Jan-20-2021 23:58:22", return_time="Jan-25-2021 23:58:22", expected_time="Jan-25-2021")
    h11 = HistRecord(product_id="pd001", product_name="平板電腦1", product_category="平板電腦", in_store=False, comment="", borrow_uid="21153", borrow_uname="Lala Queen", borrow_time="Jan-25-2021 23:58:22", expected_time="Jan-27-2021")
    h12 = HistRecord(product_id="p001", product_name="投影筆1", product_category="投影筆", in_store=False, borrow_uid="19692", borrow_uname="昱齊", borrow_time="Jan-22-2021 23:58:22", expected_time="Jan-31-2021")
    h13 = HistRecord(product_id="m001", product_name="投影機1", product_category="投影機", in_store=False, borrow_uid="21125", borrow_uname="昱辰", borrow_time="Jan-23-2021 23:58:22", expected_time="Jan-27-2021")
    h14 = HistRecord(product_id="t003", product_name="轉接頭3", product_category="轉接頭", in_store=False, borrow_uid="16875", borrow_uname="Kevin", borrow_time="Jan-21-2021 23:58:22", expected_time="Jan-31-2021")

    db.session.add_all([h1, h2, h3, h4, h5, h6, h7, h8, h9, h10, h11, h12, h13, h14]) # 一次寫入多筆
    db.session.commit()