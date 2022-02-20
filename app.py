import streamlit as st
from praw.models import Submission

from interest import get_interest_rater
from prawutils import get_reddit
from sqlitedict import SqliteDict

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


with st.sidebar:
    subreddit = st.text_input('subreddit', value='all')


submission_generator = (
    reddit
    .subreddit(display_name=subreddit)
    .top(time_filter='day')
)

num_links_per_refresh = 25

i = 0
submissions = []
while i < num_links_per_refresh:
    submissions.append(next(submission_generator))
    i += 1

submissions = sorted(submissions, key=get_interest_cached, reverse=True)

for i, submission in enumerate(submissions):

    comments_url = f'https://www.reddit.com{submission.permalink}'
    content_url = submission.url if len(submission.selftext) > 0 else comments_url

    st.markdown(f'''
    [{i}] *From r/{submission.subreddit.display_name}*

    [**{submission.title}**]({content_url})

    [{submission.num_comments} comments]({comments_url})
    Interest: {get_interest_cached(submission):.2f}
    Score: {submission.score}
    Upvote ratio: {submission.upvote_ratio}

    ----
    ''')
