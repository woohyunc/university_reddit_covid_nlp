# University_Reddit_NLP_Covid
Code used to crawl Reddit for Covid-19 related data using the PRAW API and conduct NLP on the collected texts. 

For emotion detection, I used a UNISON model which was trained on 3 different structures of emotion (Ekman, POMS, Plutchik). The trained weights can be found in the "models" folder. The model returns the probability of the text expressing each emotion. emotion_prediction model was adapted directly from https://github.com/nikicc/twitter-emotion-recognition

For sentiment alaysis, a pretrained RoBERTa model to score each text's sentiment between 0 and 1 (0 being extremeley negative and 1 being extremely positive). 

For concern classification, a pretrained BERT model was used to group texts into similar categories depending on the theme of their contents. Users can extract key-words from each category to give a label to each concern. 
