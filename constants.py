import multiprocessing

CPU_COUNT = multiprocessing.cpu_count()

DATA_PATH = "./data/"

LEXICAL_RESOURCES_PATH = DATA_PATH + "Risorse_lessicali/Archive_risorse_lessicali/"
# LEXICAL_RESOURCES_FOLDERS = ["Anger", "Anticipation", "Disgust", "Fear", "Hope", "Joy", "Like", "Neg", "Pos", "Sadness", "Surprise", "Trust"]

LEXICAL_RESOURCES_FILES = {
	"Anger": ["EmoSN_anger.txt", "NRC_anger.txt", "sentisense_anger.txt"],
	"Anticipation": ["NRC_anticipation.txt", "sentisense_anticipation.txt"],
	"Disgust": ["NRC_disgust.txt", "sentisense_disgust.txt"],
	"Hate": ["sentisense_hate.txt"],
	"Fear": ["NRC_fear.txt", "sentisense_fear.txt"],
	"Hope": ["sentisense_hope.txt"],
	"Joy": ["EmoSN_joy.txt", "NRC_joy.txt", "sentisense_joy.txt"],
	"Like": ["sentisense_like.txt"],
	"Love": ["sentisense_love.txt"],
	"Neg": ["GI_NEG.txt", "HL-negatives.txt", "listNegEffTerms.txt", "LIWC-NEG.txt"],
	"Pos": ["GI_POS.txt", "HL-positives.txt", "listPosEffTerms.txt", "LIWC-POS.txt"],
	"Sadness": ["NRC_sadness.txt", "sentisense_sadness.txt"],
	"Surprise": ["NRC_surprise.txt", "sentisense_surprise.txt"],
	"Trust": ["NRC_trust.txt"]
}

LEXICAL_RESOURCES_SOURCES = ["EmoSN", "NRC", "sentisense", "GI", "HL", "LIWC", "EffTerms"]

TWITTER_MESSAGES_PATH = DATA_PATH + "Twitter messaggi/"
TWITTER_SENTIMENTS = ["anger", "anticipation", "disgust", "fear", "joy", "sadness", "surprise", "trust"]

TWITTER_DATASETS_PATHS = []
for sentiment in TWITTER_SENTIMENTS:
	TWITTER_DATASETS_PATHS.append(TWITTER_MESSAGES_PATH + "dataset_dt_" + sentiment + "_60k.txt")

