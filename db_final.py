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
            status: boolean
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
    status = db.Column(db.Boolean)
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
            status: boolean
            rate: float
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
    status = db.Column(db.Boolean)
    rate = db.Column(db.Float)
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

# if __name__ == '__main__':
#     db.drop_all() # 清除資料庫所有資料
#     db.create_all() # 建立所有表

    # # 寫入資料
    # role1 = Role(name="admin")
    # db.session.add(role1) # session 紀錄
    # db.session.commit() # commit 至資料庫

    # role2 = Role(name="stuff")
    # db.session.add(role2)
    # db.session.commit()

    # user1 = User(name="yu", email="yu@gmail.com", password="123", role_id=role1.id)
    # user2 = User(name="li", email="li@gmail.com", password="abc", role_id=role2.id)
    # user3 = User(name="chen", email="chen@gmail.com", password="321", role_id=role2.id)
    # user4 = User(name="liang", email="liang@gmail.com", password="cba", role_id=role1.id)

    # db.session.add_all([user1, user2, user3, user4]) # 一次寫入多筆
    # db.session.commit()