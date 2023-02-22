import mongo_functions
import constants
import helpers

mongo_functions.mongo_connect()

for sentiment in constants.LEXICAL_RESOURCES_FILES:

	if sentiment.lower() in constants.TWITTER_SENTIMENTS:
		for file_name in constants.LEXICAL_RESOURCES_FILES[sentiment]:
			for source in constants.LEXICAL_RESOURCES_SOURCES:
				if source in file_name:
					sentiment = sentiment.lower()

					n_lex_words = mongo_functions.aggregate('lex_resources_words', [
						{'$match': {'sentiment': sentiment, 'source': source}},
						{'$count': 'string'}
					])
					n_lex_words = int(n_lex_words[0]['string'])

					n_twitter_words = mongo_functions.aggregate('tweet', [
						{'$match': {'sentiment': sentiment}},
						{'$project': {'keys': {'$objectToArray': '$word_count'}}},
						{'$unwind': '$keys'},
						{'$group': {'_id': '$keys.k'}},
						{'$group': {'_id': None, 'count': {'$sum': 1}}}
					])
					n_twitter_words = n_twitter_words[0]['count']

					# n_shared_words
					# temp collection con le distinct words di tweet
					mongo_functions.drop_collection('tempCollection1')
					mongo_functions.drop_collection('tempCollection2')

					mongo_functions.aggregate('tweet', [
						{"$match": {"sentiment": sentiment}},
						{"$project": {"keys": {"$objectToArray": "$word_count"}}},
						{"$unwind": "$keys"},
						{"$group": {"_id": "$keys.k"}},
						{"$project": {"_id": 0, "word": "$_id"}},
						{"$out": "tempCollection1"}
					])
					mongo_functions.aggregate('lex_resources_words', [
						{"$match": {"sentiment": sentiment, "source": source}},
						{"$project": {"_id": 0, "word": "$word"}},
						{"$out": "tempCollection2"}
					])

					n_shared_words = mongo_functions.aggregate('tempCollection1', [
						{"$lookup": {"from": "tempCollection2", "localField": "word", "foreignField": "word",
									 "as": "joined_docs"}},
						{"$unwind": "$joined_docs"},
						{"$count": "total_count"}
					])
					n_shared_words = n_shared_words[0]['total_count']

					mongo_functions.drop_collection('tempCollection1')
					mongo_functions.drop_collection('tempCollection2')


					print("SENTIMENT: %s	SOURCE: %s\n" % (sentiment, source))
					print("n_shared_words: %s" % (str(n_shared_words)))
					print("n_lex_words: %s" % (str(n_lex_words)))
					print("n_twitter_words: %s\n" % (str(n_twitter_words)))


mongo_functions.mongo_disconnect()

