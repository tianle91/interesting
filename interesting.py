import asyncio
import os
from typing import Dict, List
from urllib.parse import urljoin

import requests
from praw.models import Submission
from sqlitedict import SqliteDict

from prawutils import get_reddit

reddit = get_reddit()
interest_cache_path = 'cached_interest.sqlite'

HF_INFERENCE_URL = os.getenv('HF_INFERENCE_URL')


async def get_interest(submission: Submission) -> float:
    body = f'''Title: {submission.title}
    Subreddit: {submission.subreddit.display_name}
    {submission.selftext}'''
    if len(submission.selftext) > 0 and submission.num_comments > 0:
        body += f'\n{submission.comments[0].body}'
    url = urljoin(HF_INFERENCE_URL, 'gpt2loss')
    return float(requests.post(url, json=body[:1000]).json()['loss'])


async def get_interests(submissions: List[Submission]) -> Dict[str, float]:
    res = {}
    with SqliteDict(interest_cache_path) as d:
        new_submissions = []
        for submission in submissions:
            if submission.id in d:
                res[submission.id] = d[submission.id]
            else:
                new_submissions.append(submission)

    new_interests = await asyncio.gather(*[
        get_interest(submission)
        for submission in new_submissions
    ])
    with SqliteDict(interest_cache_path) as d:
        for new_submission, new_interest in zip(new_submissions, new_interests):
            d[new_submission.id] = new_interest
            res[new_submission.id] = new_interest
        d.commit()
    return res
