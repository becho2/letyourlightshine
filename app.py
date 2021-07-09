# import sys
# sys.path.insert(0,'./light_config')
# import light_mongo_auth
import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

from pymongo import MongoClient

client = MongoClient('mongodb://test:test@localhost', 27017)
# client = MongoClient('localhost', 27017)
db = client.dbhomework

## HTML 화면 보여주기
@app.route('/')
def index():
    return render_template('index.html')

## HTML 화면 보여주기
@app.route('/jobs')
def jobs():
    return render_template('jobs.html')


## 채용공고 스크래핑 API 
@app.route('/jobs_get', methods=['GET'])
def write_review():
    url_rec = https://www.saramin.co.kr/zf_user/search?cat_key=120311&company_cd=0%2C1%2C2%2C3%2C4%2C5%2C6%2C7%2C9%2C10&loc_cd=101240%2C101180%2C101150%2C101230%2C101130%2C101140%2C101010%2C101120%2C101160&panel_type=&search_optional_item=y&search_done=y&panel_count=y
    # print(url_rec, comment_rec)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get(url_rec, headers=headers)
    soup = BeautifulSoup(data.text, 'html.parser')
    return jsonify({'msg': '등록 완료!', 'response':soup})

    title = soup.select_one('meta[property="og:title"]')['content']
    image_url = soup.select_one('meta[property="og:image"]')['content']
    synopsis = soup.select_one('meta[property="og:description"]')['content']
    # print(title, image_url, synopsis)
    doc = {
        "url": url_rec,
        "comment": comment_rec,
        "title": title,
        "imageUrl": image_url,
        "synopsis": synopsis
    }
    res = db.alonememo.insert_one(doc)
    print(res)
    return jsonify({'msg': '등록 완료!'})

# 주문하기(POST) API
@app.route('/order', methods=['POST'])
def save_order():
    name_rec = request.form['name']
    cnt_rec = request.form['cnt']
    addr_rec = request.form['addr']
    code_rec = request.form['code']
    phone_rec = request.form['phone']
    doc = {
        "name": name_rec,
        "cnt": cnt_rec,
        "addr": addr_rec,
        "code": code_rec,
        "phone": phone_rec
    }
    db.orders.insert_one(doc)
    return jsonify({'msg': '진짜 사시려구요? 정보 등록됐습니다!'})


# 주문 목록보기(Read) API
@app.route('/order', methods=['GET'])
def view_orders():
    orders = list(db.orders.find({},{'_id':False}))
    return jsonify({'msg': '성공', 'orders': orders})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)