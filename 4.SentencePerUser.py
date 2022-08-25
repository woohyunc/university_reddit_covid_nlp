import pandas as pd
import string
from csv import reader
import praw
import prawcore
from datetime import datetime
reddit = praw.Reddit(
                     client_id="",
                     client_secret="",
                     user_agent="",
                     username="",
                     password="",
                     )

user_dict = {}

user_cakeday = {}
user_comment_karma = {}
user_post_karma = {}
user_num_post = {}
user_num_comment = {}

with open('/Users/macintosh/Desktop/User Freq.csv',encoding = "ISO-8859-1") as read_obj:
    csv_reader = reader(read_obj)
    for row in csv_reader:
        for string in row:
            print(string)
            if string in user_dict.keys():
                user_dict[string] = user_dict[string]+1
            else:
                try:
                    user = reddit.redditor(string)
                    ts = int(getattr(user,'created_utc','0'))
                    user_cakeday[string] = datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
                    user_comment_karma[string] = getattr(user,'comment_karma',0)
                    user_post_karma[string] = getattr(user,'link_karma',0)
                    
                    j = 0
                    k = 0
                    if (getattr(user,'comment_karma',0) + getattr(user,'link_karma',0)) != 0:
                        comments = getattr(user,'comments',0).new(limit = None)
                        for c in comments:
                            j = j+1
                
                        posts = getattr(user,'submissions',0).new(limit = None)
                        for p in posts:
                            k = k+1
                
                    user_num_comment[string] = j
                    user_num_post[string] = k
                    user_dict[string] = 1
                except (prawcore.exceptions.BadRequest, prawcore.exceptions.NotFound, prawcore.exceptions.ResponseException,prawcore.exceptions.Forbidden):
                    continue

usernames = list(user_dict.keys())
num_sentences = list(user_dict.values())
cakeday = list(user_cakeday.values())
post_karma = list(user_post_karma.values())
comment_karma = list(user_comment_karma.values())
num_post = list(user_num_post.values())
num_comment = list(user_num_comment.values())

users = pd.DataFrame(usernames, columns=['Username'])
users['Num_Sentences'] = num_sentences
users['Cakeday'] = cakeday
users['Post Karma'] = post_karma
users['Comment Karma'] = comment_karma
users['Num Posts'] = num_post
users['Num Comments'] = num_comment

users.to_csv(r'/Users/macintosh/Desktop/Sentences_per_User.csv',index = False, header=True)

