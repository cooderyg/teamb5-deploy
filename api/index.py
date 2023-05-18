from flask import Flask, render_template, request, jsonify, redirect, url_for
application = app = Flask(__name__) 

from bson.json_util import dumps
from bson.objectid import ObjectId

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

#member EDIT 페이지 랜더링
@app.route('/members/edit/<memberid>')
def member_render(memberid):
    return render_template('/members/edit.html', memberid=memberid)

#guestbook EDIT 페이지 랜더링
@app.route('/guestbooks/<membername>/edit/<guestbookid>')
def guestbook_render(guestbookid, membername):
    return render_template('/guestbooks/edit.html', membername=membername, guestbookid=guestbookid)

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
    all_members = list(db.member.find({}))
    return dumps({'result': all_members})

#메인페이지 하단 멤버카드 DELETE
@app.route("/members/<memberid>", methods=["DELETE"])
def members_delete(memberid):
    db.member.delete_one({'_id':ObjectId(memberid)})
    return jsonify({'msg': '삭제완료'})

#메인EDIT페이지 GET
@app.route("/member/<memberid>", methods=["GET"])
def member_get(memberid):
    member = db.member.find_one({'_id':ObjectId(memberid)},{'_id':False})
    return jsonify({'result': member})

#메인EDIT페이지 PUT
@app.route("/member/<memberid>", methods=["PUT"])
def member_put(memberid):
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
    db.member.update_one({'_id':ObjectId(memberid)}, {"$set": doc})
    return jsonify({'msg': "수정이완료되었습니다"})

#서브페이지 상단 프로필 GET
@app.route("/profile/<membername>", methods=["GET"])
def profile_get(membername):
    profile = db.member.find_one({"member":membername},{'_id':False})
    return jsonify({'result': profile})

#서브페이지 하단 방명록 GET
@app.route("/guestbooks/<membername>", methods=["GET"])
def guestbooks_get(membername):
    all_guestbooks = list(db.guestbook.find({"member":membername}))
    return dumps({'result': all_guestbooks})

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

#서브페이지 방명록 DELETE
@app.route("/guestbooks/<guestbookid>", methods=["DELETE"])
def guestbooks_delete(guestbookid):
    db.guestbook.delete_one({'_id':ObjectId(guestbookid)})
    return jsonify({'msg': '삭제완료'})

#서브EDIT페이지 GET
@app.route("/guestbook/<guestbookid>", methods=["GET"])
def guestbook_get(guestbookid):
    gusetbook = db.guestbook.find_one({'_id':ObjectId(guestbookid)},{'_id':False})
    return jsonify({'result': gusetbook})

#서브EDIT페이지 PUT
@app.route("/guestbook/<guestbookid>", methods=["PUT"])
def guestbook_put(guestbookid):
    name_receive = request.form['name_give']
    comment_receive = request.form['comment_give']
    doc = {
        'name' : name_receive,
        'comment' : comment_receive,
    }
    db.guestbook.update_one({'_id':ObjectId(guestbookid)}, {"$set": doc})
    return jsonify({'msg': "수정이완료되었습니다"})


if __name__ == '__main__':
    app.run()