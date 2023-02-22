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

					print("SENTIMENT: %s	SOURCE: %s\n" % (sentiment, source))
					# print("n_shared_words: %s" % (str(n_shared_words)))
					print("n_lex_words: %s" % (str(n_lex_words)))
					print("n_twitter_words: %s\n" % (str(n_twitter_words)))

