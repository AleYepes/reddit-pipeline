
import praw
import datetime
from tenacity import retry, wait_exponential, stop_after_attempt, retry_if_exception_type
from src.config import RETRY_ATTEMPTS


@retry(
    wait=wait_exponential(multiplier=1, min=4, max=60),
    stop=stop_after_attempt(RETRY_ATTEMPTS),
    retry=retry_if_exception_type(praw.exceptions.PRAWException)
)
def fetch_subreddit(reddit: praw.Reddit, subreddit_name: str):
    return reddit.subreddit(subreddit_name)


@retry(
    wait=wait_exponential(multiplier=1, min=4, max=60),
    stop=stop_after_attempt(RETRY_ATTEMPTS),
    retry=retry_if_exception_type(praw.exceptions.PRAWException)
)
def fetch_submissions_for_subreddit(subreddit, limit=100):
    return list(subreddit.hot(limit=limit))


@retry(
    wait=wait_exponential(multiplier=1, min=4, max=60),
    stop=stop_after_attempt(RETRY_ATTEMPTS),
    retry=retry_if_exception_type(praw.exceptions.PRAWException)
)
def fetch_comments_for_submission(submission):
    comments_list = []
    submission.comments.replace_more(limit=None) # Fetch all comments
    for comment in submission.comments.list():
        comments_list.append(comment)
    return comments_list
