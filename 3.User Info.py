import praw
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
uofm = reddit.subreddit('nyu')
flair_template = uofm.flair.link_templates
flair_list = [[flair['text'],flair['id']] for flair in flair_template]
search_flair = 'flair:"COVID-19"'

usernames = []
cakedays = []
comment_karmas = []
link_karmas = []
total_karmas = []
num_posts = []
num_comments = []
icons = []

print(search_flair)
i=1
for post in uofm.search(search_flair, syntax = 'lucene', limit=5000):
    if((post.author.name not in usernames)):
        print("num_users: ",i)
        i= i+1
        ts = int(getattr(post.author,'created_utc','0'))

        usernames.append(getattr(post.author,'name'))
        cakedays.append(datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S'))
        comment_karmas.append(getattr(post.author,'comment_karma',0))
        link_karmas.append(getattr(post.author,'link_karma',0))
        total_karmas.append(getattr(post.author,'comment_karma',0) + getattr(post.author,'link_karma',0))
        j = 0
        k = 0
        if (getattr(post.author,'comment_karma',0) + getattr(post.author,'link_karma',0)) != 0:
            comments = getattr(post.author,'comments',0).new(limit = None)
            for c in comments:
                j = j+1

            posts = getattr(post.author,'submissions',0).new(limit = None)
            for p in posts:
                k = k+1
        num_comments.append(j)
        num_posts.append(k)

        icons.append(getattr(post.author,'icon_img','0'))


users = pd.DataFrame(usernames, columns=['Username'])
users['Cakeday'] = cakedays
users['Link Karma'] = link_karmas
users['Comment Karma'] = comment_karmas
users['Total Karma'] = total_karmas
users['Icon Link'] = icons
users['Num Comments'] = num_comments
users['Num Posts'] = num_posts

#Create CSV file of the desired posts
users.to_csv(r'/Users/macintosh/Desktop/User Info.csv',index = False, header=True)
