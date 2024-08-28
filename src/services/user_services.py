import jwt
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash
from bson.objectid import ObjectId
from config import ConfigMongo
from flask import Flask, jsonify
from bson import ObjectId

from src.utils.jwt_process import token_required

app = Flask(__name__)
app.config['SECRET_KEY'] = 'jwtsecretkey'

client = MongoClient(ConfigMongo.ConfigMongo.MONGO_URI)
db = client[ConfigMongo.ConfigMongo.MONGO_DBNAME]


class userProcess:
    @staticmethod
    def create_user(datas):
        data = datas.get('data', {})

        required_fields = ["Name", "Surname", "Password", "e-mail", "Phone", "Job"]

        missing_fields = []
        for field in required_fields:
            if not data.get(field):
                missing_fields.append(field)

        count = len(list(db.user.find({"users.e-mail": data["e-mail"]})))

        token = jwt.encode({
            'user': data["Name"],
            'surname': data["Surname"],
            'e_mail': data["e-mail"],

        }, app.config['SECRET_KEY'], algorithm='HS256')

        token = {"token": token}

        if missing_fields:
            return "Lütfen gerekli alanları doldurun: "
        elif count != 0:
            return "kullanıcı zaten var"
        else:

            res = db.user.insert_one({
                'users': data,

            })
            result = ["işlem başarılı", token]
            return jsonify(result)

    @staticmethod
    def login(data):
        mail = data["mail"]
        password = data["password"]

        user_detail = list(db.user.find({"users.e-mail": mail}))

        if user_detail:
            if password == user_detail[0]['users']['Password']:
                return "Giriş Yapıldı."
            else:
                return "Password yanlış."
        else:
            return "kullanıcı adı ya da password hatalı"
            print("kullanıcı adı ya da password hatalı")

        return jsonify(user_detail[0]["users"])

    @staticmethod
    def delete_email(data):
        mail = data.get("e-mail")

        if not mail:
            return "Mail bilgisi gereklidir."

        result = db.user.delete_many({"users.e-mail": mail})

        if result.deleted_count > 0:
            return "Kullanıcı silindi."
        else:
            return "Kullanıcı bulunamadı."

    @staticmethod
    def update_user(data):
        user_id = ObjectId(data["_id"])
        result = db.collection.update_one(
            {"_id": user_id},
            {"$set": data}
        )
        return result





"""
login kısmında 
1- token i decode et 
2- decode sonucu username ve pass hash'ini db üzerinden kontrol et ve eşleşen data varsa kullanıcıyı sisteme al
 eğer yoksa kullanıcı adı yada şifre yanlış resultu dön varsa da giriş başarılı dön
"""
