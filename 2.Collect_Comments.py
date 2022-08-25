import praw
import prawcore
from praw.models import MoreComments
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
uofm = reddit.subreddit('UniversityofKentucky')
flair_template = uofm.flair.link_templates
flair_list = [[flair['text']] for flair in flair_template]
search_flair = 'flair:"COVID-19"'
comments = []
usernames = []
dates = []

covid_comments = []
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
    for post in uofm.search(search_flair, syntax = 'lucene', limit=1000):
        ts = int(post.created_utc)
        if ts < 1584662400:
            continue
        try:
            post.comments.replace_more(limit = None)
            comment_queue = post.comments[:]
            while comment_queue:
                comment = comment_queue.pop(0)
                username = post.author.name
                text = comment.body
                text = re.sub(r'\d+', '', text)
                words = text.split(' ')
                blacklist = []
                for word in words:
                    if(('.com' in word) or ('.edu' in word) or ('www' in word) or ('https' in word) or ('Ph.' in word) or ('M.D' in word) or ('Dr.' in word) or ('Mr.' in word) or ('Mrs.' in word)):
                        blacklist.append(word)
                querywords = text.split(' ')
                resultwords  = [word for word in querywords if word not in blacklist]
                text = ' '.join(resultwords)
                parts = text.split('.')
                comment_queue.extend(comment.replies)
                for allparts in parts:
                    allparts = allparts.translate(text.maketrans("","", string.punctuation))
                    allparts = allparts.strip()
                    allparts = word_tokenize(allparts)
                    text_without_sw = [word for word in allparts if (len(word) <30) and (not word in (stopwords.words('english')))]
                    if len(text_without_sw) > 1:
                        comments.append([text_without_sw])
                        usernames.append(getattr(comment.author,'name','Deleted'))
                        dates.append(datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S'))
                        if "COVID-19" in search_flair:
                            covid_comments.append([text_without_sw])
                            covid_usernames.append(getattr(comment.author,'name','Deleted'))
                            ts1 = datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
                            covid_dates.append(ts1)
                            j=j+1;
                        i=i+1;
        except(prawcore.exceptions.BadRequest, prawcore.exceptions.NotFound, prawcore.exceptions.ResponseException,prawcore.exceptions.Forbidden,prawcore.exceptions.ServerError):
                continue
print(i)
print(j)
comments = pd.DataFrame(comments, columns=['Text'])
comments['Username'] = usernames
comments['Date'] = dates
comments.to_csv(r'/Users/macintosh/Desktop/All Comments.csv',index = False, header=True)

posts = pd.DataFrame(covid_comments, columns=['Text'])
posts['Username'] = covid_usernames
posts['Dates'] = covid_dates

posts.to_csv(r'/Users/macintosh/Desktop/Covid Comments.csv',index = False, header=True)

