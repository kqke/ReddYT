from praw import Reddit
from bloom_filter import BloomFilter

from reddit_utils import *

# b_filter = BloomFilter(filename=BF_path)

reddit = Reddit(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, user_agent=USER_AGENT)

for submission in reddit.subreddit('WatchPeopleDieInside').hot(limit=10):
    print(submission.title)
    print(submission.url)