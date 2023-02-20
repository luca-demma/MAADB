import mongo_functions


def populate(words):
	records = []

	mongo_functions.mongo_connect()

	for sentiment in words:
		for word in words[sentiment]:
			for source in words[sentiment][word]:
				# TODO:
				# source_id_query = "SELECT ID FROM SENTIMENT_R_LEXICAL_RESOURCE WHERE SENTIMENT = '%s' AND LEXICAL_RESOURCE = '%s';"%(sentiment, source)
				# source_id = mysql_functions.exec_query(source_id_query, False, True)
				# source_id = source_id[0]
				# records.append((word, source_id))

	print(records)
	mongo_functions.insert_many('lex_resources_words', records)

	mongo_functions.mongo_disconnect()