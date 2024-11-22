# -*- coding: utf-8 -*-
"""SurpriseMe.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1myodxTWqaEeYzmkkDVZA3J_lfIWhgOwc
"""

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
    POS_tags = [(word, 'VBG') if word.endswith('ing') else (word, pos) for word, pos in pos_tag(no_stopwords)]

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

from transformers import AutoTokenizer, AutoModel
import torch

tokenizer = AutoTokenizer.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")
model = AutoModel.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")

def get_bert_embeddings(texts):
    """Generates embeddings for a list of texts using BERT."""
    tokens = tokenizer(
        texts,
        padding=True,
        truncation=True,
        max_length=512,
        return_tensors="pt"
    )
    with torch.no_grad():
        model_output = model(**tokens)
    # Average pooling of token embeddings
    embeddings = model_output.last_hidden_state.mean(dim=1)
    return embeddings

def ask_question(prompt):
    return input(f"{prompt}\nYou: ")

!pip install -U nltk

import pandas as pd
import nltk
import numpy as np
# Download necessary resources before other nltk imports
nltk.download('averaged_perceptron_tagger')
nltk.download('averaged_perceptron_tagger_eng')
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
import re
import math
from nltk import word_tokenize
from nltk import sent_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords, wordnet
from nltk import pos_tag
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics.pairwise import cosine_similarity
stopwords = set(stopwords.words('english'))


def split_database_by_holiday(gift_data, holiday):
    #Splits gift database by specified holiday.
    if holiday.lower() == "christmas":
        return gift_data[gift_data['Holiday'].str.contains("Christmas", case=False)]
    elif holiday.lower() == "anniversary":
        return gift_data[gift_data['Holiday'].str.contains("Anniversary", case=False)]
    return gift_data

def split_database_by_gender(gift_data, gender):
    #Splits gift database by specified holiday.
    if gender.lower() == "male":
        return gift_data[gift_data['Gender'].str.contains(r"\bMale\b", case=False, regex=True)]
    elif gender.lower() == "female":
        return gift_data[gift_data['Gender'].str.contains(r"\bFemale\b", case=False, regex=True)]
    return gift_data

def recommend_gifts_based_on_input(user_input, gift_data):
    # Preprocess input
    cleaned_input = preprocess_data(user_input)
    input_sentence = user_input

    #print(cleaned_input)

    # Split database by holiday
    if "christmas" in cleaned_input:
        filtered_data = split_database_by_holiday(gift_data, "Christmas")
    elif "anniversary" in cleaned_input:
        filtered_data = split_database_by_holiday(gift_data, "Anniversary")
    else:
        filtered_data = gift_data

    # Split database by gender
    male_keywords = {"male", "man", "boy", "boyfriend", "husband", "nephew", "grandson", "brother", "uncle", "father", "dad", "grandpa"}
    female_keywords = {"female", "woman", "girl", "girlfriend", "wife", "niece", "granddaughter", "sister", "aunt", "mother", "mom", "grandma"}
    if set(cleaned_input) & male_keywords:
        gender_filtered_data = split_database_by_gender(filtered_data, "Male")
    elif set(cleaned_input) & female_keywords:
        gender_filtered_data = split_database_by_gender(filtered_data, "Female")
    else:
        gender_filtered_data = filtered_data

    # Combine gift titles and summaries for vectorization
    gender_filtered_data['CombinedText'] = (gender_filtered_data['Gift Title'] + " " + gender_filtered_data['Gift Summary'] + " " + (gender_filtered_data['Relationship'] + " ") + " " + ((gender_filtered_data['Associated Hobbies'] + " ")*5)).apply(preprocess_data)
    gender_filtered_data['CombinedTextBERT'] = gender_filtered_data['CombinedText'].apply(lambda x: " ".join(x))

    # Get the word counts of every word in the description of each gift
    gift_word_counts = get_word_counts(gender_filtered_data['CombinedText'])

    # Get the number of documents that each word occurs in
    word_document_counts = get_document_counts(gender_filtered_data['CombinedText'])

    # Create TF-IDF matrix
    tf_idf_matrix = create_tf_idf_matrix(gender_filtered_data['CombinedText'], gift_word_counts, word_document_counts)

    # Compute TF-IDF vector for user input
    user_input_counts = {token: cleaned_input.count(token) for token in cleaned_input}
    user_tf_idf_vector = calculate_tf_idf_vector(user_input_counts, gender_filtered_data['CombinedText'], word_document_counts)

    #Calculate similarity scores
    similarity_scores = [
        calculate_cosine_similarity(user_tf_idf_vector, tf_idf_matrix[gift_id])
        for gift_id in tf_idf_matrix
    ]

    #BERT Similarity
    gift_texts = gender_filtered_data['CombinedTextBERT'].tolist()
    gift_embeddings = get_bert_embeddings(gift_texts)
    user_embedding = get_bert_embeddings([input_sentence])

    bert_similarity_scores = cosine_similarity(
        user_embedding.numpy(),
        gift_embeddings.numpy()
    ).flatten()

    #Normalize Scores
    scaler = MinMaxScaler()
    tfidf_similarity_scores = scaler.fit_transform(np.array(similarity_scores).reshape(-1,1)).flatten()
    bert_similarity_scores = scaler.fit_transform(bert_similarity_scores.reshape(-1, 1)).flatten()

    overall_similarity_scores = (
        0.4 * tfidf_similarity_scores +
        0.6 * bert_similarity_scores
    )

    #print("Overall Similarity Scores:", overall_similarity_scores)
    # Add similarity scores to the dataframe
    gender_filtered_data['Similarity'] = overall_similarity_scores

    # Sort by similarity score and return top recommendations
    recommendations = gender_filtered_data.sort_values(by='Similarity', ascending=False).head(50)

    return recommendations

def main():
    while True:
        print("\nWelcome to Surprise Me! Please input your option.")
        print("1. Surprise me with a gift!")
        print("2. Exit")

        # Get user input
        choice = input("Please enter your choice (1 or 2): ").strip()

        if choice == '1':
            # Logic for finding a new gift
            find_new_gift()
        elif choice == '2':
            print("Thank you for using Surprise Me! Goodbye!")
            break
        else:
            print("Invalid input. Please choose 1 or 2.")

def find_new_gift():
    print("\nLet's find a new gift!")
    # Get user input for gift preferences
    user_input = input("Describe the gift or holiday preferences in one sentence: ")
    recommendations = recommend_gifts_based_on_input(user_input, preprocessed_giftsData)

    # Pagination logic
    start_index = 0
    page_size = 5

    while True:
        # Display the current page of recommendations
        end_index = start_index + page_size
        current_page = recommendations.iloc[start_index:end_index]

        print(f"\nShowing recommendations {start_index + 1} to {min(end_index, len(recommendations))}:")
        for _, row in current_page.iterrows():
            print(f"Gift ID: {row['Gift ID']} Title: {row['Gift Title']}, Similarity: {row['Similarity']:.4f}")

        # Check if there are more items to display
        if end_index >= len(recommendations):
            print("\nNo more recommendations to show.")
            break

        # Ask the user if they want to see more
        user_choice = input("\nWould you like to see the next 5 recommendations? (yes/no): ").strip().lower()
        if user_choice not in ['yes', 'y']:
            print("Thank you for using Surprise Me!")
            break

        # Update start index for the next page
        start_index += page_size

# Example usage
if __name__ == "__main__":
    giftsFile = "./giftDB.csv"
    giftsData = pd.read_csv(giftsFile).dropna()

    #Preprocess data
    preprocessed_giftsData = giftsData.copy()
    main()
