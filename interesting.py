import os
from functools import lru_cache
from typing import Dict, List
from urllib.parse import urljoin

import requests
from praw.models import Submission

from prawutils import get_reddit

reddit = get_reddit()
interest_cache_path = 'cached_interest.sqlite'

HF_INFERENCE_URL = os.getenv('HF_INFERENCE_URL', 'http://vpn.tchen.xyz:33960/')


@lru_cache(maxsize=1000000)
def get_interest(submission: Submission) -> float:
    body = f'''Title: {submission.title}
    Subreddit: {submission.subreddit.display_name}
    {submission.selftext}'''
    if len(submission.selftext) > 0 and submission.num_comments > 0:
        for i in range(min(len(submission.comments), 10)):
            body += f'\n{submission.comments[i].body}'
    url = urljoin(HF_INFERENCE_URL, 'gpt2loss')
    return float(requests.post(url, json=body[:1000]).json()['loss'])


def get_interests(submissions: List[Submission]) -> Dict[str, float]:
    return {
        submission.id: get_interest(submission)
        for submission in submissions
    }
