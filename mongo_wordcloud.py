import mongo_functions
import constants
import helpers
import time

mongo_functions.mongo_connect()

time_start = time.time()

# Wordcount WORDS
for sentiment in constants.TWITTER_SENTIMENTS:
	print("GENERATING WORDS %s WORDCLOUD" % sentiment)

	words_count_sum = mongo_functions.aggregate('tweet', [
		{'$match': {'sentiment': sentiment}}, {'$project': {'word_count': 1}},
		{'$project': {'words': {'$objectToArray': '$word_count'}}}, {'$unwind': '$words'},
		{'$project': {'word': '$words.k', 'count': '$words.v'}},
		{'$group': {'_id': '$word', 'count': {'$sum': '$count'}}}
	])

	# converting results to dict
	w_count = {}
	for w in words_count_sum:
		w_count[w['_id']] = w['count']

	# helpers.word_cloud(w_count, sentiment + "_words")


# Wordcount EMOJI
for sentiment in constants.TWITTER_SENTIMENTS:
	print("GENERATING EMOJI %s WORDCLOUD" % sentiment)

	emoji_count_sum = mongo_functions.aggregate('tweet', [
		{"$match": {"sentiment": sentiment}},
		{"$project": {"emojis": 1}},
		{"$unwind": "$emojis"},
		{"$group": {"_id": "$emojis", "count": {"$sum": "$count"}}}
	])

	# converting results to dict
	emj_count = {}
	for w in emoji_count_sum:
		emj_count[w['_id']] = w['count']

	helpers.word_cloud(emj_count, sentiment + "_emojis", True)

# Wordcount EMOTICONS
for sentiment in constants.TWITTER_SENTIMENTS:
	print("GENERATING EMOTICON %s WORDCLOUD" % sentiment)

	emoticon_count_sum = mongo_functions.aggregate('tweet', [
		{"$match": {"sentiment": sentiment}},
		{"$project": {"emoticons": 1}},
		{"$unwind": "$emoticons"},
		{"$group": {"_id": "$emoticons", "count": {"$sum": 1}}}
	])

	# converting results to dict
	emtc_count = {}
	for w in emoticon_count_sum:
		emtc_count[w['_id']] = w['count']

	# helpers.word_cloud(emtc_count, sentiment + "_emoticons")

time_end = time.time()
time_lapsed = time_end - time_start
print("TIME MONGO WORDCLOUDS " + str(time_lapsed))

mongo_functions.mongo_disconnect()
