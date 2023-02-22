import mongo_functions


def populate(words):
	records = []

	mongo_functions.mongo_connect()

	for sentiment in words:
		for word in words[sentiment]:
			for source in words[sentiment][word]:
				source_obj = mongo_functions.find_one('lex_resources', {'sentiment': sentiment, 'source': source})
				source_id = source_obj['_id']
				obj = {'word': word, 'sentiment': sentiment, 'source': source, 'source_id': source_id}
				records.append(obj)

	mongo_functions.insert_many('lex_resources_words', records)

	mongo_functions.mongo_disconnect()
