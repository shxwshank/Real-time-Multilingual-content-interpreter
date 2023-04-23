# Real time multilingual Content Interpreter for the Music industry and recommendation system

This work is part of our Final Project Submission for the course Information Retrieval (CSE508) at IIIT Delhi.
The interpreter translates lyrics of any song in any language, given the song name and artist name (optional) to the preferred language, and also recommends similar songs 
based on the translation/meaning in the translated language.
The recommender stores tf-idf matrices in vector form and then uses cosine similarities to recommend top 'k' songs to the user.

In order to run the code, please follow the following steps:
1. `python -m venv venv`
2. `pip3 install -r requirements.txt`
3. `python3 manage.py server`
