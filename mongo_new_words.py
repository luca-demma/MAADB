import mongo_functions
import helpers
import constants

mongo_functions.mongo_connect()

for sentiment in constants.TWITTER_SENTIMENTS:

	print("FINDING NEW WORS: " + sentiment)

	mongo_functions.drop_collection('tmp_lex')
	mongo_functions.drop_collection('tmp_tweet')

	mongo_functions.aggregate('lex_resources_words', [
		{"$match": {"sentiment": sentiment}},
		{"$group": {"_id": "$word"}},
		{"$project": {"_id": 0, "word": "$_id"}},
		{"$out": "tmp_lex"}
	])

	mongo_functions.aggregate('tweet', [
		{"$match": {"sentiment": sentiment}},
		{"$project": {"keys": {"$objectToArray": "$word_count"}}},
		{"$unwind": "$keys"},
		{"$group": {"_id": "$keys.k", "count": {"$sum": "$keys.v"}}},
		{"$project": {"_id": 0, "word": "$_id", "count": "$count"}},
		{"$out": "tmp_tweet"}
	])

	res = mongo_functions.aggregate('tmp_tweet', [
		{"$lookup": {"from": "tmp_lex", "localField": "word", "foreignField": "word", "as": "matched_docs"}},
		{"$match": {"matched_docs": {"$size": 0}}},
		{"$project": {"_id": 0, "word": 1, "count": 1}},
		{"$sort": {"count": -1}},
		{"$project": {"word": "$word", "count": "$count", "sentiment": sentiment}},
		{"$merge": {"into": "new_lex_resource"}}
	])



	mongo_functions.drop_collection('tmp_lex')
	mongo_functions.drop_collection('tmp_tweet')


mongo_functions.mongo_disconnect()
