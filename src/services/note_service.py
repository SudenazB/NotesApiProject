from config import ConfigMongo
from pymongo import MongoClient
from bson.objectid import ObjectId

client = MongoClient(ConfigMongo.ConfigMongo.MONGO_URI)
db = client[ConfigMongo.ConfigMongo.MONGO_DBNAME]

class noteProcess:
    @staticmethod
    def addNote(note):
        print(note)
        db.notes.insert_one({
            'not': note["data"],

        })
        return "not kayıt edildi"

    @staticmethod
    def getNote():
        notss = []
        for nots in db.notes.find({}, {'_id': 0}):
            notss.append({
                'note': nots.get('not')
            })
        return notss

    @staticmethod
    def deleteNote(note_id):
        try:
            result = db.notes.delete_one({"_id": ObjectId(note_id)})
            if result.deleted_count == 1:
                return "Note successfully deleted"
            else:
                return "Note not found"
        except Exception as e:
            return str(e)

    @staticmethod
    def update_note(id, data):
        result = db.notes.update_one(
            {"_id": ObjectId(id)},
            {"$set":  data}
        )
        return "Note successfully update"

