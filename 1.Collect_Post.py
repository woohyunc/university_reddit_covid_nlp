import praw
import prawcore
import pandas as pd
from datetime import datetime
import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')
nltk.download('punkt')
from nltk.tokenize import word_tokenize
import re
import string

def contains_covid(str):
    string = str.lower();
    if(("cov" in string) or ("rona" in string) or ("pandemic" in string) or ("epidemic" in string) or ("vaccin" in string) or ("mask" in string) or ("sars" in string)):
        return True
    return False;

reddit = praw.Reddit(
                     client_id="",
                     client_secret="",
                     user_agent="",
                     username="",
                     password="",
                     )
uofm = reddit.subreddit('ucf')
flair_template = uofm.flair.link_templates
flair_list = [[flair['text']] for flair in flair_template]
search_flair = 'flair:"COVID-19"'
posts = []
usernames = []
dates = []

covid_posts = []
covid_usernames = []
covid_dates = []
#Use i to check the number of posts in each category
#Start with COVID-19 because it is our main focus
i=0;
j=0;
punctuation='''!()-.[]{};:'"“‘’\, <>/?@#$%^&*_~'''
print("COVID-19")

for search_flair in flair_list:
    print(search_flair)
    try:
        for post in uofm.search(search_flair, syntax = 'lucene', limit=1000):
            username = post.author.name
            ts = int(post.created_utc)
            if ts < 1584662400:
                continue
            title = post.title
            title = re.sub(r'\d+', '', title)
            text = post.selftext
            text = re.sub(r'\d+', '', text)
            alltext = title+" . "+text
            words = alltext.split(' ')
            blacklist = []
            for word in words:
                if(('.com' in word) or ('.edu' in word) or ('www' in word) or ('https' in word) or ('Ph.' in word) or ('M.D' in word) or ('Dr.' in word) or ('Mr.' in word) or ('Mrs.' in word)):
                    blacklist.append(word)
            querywords = alltext.split(' ')
            resultwords  = [word for word in querywords if word not in blacklist]
            alltext = ' '.join(resultwords)
            parts = alltext.split('.')
            for allparts in parts:
                allparts = allparts.translate(alltext.maketrans("","", string.punctuation))
                allparts = allparts.strip()
                allparts = word_tokenize(allparts)
                text_without_sw = [word for word in allparts if (len(word) <30) and (not word in (stopwords.words('english')))]

                if len(text_without_sw) > 1:
                    posts.append([text_without_sw])
                    usernames.append(getattr(post.author,'name'))
                    dates.append(datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S'))
                    if "'rona virus 😷" in search_flair:
                        covid_posts.append([text_without_sw])
                        covid_usernames.append(getattr(post.author,'name'))
                        covid_dates.append(datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S'))
                        j=j+1;
                    i=i+1;
    except(prawcore.exceptions.BadRequest, prawcore.exceptions.NotFound, prawcore.exceptions.ResponseException,prawcore.exceptions.Forbidden,prawcore.exceptions.ServerError):
        continue
print(i)
print(j)
#There were 241 posts under the COVID-19 Flair, 996 sentences after weeding out links/emoji/blanks
posts = pd.DataFrame(posts, columns=['Text'])
posts['Username'] = usernames
posts['Dates'] = dates

#Create CSV file of the desired posts
posts.to_csv(r'/Users/macintosh/Desktop/All Posts.csv',index = False, header=True)

covid_posts = pd.DataFrame(covid_posts, columns=['Text'])
covid_posts['Username'] = covid_usernames
covid_posts['Dates'] = covid_dates

covid_posts.to_csv(r'/Users/macintosh/Desktop/Covid Posts.csv',index = False, header=True)
