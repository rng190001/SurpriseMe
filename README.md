# ![image](https://github.com/user-attachments/assets/41e74e54-f7e3-4702-b03f-f89ef368e109) SurpriseMe

Welcome to SurpriseMe, a chatbot-driven platform designed to help users find the perfect gifts for Valentine's Day and Christmas! Whether you’re searching for something sweet and romantic or something festive and merry, our app offers tailored gift suggestions based on user preferences.

##  ![image](https://github.com/user-attachments/assets/377e33a0-eb64-45c9-bac2-bcac2a113391) Features
  - **Holiday-Themed Gift Suggestions:** Curated for both Valentine's Day and Christmas, ensuring a unique and relevant selection of gift ideas.
  - **Personalized Recommendations:** Get suggestions based on key factors like age, gender, relationship, occasion, hobbies, and budget.
  - **Interactive Chatbot:** Users can interact with a chatbot to easily find gift ideas, narrowing down options through a conversation.
  - **User-Friendly Design:** A clean and intuitive interface.
  - **Gift Links & Images:** Each recommendation comes with the gift title, gift description, approximated price range, and lastly the link to the gift.
  - **NLP Techniques & Models:**
      - BERT (Bidirectional Encoder Representations from Transformers) was used to create context-aware embeddings for the user queries and the dataset. This model captures deep relationships between words beyond surface-level similarity. This model then is producing a cosine similarity value that measures how similar two sentences are to each other.
      - TF-IDF was used to calculate how important a word is in the context of the gift dataset. This model ultimately helps us measure the similarity between the user input and gift descriptions from the gift database.
      - Cosine Similarity was used to calculate the final measures to capture similar gifts to the user queries. The TF-IDF scores and the BERT scores were weighted to calculate the overall similarities of the gifts.
    
## ![image](https://github.com/user-attachments/assets/b37223d7-f6f0-4b1e-bbac-3a67b167834b) Dataset 
  - The dataset is **custom-made** to ensure accurate and personalized recommendations for major holidays, such as Christmas and Valentine's Day.
  - It includes fields such as Holiday, Gender, Age, Relationship, Budget, Max Budget, Associated Hobbies, Gift Title, Gift Summary, Rating, and Link.
  - The data is preprocessed to extract relevant information, helping to provide tailored gift recommendations for the user.

## ![image](https://github.com/user-attachments/assets/8a972332-f13b-49d9-b180-3d13b239e718) Input

<img width="1432" alt="Screenshot 2024-11-25 at 4 57 09 PM" src="https://github.com/user-attachments/assets/dfc50b45-710c-481d-a185-5b7b840b4e97">

  - The following input was given in the textbox: I want to get an anniversary gift for my wife who loves jewelry and loves to cook.
    - Remember the user can be as vague and as detailed as they would like to be!

## ![image](https://github.com/user-attachments/assets/d0830545-5713-469e-b402-2a40a71f50dd) Output

<img width="1432" alt="Screenshot 2024-11-25 at 4 59 33 PM" src="https://github.com/user-attachments/assets/5c2b73f9-53aa-4874-85e9-968a7aa500a1">

  - The user will receive a list of gift suggestions tailored to their query, with the top 5 recommendations displayed initially. They can choose to view additional options or request new recommendations with a new query. 

## ![image](https://github.com/user-attachments/assets/8f182ae4-c03f-4ffc-ad59-c4597001cf30) Try it Yourself!

1. Clone the repo
```sh
git clone https://github.com/rng190001/SurpriseMe.git
```

2. Install all of the python packages
```sh
pip3 install flask transformers torch pandas nltk numpy==1.25.2 scikit-learn regex
```
  - Make sure that the numpy version is numpy==1.25.2
    
3. Manually download the needed resources
```sh
python3 -m nltk.downloader stopwords punkt wordnet averaged_perceptron_tagger averaged_perceptron_tagger_eng
```

4. Start the python script and Flask application
```sh
python3 main.py
```
  - The flask application will typically be running on http://127.0.0.1:5000/ on your local computer

