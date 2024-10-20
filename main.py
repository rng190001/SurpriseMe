import pandas as pd
import nltk
import re
import math
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
def calculate_tf_idf(word, gift_descriptions, gift_word_counts, word_document_counts):
    # Calculate TF-IDF any given word
    tf_idfs = dict()

    # Go through each gift and calculate the word's tf-idf in relation to that gift
    for key, value in gift_word_counts.items():
        # If this word is used to describe this gift, calculate its tf-idf
        if word in value:
            # TF = # of times word is used for gift description/total number of terms for this gift description
            term_frequency = gift_word_counts[key][word]/(len(gift_descriptions[key]))

            # IDF = log(# of gifts in dataset/# of gifts containing word in its description)
            inverse_doc_frequency = math.log10(len(gift_descriptions)/word_document_counts[word])

            tf_idfs[key] = (term_frequency * inverse_doc_frequency)
        else:
            # If the word is not used to describe the gift, don't add it to the tf-idf dictionary
            # tf_idfs[key] = 0
            continue
    
    # After calculating the tf-idfs for every gift and the given word, sort in descending
    # order to see the highest tf-idfs at the top
    sorted_tf_idfs = dict(sorted(tf_idfs.items(), key=lambda item: item[1], reverse=True))

    for key, value in sorted_tf_idfs.items():
        print(key, "- description ", gift_descriptions[key], " with TF-IDF: ", value)

    return sorted_tf_idfs

def get_document_counts(giftDescriptions):
    # Create a dictionary where key: word, value: list of giftIDs
    document_counts_for_word = dict()

    # For each word in a gift description, create a list of giftIDs that it is used to describe
    for key, value in giftDescriptions.items():
        for word in value:
            # If the key (current giftID) is not in the giftID list for the word, add it
            if word in document_counts_for_word and key not in document_counts_for_word[word]:
                document_counts_for_word[word] += [key]
            # If the key already is in the giftID list, move on
            elif word in document_counts_for_word and key in document_counts_for_word[word]:
                continue
            else:
            # Otherwise, make a new entry for the word and a corresponding giftID list as the value
                document_counts_for_word[word] = [key]

    # Replace the list of giftIDs that the word occurs in with the length of the list,
    # allowing us to know how many gift descriptions the word occurs in
    for key, value in document_counts_for_word.items():
        document_counts_for_word[key] = len(value)

    ''' TO TEST
    i = 0
    for key, value in document_counts_for_word.items():
        i += 1
        print(key, value)
        if i == 50:
            break
    '''

    return document_counts_for_word

def get_word_counts(giftDescriptions):
    # Create a dictionary where key: gift ID, value: dictionary of word counts 
    gift_word_counts = dict()

    # Go through the description of each gift
    for key, value in giftDescriptions.items():
        # Create a dictionary at the value
        gift_word_counts[key] = dict()
        # Get the counts of each word for that specific gift description
        for word in value:
            if word in gift_word_counts[key]:
                gift_word_counts[key][word] += 1
            else:
                gift_word_counts[key][word] = 1
    
        ''' TO TEST
        i = 0
        for key, value in word_counts.items():
            i += 1
            print(key, value)
            if i == 30:
                break
        '''
    
    return gift_word_counts

# Convert nltk POS tags to WordNet POS tags
def get_wordnet_pos(tree_tag):
    # Assign Verb tag
    if tree_tag.startswith('V'):
        return wordnet.VERB  
    # Assign Noun tag
    elif tree_tag.startswith('N'):
        return wordnet.NOUN
    # Assign Adjective tag
    elif tree_tag.startswith('J'):
        return wordnet.ADJ
    # Assign Adverb tag
    elif tree_tag.startswith('R'):
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
    no_stopwords = [word for word in cleaned_sentence if word not in stopwords and len(word) > 2]

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

    # Preprocess associated hobbies: tokenize, remove stopwords, lemmatize
    preprocessed_giftsData['Associated Hobbies'] = preprocessed_giftsData['Associated Hobbies'].apply(lambda x: preprocess_data(x))

    # Preprocess gift titles: tokenize, remove stopwords, lemmatize
    preprocessed_giftsData['Gift Title'] = preprocessed_giftsData['Gift Title'].apply(lambda x: preprocess_data(x))

    # Preprocess gift summaries: tokenize, remove stopwords, lemmatize
    preprocessed_giftsData['Gift Summary'] = preprocessed_giftsData['Gift Summary'].apply(lambda x: preprocess_data(x))

    # Create a dictionary where key: gift ID, value: title + summary combined
    gift_descriptions = dict(zip(preprocessed_giftsData['Gift ID'], preprocessed_giftsData['Gift Title']+preprocessed_giftsData['Gift Summary']))
   
    # Get the word counts of every word in the description of each gift
    gift_word_counts = get_word_counts(gift_descriptions)

    # Get the number of documents that each word occurs in
    word_document_counts = get_document_counts(gift_descriptions)

    # Calculate tf-idfs using a given word
    calculate_tf_idf('mug', gift_descriptions, gift_word_counts, word_document_counts)

    # Filter gifts based on occasion -- We can use similar logic to filter based on user's response
    # before applying cosine similarity for gifts closely related to associated hobbies/items
    christmas_gifts = preprocessed_giftsData[preprocessed_giftsData['Holiday'] == 'Christmas']
    print(christmas_gifts)

    # print(preprocessed_giftsData['Associated Hobbies'])
    # print(gift_descriptions[200])
    # print(giftsData['Gift Summary'])
    # print(preprocessed_giftsData['Gift Summary'])

# Runs the whole program
if __name__ == '__main__':
    main()