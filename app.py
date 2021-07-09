from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

from pymongo import MongoClient

client = MongoClient('mongodb://test:test@localhost', 27017)
# client = MongoClient('localhost', 27017)
db = client.dbhomework

## HTML 화면 보여주기
@app.route('/')
def homework():
    return render_template('index.html')


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