from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# # 設置連接DB的url
# # [sql server] :// [帳號]:[密碼]@[資料庫路徑]:[端口號]/[資料庫名稱]
# app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://yuchen:22234026@127.0.0.1:5432/flask"

# # 自動提交資料庫的改動(不建議設定)
# app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = False

# # 追蹤資料庫修改
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# # 查詢時顯示原始的SQL語句
# app.config['SQLALCHEMY_ECHO'] = True

class Config(object):
    """資料庫配置"""
    # 設置連接DB的url
    SQLALCHEMY_DATABASE_URI = "postgresql://yuchen:ilove5566@127.0.0.1:5432/flask"
    # 自動提交資料庫的改動(不建議設定)
    SQLALCHEMY_COMMIT_ON_TEARDOWN = False
    # 追蹤資料庫修改
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    # 查詢時顯示原始的SQL語句
    SQLALCHEMY_ECHO = True

# 代入Config
app.config.from_object(Config)
# 創建資料庫連線
db = SQLAlchemy(app)

# 每個class都是一張表
# 創建資料庫模型 >>> CREAT TABLE
class User(db.Model):
    """用戶表"""
    # 指定資料庫表名 tbl_users
    __tablename__ = 'tbl_users'

    # 指定資料庫schema flask_demo
    __table_args__ = {
        'schema': 'flask_demo'
    }

    # Flask SQLAlchemy 不會自動創建 primary key 需自行設置
    id = db.Column(db.Integer, primary_key=True)        # 會默認為自增主鍵
    # name, email應為唯一值, unique=True
    name = db.Column(db.String(64), unique=True)
    email = db.Column(db.String(128), unique=True)
    password = db.Column(db.String(128))
    
    # 創建外鍵 Foreign key >>> 外鍵必為另一張表的主鍵
    # 透過 db.ForeignKey 使該欄位跟 tbl_roles 的主鍵 id 產生關聯
    role_id = db.Column(db.Integer, db.ForeignKey("flask_demo.tbl_roles.id"))

class Role(db.Model):
    """用戶身分表"""
    # 指定資料庫表名 tbl_roles
    __tablename__ = 'tbl_roles'

    # 指定資料庫schema flask_demo
    __table_args__ = {
        'schema': 'flask_demo'
    }
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)

    # 將該個 class Role 與 class User 建立關聯(非直接出現在資料表的內容)
    # 透過 Role.users 呼叫 User 裡的 attributes
    # backref='role' 等於在class User 裡創建一個 attribute 'role'
    # 透過user.role 可以直接呼叫 role 裡對應 role_id 的資料
    users = db.relationship("User", backref='role')

@app.route('/')
def index():
    return "index page"

if __name__ == '__main__':
    # 清除資料庫裡所有的資料
    db.drop_all()
    # 創建所有的表(上面的所有class)
    db.create_all()

    # 創建對象
    role1 = Role(name='admin')
    # session 記錄對象任務
    db.session.add(role1)
    # 提交任務到資料庫中
    db.session.commit()

    role2 = Role(name='stuff')
    db.session.add(role2)
    db.session.commit()

    usr1 = User(name='123', email='123@esb.com.tw', password='ilove123', role_id=role1.id)
    usr2 = User(name='45', email='45@esb.com.tw', password='ilove45', role_id=role2.id)
    usr3 = User(name='67', email='67@esb.com.tw', password='ilove67', role_id=role2.id)
    usr4 = User(name='890', email='890@esb.com.tw', password='ilove890', role_id=role1.id)

    # add_all([list]) 一次保存多筆數據
    db.session.add_all([usr1, usr2, usr3, usr4])
    db.session.commit()