import pymongo
from pymongo import MongoClient

client = ""
db = ""


def mongo_connect():
	global db, client
	client = MongoClient("mongodb://127.0.0.1:27117,127.0.0.1:27118/")
	db = client.progetto


def insert_one(table, data):
	return db[table].insert_one(data)


def insert_many(table, data):
	return db[table].insert_many(data)


def find_one(table, data):
	return db[table].find_one(data)


def aggregate(table, aggregation_steps):
	return list(db[table].aggregate(aggregation_steps))


def mongo_disconnect():
	client.close()

