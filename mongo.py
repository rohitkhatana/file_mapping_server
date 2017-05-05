from pymongo import MongoClient


def client(user_name, password, db_name, host="planmycash.in"):
    if user_name:
        return MongoClient("mongodb://{}:{}@{}:27017/{}".format(user_name, password, host, db_name))
    return MongoClient("mongodb://{}:27017/{}".format(host, db_name))
