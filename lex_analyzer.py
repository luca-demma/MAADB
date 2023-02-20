import constants
import helpers
import mongo_populate_word_r_source
import sql_populate_word_r_source

# [sentiment][word][lex_resource_source]
words = helpers.multi_dict(3, int)

# per ogni cartella delle risorse lessicali
for lex_folder in constants.LEXICAL_RESOURCES_FILES:
	# per ogni file presente nella cartella
	for lex_file in constants.LEXICAL_RESOURCES_FILES[lex_folder]:
		lex_file_strings_list = helpers.read_file(constants.LEXICAL_RESOURCES_PATH + lex_folder + "/" + lex_file)
		# per ogni riga del file
		for word in lex_file_strings_list:
			# removing \n from every
			word = word.replace('\n', '')
			# saltiamo le word che contengono l'underscore che sono parole composte, così come suggerito dalla prof
			if not('_' in word):
				sentiment = lex_folder.lower()
				lex_resource_source = ""
				# prendiamo la source dal nome del file
				for source in constants.LEXICAL_RESOURCES_SOURCES:
					if source in lex_file:
						lex_resource_source = source
						break
				words[sentiment][word][lex_resource_source]


# sql_populate_word_r_source.populate(words)
mongo_populate_word_r_source.populate(words)
