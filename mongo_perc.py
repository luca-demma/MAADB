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


