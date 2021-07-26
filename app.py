# import sys
# sys.path.insert(0,'./light_config')
# import light_mongo_auth
import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

from pymongo import MongoClient

# client = MongoClient('mongodb://test:test@localhost', 27017)
client = MongoClient('localhost', 27017)
db = client.dbhomework

## HTML 화면 보여주기
@app.route('/')
def index():
    name = "what the"
    return render_template('index.html',
                           name = "what the"
                           )

## HTML 화면 보여주기
@app.route('/jobs')
def jobs():
    return render_template('jobs.html')


## 채용공고 스크래핑 API 
@app.route('/jobs_get', methods=['GET'])
def jobs_get():
    url_rec = "https://www.saramin.co.kr/zf_user/search?searchType=search&loc_cd=101010%2C101120%2C101130%2C101140%2C101150%2C101160%2C101180%2C101230%2C101240&cat_key=120311&company_cd=0%2C1%2C2%2C3%2C4%2C5%2C6%2C7%2C9%2C10&keydownAccess=&searchword=%ED%8C%A8%ED%82%A4%EC%A7%80+%EB%94%94%EC%9E%90%EC%9D%B4%EB%84%88+%EA%B2%BD%EB%A0%A5&panel_type=&search_optional_item=y&search_done=y&panel_count=y"
    # print(url_rec, comment_rec)
    # #recruit_info_list > div.content > div:nth-child(1)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get(url_rec, headers=headers)
    soup = BeautifulSoup(data.text, 'html.parser')
    items = soup.select('#recruit_info_list > div.content > div')
    job_list = []
    for item in items:
        company = item.select_one('div.area_corp > strong > a')['title']
        company_url = item.select_one('div.area_corp > strong > a')['href']
        title = item.select_one('div.area_job > h2 > a')['title']
        title_url = item.select_one('div.area_job > h2 > a')['href']
        region = item.select_one('div.area_job > div.job_condition > span:nth-child(1) > a:nth-child(2)').text
        newornot = item.select_one('div.area_job > div.job_condition > span:nth-child(2)').text

        job_list.append({
            "company": company,
            "company_url": "https://www.saramin.co.kr"+company_url,
            "title": title,
            "title_url": "https://www.saramin.co.kr"+title_url,
            "region": region,
            "newornot": newornot
        })
    return jsonify({'job_list': job_list})

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