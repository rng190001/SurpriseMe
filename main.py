#Uncomment the downloads when running for the first time
import pandas as pd
import nltk
import re
import math
from nltk import word_tokenize
from nltk import sent_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords, wordnet
from nltk import word_tokenize, pos_tag, ne_chunk
#nltk.download('punkt')
#nltk.download('stopwords')
#nltk.download('punkt_tab')
#nltk.download('wordnet')
#nltk.download('maxent_ne_chunker_tab')
#nltk.download('words')
#nltk.download('averaged_perceptron_tagger_eng')
#nltk.download('averaged_perceptron_tagger')
stopwords = set(stopwords.words('english'))

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

def calculate_cosine_similarity(vector1, vector2):
    # Calculate the dot product and magnitudes
    dot_product = sum(vector1[word] * vector2[word] for word in vector1 if word in vector2)
    magnitude1 = math.sqrt(sum(value**2 for value in vector1.values()))
    magnitude2 = math.sqrt(sum(value**2 for value in vector2.values()))

    if not magnitude1 or not magnitude2:
        return 0.0
    return dot_product / (magnitude1 * magnitude2)

def create_tf_idf_matrix(gift_descriptions, gift_word_counts, word_document_counts):
    tf_idf_matrix = {}
    for gift_id, word_counts in gift_word_counts.items():
        tf_idf_vector = calculate_tf_idf_vector(word_counts, gift_descriptions[gift_id], word_document_counts)
        tf_idf_matrix[gift_id] = tf_idf_vector
    return tf_idf_matrix

def calculate_tf_idf_vector(word_counts, description, word_document_counts):
    total_terms = sum(word_counts.values())
    tf_idf_vector = {}
    for word in word_counts:
        term_frequency = word_counts[word] / total_terms
        inverse_document_frequency = math.log10(len(description) / word_document_counts[word]) if word in word_document_counts else 0
        tf_idf_vector[word] = term_frequency * inverse_document_frequency
    return tf_idf_vector

def find_similar_gifts(gift_id, tf_idf_matrix):
    target_vector = tf_idf_matrix[gift_id]
    similarities = {}
    for other_id, vector in tf_idf_matrix.items():
        if other_id != gift_id:
            similarity = calculate_cosine_similarity(target_vector, vector)
            similarities[other_id] = similarity
    # Sort by similarity score in descending order
    return dict(sorted(similarities.items(), key=lambda item: item[1], reverse=True)[:10])

def main():

    # Read in the CSV file
    giftsFile = "./giftDB.csv"
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

    # Create TF-IDF matrix
    tf_idf_matrix = create_tf_idf_matrix(gift_descriptions, gift_word_counts, word_document_counts)

    # Example: Find similar gifts to a specific gift ID
    gift_id = 52
    similar_gifts = find_similar_gifts(gift_id, tf_idf_matrix)

    print(f"Top 10 similar gifts to {gift_id}:")
    for similar_gift_id, similarity in similar_gifts.items():
        print(f"Gift ID: {similar_gift_id}, Similarity: {similarity:.4f}")

# Runs the whole program
if __name__ == '__main__':
    main()