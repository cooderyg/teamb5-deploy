from flask import Flask, render_template, request, jsonify
application = app = Flask(__name__) 

from pymongo import MongoClient
client = MongoClient('mongodb+srv://sparta:test@cluster0.jy74xj7.mongodb.net/?retryWrites=true&w=majority')
db = client.dbsparta

#메인페이지 렌더링
@app.route('/')
def home():
    return render_template('index.html')

#서브페이지 렌더링
@app.route('/members/<membername>')
def get_membername(membername):
    return render_template(f'/members/{membername}.html')

#메인페이지 팀원 POST
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

#메인페이지 하단 멤버카드 GET
@app.route("/members", methods=["GET"])
def members_get():
    all_members = list(db.member.find({}, {'_id':False}))
    return jsonify({'result': all_members})

#메인페이지 하단 멤버카드 DELETE
@app.route("/members/<membername>", methods=["DELETE"])
def members_delete(membername):
    db.member.delete_one({'name':membername})
    return jsonify({'msg': '삭제완료'})

#서브페이지 상단 프로필 GET
@app.route("/profile/<membername>", methods=["GET"])
def profile_get(membername):
    profile = db.member.find_one({"member":membername},{'_id':False})
    return jsonify({'result': profile})

#서브페이지 하단 방명록 GET
@app.route("/guestbooks/<membername>", methods=["GET"])
def guestbooks_get(membername):
    all_guestbooks = list(db.guestbook.find({"member":membername},{'_id':False}))
    return jsonify({'result': all_guestbooks})

#서브페이지 방명록 POST
@app.route("/guestbooks", methods=["POST"])
def guestbook_post():
    name_receive = request.form['name_give']
    comment_receive = request.form['comment_give']
    member_receive = request.form['member_give']

    doc = {
        'name' : name_receive,
        'comment' : comment_receive,
        'member' : member_receive
    }
    db.guestbook.insert_one(doc)
    return jsonify({'msg': '저장 완료!'})

if __name__ == '__main__':
    app.run()