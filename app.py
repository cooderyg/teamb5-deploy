from flask import Flask, render_template, request, jsonify
application = app = Flask(__name__) 

from pymongo import MongoClient
client = MongoClient('mongodb+srv://sparta:test@cluster0.jy74xj7.mongodb.net/?retryWrites=true&w=majority')
db = client.dbsparta

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/members/<membername>')
def get_membername(membername):
    return render_template(f'/members/{membername}.html')

@app.route('/guestbook')
def guestbook():
    return render_template('guestbook.html')

@app.route("/members", methods=["POST"])
def member_post():
    name_receive = request.form['name_give']
    mbti_receive = request.form['mbti_give']
    advantage_receive = request.form['advantage_give']
    style_receive = request.form['style_give']
    
    doc = {
        'name' : name_receive,
        'mbti' : mbti_receive,
        'advantage' : advantage_receive,
        'style' : style_receive
    }
    db.member.insert_one(doc)
    return jsonify({'msg': '저장 완료!'})

@app.route("/guestbook", methods=["POST"])
def guestbook_post():
    name_receive = request.form['name_give']
    comment_receive = request.form['comment_give']

    doc = {
        'name' : name_receive,
        'comment' : comment_receive
    }
    db.guestbook.insert_one(doc)
    return jsonify({'msg': '저장 완료!'})

if __name__ == '__main__':
    app.run()