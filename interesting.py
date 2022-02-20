from praw.models import Submission
from sqlitedict import SqliteDict

from interest import get_interest_rater
from prawutils import get_reddit

reddit = get_reddit()
rater = get_interest_rater()
interest_cache_path = 'cached_interest.sqlite'


def get_interest(submission: Submission) -> float:
    s = f'''Title: {submission.title}
    Subreddit: {submission.subreddit.display_name}
    {submission.selftext}'''
    if len(submission.selftext) > 0 and submission.num_comments > 0:
        s += f'\n{submission.comments[0].body}'
    return rater(s[:1000])


def get_interest_cached(submission: Submission) -> float:
    with SqliteDict(interest_cache_path) as d:
        res = d.get(submission.id, None)
        if res is None:
            res = get_interest(submission)
            d[submission.id] = res
            d.commit()
    return res
