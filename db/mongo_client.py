from pymongo import MongoClient

client = MongoClient()
db = client.python


def c(collection_name):
    return MongoCollection(db[collection_name])


class MongoCollection:
    def __init__(self, collection):
        self.collection = collection

    def insert_one(self, document):
        return self.collection.insert_one(document)

    def find_all(self):
        cursor = self.collection.find()
        ads = list()
        for x in cursor:
            ads.append(x)
        return ads

    def update(self, item):
        return self.collection.save(item)
