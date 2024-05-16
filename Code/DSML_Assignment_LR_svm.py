#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 28 18:15:38 2024

@author: timbaettig
"""

"""
DS & ML
"""
#install packages
#!pip install -U spacy

#imoprt packages
import pandas as pd
from sklearn.model_selection import train_test_split
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
import nltk
nltk.download('stopwords')
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.metrics import classification_report, accuracy_score
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC


#import data
directory = "/Users/timbaettig/Library/Mobile Documents/com~apple~CloudDocs/00_Privat/00_EPFL/Courses/SS 2024/Data Science and Machine Learning/Project/Data/"
training = pd.read_csv(directory+"training_data.csv")
test = pd.read_csv(directory+"unlabelled_test_data.csv")

#data exploration

#data preparation
def preprocess_text(text):
    # Remove punctuation, digits, etc.
    text = ''.join([char for char in text if char.isalpha() or char.isspace()])
    # Lowercase
    text = text.lower()
    # Tokenization and remove stop words
    tokens = text.split()
    stop_words = set(stopwords.words('french'))
    tokens = [word for word in tokens if word not in stop_words]
    # Stemming
    stemmer = SnowballStemmer('french')
    tokens = [stemmer.stem(word) for word in tokens]
    return ' '.join(tokens)

training['processed_sentence'] = training['sentence'].apply(preprocess_text)

# Vectorize the training data
vectorizer = TfidfVectorizer(max_features=5000, ngram_range=(1,2))
X_train = vectorizer.fit_transform(training['processed_sentence'])
y_train = training['difficulty']

# Train SVM model as an alternative to logistic regression
svm_model = SVC(kernel='linear', probability=True, random_state=42)
svm_model.fit(X_train, y_train)

# Make predictions with SVM model


#------------------------------------------------------------------------------------------------
#Prediction Preparation 
test['processed_sentence'] = test['sentence'].apply(preprocess_text)

# Vectorize the test data
X_test = vectorizer.transform(test['processed_sentence'])

# Make predictions
predicted_difficulties = svm_model.predict(X_test)

# Create a submission DataFrame
submission = pd.DataFrame({
    'id': test['id'],
    'difficulty': predicted_difficulties
})

# Export to CSV
submission.to_csv(directory+'Outputs/prediction3_log_reg_svm.csv', index=False)