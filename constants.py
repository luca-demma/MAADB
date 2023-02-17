DATA_PATH = "./data/"

LEXICAL_RESOURCES_PATH = DATA_PATH + "Risorse lessicali/Archive_risorse_lessicali/"
LEXICAL_RESOURCES_FOLDERS = ["Anger", "Anticipation", "Disgust-Hate", "Fear", "Hope", "Joy", "Like-Love", "Neg", "Pos", "Sadness", "Surprise", "Trust"]

# incompleto
LEXICAL_RESOURCES_FILES = {
	"Anger": ["EmoSN_anger.txt", "NRC_anger.txt", "sentisense_anger.txt"],
	"Anticipation": ["NRC_anticipation.txt", "sentisense_anticipation.txt"],
	"Disgust-Hate": ["NRC_disgust.txt", "sentisense_disgust.txt", "sentisense_hate.txt"]
}
LEXICAL_RESOURCES_SOURCES = ["EmoSN", "NRC", "sentisense", "GI", "HL", "LIWC"]

TWITTER_MESSAGES_PATH = DATA_PATH + "Twitter messaggi/"
TWITTER_SENTIMENTS = ["anger", "anticipation", "disgust", "fear", "joy", "sadness", "surprise", "trust"]

TWITTER_DATASETS_PATHS = []
for sentiment in TWITTER_SENTIMENTS:
	TWITTER_DATASETS_PATHS.append(TWITTER_MESSAGES_PATH + "dataset_dt_" + sentiment + "_60k.txt")

