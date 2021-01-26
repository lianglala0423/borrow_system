#!/usr/bin/python
# -*- coding: utf-8 -*-

import pandas as pd
from statistics import mean
from datetime import datetime, timedelta
from flask import Flask, render_template, url_for, request, redirect, session
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_, func
from db_final import ProductInfo, HistRecord # 匯入某個 class (某個資料表)
from jinja2 import Markup

from pyecharts.charts import Bar, Liquid
from pyecharts import options

app = Flask(__name__)
# 必須自己設置一個安全碼
app.config['SECRET_KEY'] = 'development'
category = ['公用電腦', '投影筆', '投影機', '轉接頭', '平板電腦']

hist = []

# 定義表單的模型類別
class Config(object):
    """
    把要配置的參數都包在這個類別
    """
    # sqlalchemy 的配置參數: 要連去哪個資料庫
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://DB_USER:PASSWORD@HOST/DATABASE'
    POSTGRES = {
        'user': 'postgres',
        'password': 'postgres',
        'db': 'postgres',
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

def get_top_rate():

    delta = timedelta(days=28)
    end_date = datetime.now()
    start_date = end_date - delta

    leaderboard = db.session.query(
        HistRecord.product_name, 
        HistRecord.rate, #func.avg(HistRecord.rate).label('avg_rate')
        HistRecord.comment
    ).filter(
        HistRecord.borrow_time > start_date,
        HistRecord.borrow_time <= end_date,
        HistRecord.in_store == 't'
    ).order_by(
        HistRecord.rate.desc()
    ).all()

    top_rate = {}
    for data in leaderboard:

        if data[0] in top_rate:
            if data[1]:
                top_rate[data[0]]['rate'].append(data[1]) 
            if data[2]:
                top_rate[data[0]]['comment'].append(data[2])
        else:
            top_rate[data[0]] = {'rate': [data[1]], 'comment': [data[2]]}

    for i in top_rate.keys():
        top_rate[i]['rate'] = round(mean(top_rate[i]['rate']), 1)

    return top_rate

def get_borrow_record():

    data = db.session.query(
        ProductInfo.borrow_uname, ProductInfo.product_name, ProductInfo.expected_time
    ).filter(
        ProductInfo.in_store == 'f'
    ).order_by(
        ProductInfo.expected_time
    ).all()

    print(data)
    return data

def get_month():

    date_today = datetime.now()

    # get 4 week date
    weeklist = get_week_date(date_today, 4)
    datalist = []
    
    for week in weeklist:
        start_date = week.split('-')[0]
        end_date = week.split('-')[-1]

        data = db.session.query(
            HistRecord.product_category, func.count(HistRecord.product_category)
        ).filter(
            HistRecord.borrow_time > start_date,
            HistRecord.borrow_time <= end_date
        ).group_by(
            HistRecord.product_category
        ).all()
        datalist.append(data)

    weeklist.reverse()
    datalist.reverse()

    return weeklist, datalist

def get_in_use_rate():
    global category

    # query 產品借用紀錄
    in_use_rate = {}
    total_items = db.session.query(
        ProductInfo.product_category, ProductInfo.in_store, func.count(ProductInfo.product_category)
    ).group_by(
        ProductInfo.product_category,
        ProductInfo.in_store
    ).all()

    for i in range(len(category)):
        # 統計產品借出數量, 總數
        item_count = 0
        in_use_count = 0
        temp = [item for item in total_items if item[0] == category[i]]
        for item in temp:
            item_count = item_count + int(item[2])
        for item in temp:
            if item[1] == False:
                in_use_count = in_use_count + int(item[2])
        
        # 計算產品類別借用率
        rate = 0 if in_use_count == 0 else (in_use_count/item_count)
        in_use_rate[category[i]] = round(rate, 2)

    return in_use_rate

def get_goods_stacked_bar():
    date_xaxis, query_data = get_month()
    print(query_data)
    product_category = ["公用電腦", "平板電腦", "投影筆", "投影機", "轉接頭"]

    # initial history data
    hist = {k:[] for k in product_category}

    for week_idx, week_data in enumerate(query_data):
        # init
        for v in hist.values():
            v.append(0)

        # update     
        for product_info in week_data:
            product_name = product_info[0]
            count = product_info[1]

            hist[product_name][week_idx] = count

    # create graph
    c = Bar()
    c.set_global_opts(xaxis_opts=options.AxisOpts(axislabel_opts=options.LabelOpts(interval=0)))    
    c.add_xaxis(date_xaxis)
    for idx, (prod_name, prod_data) in enumerate(hist.items()):
        c.add_yaxis(prod_name, prod_data, stack="stack"+str(idx))

    return c

def get_week_date(datelast, weeks):
    '''
        Args:
            datelast: 從這天往前推
            weeks: 往前推幾週

        return:
            weeklist
                example:
                ['2021/01/17-2021/01/24', '2021/01/09-2021/01/16', '2021/01/01-2021/01/08', '2020/12/24-2020/12/31']
    '''

    weeklist = []
    delta = timedelta(days=7)

    for i in range(weeks):
        items = (datelast - delta).strftime("%Y/%m/%d") + '-' + datelast.strftime("%Y/%m/%d")
        weeklist.append(items)
        datelast = datelast - delta - timedelta(days=1)

    return weeklist


def whale_shape_liquid(cate, rate):
    shape = ("path://M367.855,428.202c-3.674-1.385-7.452-1.966-11.146-1"
            ".794c0.659-2.922,0.844-5.85,0.58-8.719 c-0.937-10.407-7."
            "663-19.864-18.063-23.834c-10.697-4.043-22.298-1.168-29.9"
            "02,6.403c3.015,0.026,6.074,0.594,9.035,1.728 c13.626,5."
            "151,20.465,20.379,15.32,34.004c-1.905,5.02-5.177,9.115-9"
            ".22,12.05c-6.951,4.992-16.19,6.536-24.777,3.271 c-13.625"
            "-5.137-20.471-20.371-15.32-34.004c0.673-1.768,1.523-3.423"
            ",2.526-4.992h-0.014c0,0,0,0,0,0.014 c4.386-6.853,8.145-14"
            ".279,11.146-22.187c23.294-61.505-7.689-130.278-69.215-153"
            ".579c-61.532-23.293-130.279,7.69-153.579,69.202 c-6.371,"
            "16.785-8.679,34.097-7.426,50.901c0.026,0.554,0.079,1.121,"
            "0.132,1.688c4.973,57.107,41.767,109.148,98.945,130.793 c58."
            "162,22.008,121.303,6.529,162.839-34.465c7.103-6.893,17.826"
            "-9.444,27.679-5.719c11.858,4.491,18.565,16.6,16.719,28.643 "
            "c4.438-3.126,8.033-7.564,10.117-13.045C389.751,449.992,"
            "382.411,433.709,367.855,428.202z")

    liquid = Liquid()
    # liquid.width = '630px'
    # liquid.height = '350px'
    liquid.add("Liquid", [rate], shape=shape, is_outline_show=False).set_global_opts(title_opts=options.TitleOpts(title=cate, pos_left="center"))
    # liquid.add("Liquid", [rate], shape=shape, is_outline_show=False)
    return liquid

def get_graph_prod_in_store():
    global category
    data = get_in_use_rate()
    in_stotr_graph_list = []
    for cate in category:
        rate = data[cate]
        jinja_graph = Markup(whale_shape_liquid(cate, rate).render_embed())
        in_stotr_graph_list.append(jinja_graph)
    return in_stotr_graph_list

@app.route('/', methods=['GET', 'POST'])
@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    global category
    in_store_graph_list = get_graph_prod_in_store()
    goods_stacked_bar = get_goods_stacked_bar()
    borrow_record = get_borrow_record()
    top_rate = get_top_rate()
    return render_template('dashboard.html',
        in_store_graph_list=in_store_graph_list,
        goods_stacked_bar=Markup(goods_stacked_bar.render_embed()),
        borrow_record=borrow_record,
        top_rate=top_rate)

@app.route('/history', methods=['GET', 'POST'])
def history():
    global hist
    # name = 要去接 session 帶入的員編
    # quotes = ProductInfo.query.filter_by(borrow_uid=name).all()
    # quotes = []
    # return render_template('return.html', quotes=quotes)

    if request.method == 'POST':
        start_date = datetime.strptime(request.values.get('start_date'), '%Y-%m-%d')
        end_date = datetime.strptime(request.values.get('end_date'), '%Y-%m-%d')
        product_name = request.values.get('product_name')

        if start_date > end_date:
            warning = '*結束時間不得大於起始時間'
            return render_template("history.html", warning=warning)
        else:
            print(hist)
            hist = db.session.query(HistRecord).order_by(HistRecord.borrow_time).filter(
                or_(HistRecord.borrow_time > start_date,
                    HistRecord.product_name == product_name)
            ).filter(HistRecord.borrow_time <= end_date
            ).all()
            print(hist)
            return render_template('history.html', hist=hist, start_date=start_date, end_date=end_date, product_name=product_name)

    date_today = datetime.now()
    date_today = date_today.strftime("%Y-%m-%d")
    return render_template('history.html', end_date=date_today)

@app.route('/download_csv', methods=['GET', 'POST'])
def download_csv():
    global hist

    rows = []
    used_columns = ["borrow_time", "product_name", "borrow_uname", "note"]
    for u in hist:
        _dict = u.__dict__
        row = [_dict[col] for col in used_columns]
        rows.append(row)
    df = pd.DataFrame(rows, columns=used_columns)
    df.to_csv("~/Downloads/history.csv", index=False)
    notice = '下載成功'
    return render_template('history.html', hist=hist, notice=notice)

if __name__ == "__main__":
    app.run(debug=True)