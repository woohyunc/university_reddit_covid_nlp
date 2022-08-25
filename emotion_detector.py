import os;
os.environ['KERAS_BACKEND'] = 'theano'
import pandas as pd
from emotion_predictor import EmotionPredictor

university_list = ["Kentucky","MSU","NCSU","NJIT","NYU","OSU","TT","UFL",
                   "UIUC","UM", "UMKC","UTK","UWMad","WSU"]

for university in university_list:
    
    pd.options.display.max_colwidth = 150
    pd.options.display.width = 500
    model = EmotionPredictor(classification='plutchik', setting='mc', use_unison_model=True)

    df = pd.read_csv(f"/Users/macintosh/Desktop/CSV Text Only Files/{university} All.csv")
    tweets = df[df.columns[0]].to_list()
    print(f"/Users/macintosh/Desktop/CSV Text Only Files/{university} All.csv")

    print(f"{university} Plutchik Started")
    predictions = model.predict_classes(tweets)
    predictions.to_csv(f'{university}-Plutchik.csv',index = False, header=True)
    #probabilities = model.predict_probabilities(tweets) >> If you want to see the probabilities for each emotion


    ######################

    model = EmotionPredictor(classification='ekman', setting='mc', use_unison_model=True)
    print(f"{university} Ekman Started")
    predictions = model.predict_classes(tweets)
    predictions.to_csv(f'{university}-Ekman.csv',index = False, header=True)


    ######################

    model = EmotionPredictor(classification='poms', setting='mc', use_unison_model=True)
    print(f"{university} POMS Started")
    predictions = model.predict_classes(tweets)
    predictions.to_csv(f'{university}-Poms.csv',index = False, header=True)



#Reference : https://github.com/nikicc/twitter-emotion-recognition
