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
    md_str = f'''
    [{i} *From r/{submission.subreddit.display_name}*]
    [**{submission.title}**](https://www.reddit.com{submission.permalink})'''

    if len(submission.selftext) == 0:
        if submission.url.endswith(('.jpg', '.png')):
            md_str += f'''
            <img src="{submission.url}" width="200">'''
        else:
            md_str += f'''
            [Content link]({submission.url})'''

    md_str += f'''
    Interest: `{get_interest(submission):.2f}`
    Score: `{submission.score}`
    Upvote ratio: `{submission.upvote_ratio}`
    '''
    st.markdown(md_str)
