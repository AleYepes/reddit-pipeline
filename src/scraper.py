
import praw
import datetime
from tenacity import retry, wait_exponential, stop_after_attempt, retry_if_exception_type

# Initialize PRAW
# It will automatically look for a praw.ini file in the current directory
reddit = praw.Reddit('bot1')

@retry(
    wait=wait_exponential(multiplier=1, min=4, max=60),
    stop=stop_after_attempt(5),
    retry=retry_if_exception_type(praw.exceptions.PRAWException)
)
def fetch_subreddit(subreddit_name: str):
    """Fetches a subreddit object."""
    return reddit.subreddit(subreddit_name)

@retry(
    wait=wait_exponential(multiplier=1, min=4, max=60),
    stop=stop_after_attempt(5),
    retry=retry_if_exception_type(praw.exceptions.PRAWException)
)
def fetch_posts_for_subreddit(subreddit, limit=100):
    """Fetches the latest 'hot' posts for a given subreddit object."""
    return list(subreddit.hot(limit=limit))

@retry(
    wait=wait_exponential(multiplier=1, min=4, max=60),
    stop=stop_after_attempt(5),
    retry=retry_if_exception_type(praw.exceptions.PRAWException)
)
def fetch_comments_for_post(post):
    """
    Fetches all comments for a given post, linearizing the comment tree.
    """
    comments_list = []
    post.comments.replace_more(limit=None) # Fetch all comments
    for comment in post.comments.list():
        comments_list.append(comment)
    return comments_list
