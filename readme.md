# Real Time Multilingual Content Interpreter and Receommender

This work is part of our Final Project Submission for the course Information Retrieval (CSE508) at IIIT Delhi.
The interpreter translates lyrics of any song in any language, given the song name and artist name (optional) to the preferred language, and also recommends similar songs 
based on the translation/meaning in the translated language.
The recommender stores tf-idf matrices in vector form and then uses cosine similarities to recommend top 'k' songs to the user.

For frontend  run:
cd frontend__ 
npm install__
npm start __

Dependencies for backend:
pip3 install google-cloud-translate__
pip3 install numpy__
pip3 install nltk__
pip3 install scikit-learn__
pip3 install pandas

Then run:
python3 manage.py server
