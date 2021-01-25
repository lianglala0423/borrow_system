#!/usr/bin/python
# -*- coding: utf-8 -*-

# db_demo.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

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
        'port': '5432'}

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
    """
    __tablename__ = 'product_info' # 指名資料庫table名稱
    
    # __table_args__ = {
    #     'schema': 'flask_borrow_system' # 指定資料庫schema 
    # }

    product_id = db.Column(db.String(64), primary_key=True)
    product_name = db.Column(db.String(64), nullable=False)
    product_category = db.Column(db.String(64), nullable=False)
    in_store = db.Column(db.Boolean)
    rate = db.Column(db.Float)
    
    borrow_uid = db.Column(db.String(16))
    borrow_uname = db.Column(db.String(16))
    borrow_time = db.Column(db.DateTime)

    # role_id = db.Column(db.Integer, db.ForeignKey("tbl_roles.id")) # 建立兩張表的關聯
    
    # def __repr__(self):
    #     """定義之後 可以讓查詢結果顯示的更直觀"""
    #     return "User object: name=%s" % self.name

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
            borrow_uid: str
            borrow_uname: str
            borrow_time: DateTime
            return_time: DateTime
            expected_time: DateTime
    """
    
    __tablename__ = 'hist_record' # 指名資料庫table名稱
    
    # __table_args__ = {
    #     'schema': 'flask_borrow_system' # 指定資料庫schema 
    # }

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.String(64), nullable=False)
    product_name = db.Column(db.String(64), nullable=False)
    product_category = db.Column(db.String(64), nullable=False)
    in_store = db.Column(db.Boolean)
    rate = db.Column(db.Float)
    ave_rate = db.Column(db.Float)
    note = db.Column(db.String(256))
    
    borrow_uid = db.Column(db.String(16), nullable=False)
    borrow_uname = db.Column(db.String(16), nullable=False)
    borrow_time = db.Column(db.DateTime)
    return_time = db.Column(db.DateTime)
    expected_time = db.Column(db.DateTime)
    
    # users = db.relationship("User", backref="role")
    
    # def __repr__(self):
    #     """定義之後 可以讓查詢結果顯示的更直觀"""
    #     return "Role object: name=%s" % self.name

if __name__ == '__main__':
    db.drop_all() # 清除資料庫所有資料
    db.create_all() # 建立所有表

    # 寫入資料
    # row_0 = ProductInfo(product_id='條碼值001', product_category='筆記型電腦', product_name='LC170W001', in_store=False, rate=4.65 ,borrow_uid='esb001', borrow_uname='superman', borrow_time='2021-1-6')
    # row_1 = ProductInfo(product_id='條碼值002', product_category='轉接頭', product_name='vga2hdmi_02', in_store=False, rate=4.65 ,borrow_uid='esb004', borrow_uname='wonder_woman', borrow_time='2021-1-9') 
    # row_2 = ProductInfo(product_id='條碼值003', product_category='簡報筆', product_name='logi_01', in_store=True, rate=4.85 ,borrow_uid=None, borrow_uname=None, borrow_time=None)
    # row_3 = ProductInfo(product_id='條碼值004', product_category='投影機', product_name='12b_01', in_store=False, rate=4.95 ,borrow_uid='esb002', borrow_uname='spyderman', borrow_time='2021-1-16')
    # row_4 = ProductInfo(product_id='條碼值005', product_category='筆記型電腦', product_name='LC170W002', in_store=False, rate=4.65 ,borrow_uid='esb003', borrow_uname='batman', borrow_time='2021-1-10')
    # row_5 = ProductInfo(product_id='條碼值006', product_category='投影機', product_name='12b_02', in_store=True, rate=4.65 ,borrow_uid=None, borrow_uname=None, borrow_time=None)
    # row_6 = ProductInfo(product_id='條碼值007', product_category='簡報筆', product_name='logi_02', in_store=False, rate=3.65 ,borrow_uid='esb001', borrow_uname='superman', borrow_time='2021-1-6')
    # row_7 = ProductInfo(product_id='條碼值008', product_category='筆記型電腦', product_name='LC170W003', in_store=False, rate=4.85 ,borrow_uid='esb004', borrow_uname='wonder_woman', borrow_time='2021-1-9')
    # row_8 = ProductInfo(product_id='條碼值009', product_category='筆記型電腦', product_name='LC170W004', in_store=False, rate=3.65 ,borrow_uid='esb005', borrow_uname='ironman', borrow_time='2021-1-11')
    # row_9 = ProductInfo(product_id='條碼值010', product_category='轉接頭', product_name='vga2hdmi_01', in_store=True, rate=4.65 ,borrow_uid=None, borrow_uname=None, borrow_time=None)
    row_0 = ProductInfo(product_id='條碼值001', product_category='筆記型電腦', product_name='LC170W001', in_store=True, rate=None ,borrow_uid=None, borrow_uname=None, borrow_time=None)
    row_1 = ProductInfo(product_id='條碼值002', product_category='轉接頭', product_name='vga2hdmi_02', in_store=True, rate=None ,borrow_uid=None, borrow_uname=None, borrow_time=None) 
    row_2 = ProductInfo(product_id='條碼值003', product_category='簡報筆', product_name='logi_01', in_store=True, rate=None ,borrow_uid=None, borrow_uname=None, borrow_time=None)
    row_3 = ProductInfo(product_id='條碼值004', product_category='投影機', product_name='12b_01', in_store=True, rate=None ,borrow_uid=None, borrow_uname=None, borrow_time=None)
    row_4 = ProductInfo(product_id='條碼值005', product_category='筆記型電腦', product_name='LC170W002', in_store=True, rate=None ,borrow_uid=None, borrow_uname=None, borrow_time=None)
    row_5 = ProductInfo(product_id='條碼值006', product_category='投影機', product_name='12b_02', in_store=True, rate=None ,borrow_uid=None, borrow_uname=None, borrow_time=None)
    row_6 = ProductInfo(product_id='條碼值007', product_category='簡報筆', product_name='logi_02', in_store=True, rate=None ,borrow_uid=None, borrow_uname=None, borrow_time=None)
    row_7 = ProductInfo(product_id='條碼值008', product_category='筆記型電腦', product_name='LC170W003', in_store=True, rate=None ,borrow_uid=None, borrow_uname=None, borrow_time=None)
    row_8 = ProductInfo(product_id='條碼值009', product_category='筆記型電腦', product_name='LC170W004', in_store=True, rate=None ,borrow_uid=None, borrow_uname=None, borrow_time=None)
    row_9 = ProductInfo(product_id='條碼值010', product_category='轉接頭', product_name='vga2hdmi_01', in_store=True, rate=None ,borrow_uid=None, borrow_uname=None, borrow_time=None)

    # all_list = []
    # for i in range(10):
    #     all_list.append(globals()['row_' + str(i)])
    
    # print('all_list:' , all_list)
    # db.session.add_all(all_list)

    db.session.add_all([row_0, row_1, row_2, row_3, row_4, row_5, row_6, row_7, row_8, row_9]) # 一次寫入多筆
    db.session.commit()