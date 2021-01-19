from flask import Flask, render_template, url_for, request, redirect, session
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo
from flask_sqlalchemy import SQLAlchemy
from db_table import Item # 匯入某個 class (某個資料表)

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
        'user': 'postgres',
        'password': '2618',
        'db': 'test',
        'host': '127.0.0.1',  
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


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('pf_index.html')

@app.route('/search', methods=['GET','POST'])
def search():
    # 要從 form 表單拿到資料，進行資料庫查詢操作。
    name = request.form.get('name')  #需要查詢的內容, 傳回來的東西為 .html 中 id=name 那個輸入框之值 
    if name is None:
        name = " "
    #查詢跟 type_name 有關的資料，返回結果為列表
    quotes = Item.query.filter(Item.type_name.like("%"+name+"%") if name is not None else "").all()
    # quotes = Item.query.filter_by(type_name=type_name).all()
    return render_template('prac_search.html', quotes=quotes) # 將查詢結果返回到前端

@app.route('/borrow')
def borrow():
    return '借用頁面'

@app.route('/sendback')
def sendback():
    return '歸還頁面'

if __name__ == "__main__":
    app.run(debug=True)