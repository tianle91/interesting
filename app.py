from functools import lru_cache

import streamlit as st
from praw.models import Submission

from interest import get_interest_rater
from prawutils import get_reddit

reddit = get_reddit()
rater = get_interest_rater()


@lru_cache(maxsize=1000000)
def get_interest(submission: Submission) -> float:
    s = f'''Title: {submission.title}
    Subreddit: {submission.subreddit.display_name}
    {submission.selftext}'''
    if len(submission.selftext) > 0 and submission.num_comments > 0:
        s += f'\n{submission.comments[0].body}'
    return rater(s[:1000])


submissions = list(reddit.front.top(time_filter='day'))
submissions.sort(key=get_interest, reverse=True)

for i, submission in enumerate(submissions):

    comments_url = f'https://www.reddit.com{submission.permalink}'
    content_url = submission.url if len(submission.selftext) > 0 else comments_url

    st.markdown(f'''
    [{i}] *From r/{submission.subreddit.display_name}*

    [**{submission.title}**]({content_url})

    [{submission.num_comments} comments]({comments_url})
    Interest: {get_interest(submission):.2f}
    Score: {submission.score}
    Upvote ratio: {submission.upvote_ratio}

    ----
    ''')
