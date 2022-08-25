from bertopic import BERTopic
from sklearn.datasets import fetch_20newsgroups

university_list = [] #Add universities as needed

for university in university_list:
    with open(university+'.txt') as f:
        docs = f.readlines()
    print(type(docs),type(docs[0]))
    model = BERTopic("roberta-base-nli-stsb-mean-tokens",
                     top_n_words = 20,
                     nr_topics = 5,
                     n_gram_range = (1, 2),
                     min_topic_size = 30,
                     n_neighbors = 15,
                     n_components = 5,
                     verbose=True)
    topics = model.fit(docs)
    topics = model.transform(docs)
    print(model.get_topics())
    print(model.get_topics_freq())
