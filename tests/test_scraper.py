
import pytest
import praw
import tenacity
from src import scraper

@pytest.fixture
def mock_reddit(mocker):
    return mocker.patch('src.scraper.reddit')

def test_fetch_subreddit(mock_reddit):
    subreddit = scraper.fetch_subreddit('python')
    mock_reddit.subreddit.assert_called_once_with('python')
    assert subreddit == mock_reddit.subreddit.return_value

def test_fetch_subreddit_not_found(mock_reddit):
    mock_reddit.subreddit.side_effect = praw.exceptions.PRAWException
    with pytest.raises(tenacity.RetryError):
        scraper.fetch_subreddit('non_existent_subreddit')

def test_fetch_posts_for_subreddit(mocker, mock_reddit):
    mock_subreddit = mock_reddit.subreddit.return_value
    mock_posts = [mocker.Mock(), mocker.Mock()]
    mock_subreddit.hot.return_value = mock_posts
    posts = scraper.fetch_posts_for_subreddit(mock_subreddit, limit=2)
    mock_subreddit.hot.assert_called_once_with(limit=2)
    assert posts == mock_posts

def test_fetch_comments_for_post(mocker):
    mock_post = mocker.Mock()
    mock_comments = [mocker.Mock(), mocker.Mock()]
    mock_post.comments.list.return_value = mock_comments
    comments = scraper.fetch_comments_for_post(mock_post)
    mock_post.comments.replace_more.assert_called_once_with(limit=None)
    assert comments == mock_comments

def test_fetch_comments_for_post_no_comments(mocker):
    mock_post = mocker.Mock()
    mock_post.comments.list.return_value = []
    comments = scraper.fetch_comments_for_post(mock_post)
    assert comments == []
