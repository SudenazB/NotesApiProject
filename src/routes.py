from flask import Blueprint, request, jsonify

from src.services.note_service import noteProcess
from src.services.user_services import userProcess

routes = Blueprint('routes', __name__)


@routes.route('/addnote', methods=["POST"])
def save():
    note = request.json
    res = noteProcess.addNote(note=note)
    return res


@routes.route('/getnote', methods=["GET"])
def getNote():
    res = noteProcess.getNote()
    print(res)
    return res


@routes.route("/delete/<string:id>", methods=["DELETE"])
def deleteNote(id):
    res = noteProcess.deleteNote(note_id=id)
    return res


# @routes.route("/delete", methods=["DELETE"])
# def deleteNote():
#     id = request.args.get("id")
#     res = noteProcess.deleteNote(note_id=id)
#     return res

@routes.route("/update/<string:id>", methods=["PUT"])
def update_note(id):
    data = request.json
    print(id, data, data["not"])
    res = noteProcess.update_note(id=id, data=data)
    return res


@routes.route("/create_user", methods=["POST"])
def create_user():
    data = request.json
    print(data)
    res = userProcess.create_user(datas=data)
    return res



@routes.route("/login", methods=["POST"])
def login():
    data = request.json
    res = userProcess.login(data=data)
    return res

@routes.route("/delete_user", methods=["DELETE"])
def delete_email():
    data = request.get_json().get('data', {})
    res = userProcess.delete_email(data)
    return res

@routes.route("/update_user", methods=["PUT"])
def update_user():
    data = request.json
    res = userProcess.update_user(data=data)
    return jsonify({"message": "User updated successfully"})

















