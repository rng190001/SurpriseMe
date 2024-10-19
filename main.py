import pandas as pd
import nltk
import re
from nltk import word_tokenize
from nltk import sent_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords, wordnet
from nltk import word_tokenize, pos_tag, ne_chunk
stopwords = set(stopwords.words('english'))
'''
#UNCOMMENT IF RUNNING FOR FIRST TIME: After downloading this all once, you don't have to download it again
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('punkt_tab')
nltk.download('wordnet')
nltk.download('maxent_ne_chunker_tab')
nltk.download('words')
nltk.download('averaged_perceptron_tagger_eng')
nltk.download('averaged_perceptron_tagger')
'''
# Convert nltk POS tags to WordNet POS tags
def get_wordnet_pos(treebank_tag):
    if treebank_tag.startswith('J'):
        return wordnet.ADJ
    elif treebank_tag.startswith('V'):
        return wordnet.VERB
    elif treebank_tag.startswith('N'):
        return wordnet.NOUN
    elif treebank_tag.startswith('R'):
        return wordnet.ADV
    else:
        return wordnet.NOUN

def preprocess_data(text):
    # Create lemmatizer
    lemmatizer = WordNetLemmatizer()

    # Remove all punctuation, set all words to lower case, and split by spaces
    cleaned_sentence = re.sub(r'[^\w\s-]', ' ',text).lower()
    cleaned_sentence = re.split(r'\s+', cleaned_sentence.strip())

    # Now store all words that are not stopwords
    no_stopwords = [w for w in cleaned_sentence if w not in stopwords]

    # Assign Part of Speech tags to each token
    POS_tags = pos_tag(no_stopwords)

    # Lemmatize the words
    lemmatized_words = [lemmatizer.lemmatize(word, get_wordnet_pos(pos)) for word, pos in POS_tags]

    return lemmatized_words

def main():

    # Read in the CSV file
    giftsFile = "./GiftDatabase.csv"
    giftsData = pd.read_csv(giftsFile)

    # Drop any rows that have null cells
    giftsData = giftsData.dropna()

    # Create a copy of giftsData that we will use for computation, leave the original dataset
    # as is for output purposes
    preprocessed_giftsData = giftsData.copy()

    # Preprocess gift titles: tokenize, remove stopwords, lemmatize
    preprocessed_giftsData['Gift Title'] = preprocessed_giftsData['Gift Title'].apply(lambda x: preprocess_data(x))

    # Preprocess gift summaries: tokenize, remove stopwords, lemmatize
    preprocessed_giftsData['Gift Summary'] = preprocessed_giftsData['Gift Summary'].apply(lambda x: preprocess_data(x))

    # Create a dictionary where key: gift ID, value: title + summary combined 
    giftDescriptors = dict(zip(preprocessed_giftsData['Gift ID'], preprocessed_giftsData['Gift Title']+preprocessed_giftsData['Gift Summary']))
   
    print(giftDescriptors[200])
    # print(giftsData['Gift Summary'])
    # print(preprocessed_giftsData['Gift Summary'])

# Runs the whole program
if __name__ == '__main__':
    main()