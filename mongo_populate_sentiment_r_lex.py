import constants
import mongo_functions
import helpers

mongo_functions.mongo_connect()

for sentiment in constants.LEXICAL_RESOURCES_FILES:
	for file_name in constants.LEXICAL_RESOURCES_FILES[sentiment]:
		for source in constants.LEXICAL_RESOURCES_SOURCES:
			if source in file_name:
				row = {
					"sentiment": sentiment.lower(),
					"source": source
				}
				mongo_functions.insert_one('lex_resources', row)

mongo_functions.mongo_disconnect()
