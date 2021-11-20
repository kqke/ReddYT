from BasePicker import BasePicker
import praw as reddit


class RedditPicker(BasePicker):

    def __init__(self):
        super().__init__()
        self.reddit = reddit.Reddit(client_id=self.config.get('Reddit', 'client_id'),
                                    client_secret=self.config.get('Reddit', 'client_secret'),
                                    user_agent=self.config.get('Reddit', 'user_agent'))
        self.subreddit = self.reddit.subreddit(self.config.get('Reddit', 'subreddit'))
        self.submissions = self.subreddit.hot(limit=self.config.getint('Reddit', 'submission_limit'))

    def pick(self, *args, **kwargs):
        return self.submissions.next()

