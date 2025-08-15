
import pytest
import datetime
from unittest.mock import MagicMock
from src.main import transform_praw_objects, main

@pytest.fixture
def mock_praw_objects():
    subreddit = MagicMock()
    subreddit.id = 't5_2qh1i'
    subreddit.display_name = 'python'
    subreddit.created_utc = 1234567890
    subreddit.public_description = 'Python programming language'
    subreddit.subscribers = 1000000

    post = MagicMock()
    post.id = 't3_1'
    post.title = 'Test Post'
    post.selftext = 'This is a test post.'
    post.created_utc = 1234567890
    post.score = 100
    post.upvote_ratio = 0.99
    post.num_comments = 10
    post.url = 'http://test.com/post'
    post.author = MagicMock()
    post.author.name = 'testuser'
    post.submission.id = 't3_1'

    comment = MagicMock()
    comment.id = 't1_1'
    comment.body = 'This is a test comment.'
    comment.created_utc = 1234567890
    comment.score = 50
    comment.author = MagicMock()
    comment.author.name = 'testuser2'
    comment.submission.id = 't3_1'
    comment.parent_id = 't3_1'

    return subreddit, [post], [comment]

def test_transform_praw_objects(mock_praw_objects):
    subreddit, posts, comments = mock_praw_objects
    subreddit_data, posts_data, comments_data = transform_praw_objects(subreddit, posts, comments)

    assert subreddit_data['id'] == 't5_2qh1i'
    assert posts_data[0]['id'] == 't3_1'
    assert comments_data[0]['id'] == 't1_1'
    assert posts_data[0]['author'] == 'testuser'

def test_transform_praw_objects_deleted_author(mock_praw_objects):
    subreddit, posts, comments = mock_praw_objects
    posts[0].author = None
    comments[0].author = None

    _, posts_data, comments_data = transform_praw_objects(subreddit, posts, comments)

    assert posts_data[0]['author'] == '[deleted]'
    assert comments_data[0]['author'] == '[deleted]'

def test_main(mocker, mock_praw_objects):
    mock_init_db = mocker.patch('src.main.init_db')
    mock_session_local = mocker.patch('src.main.SessionLocal')
    mock_scraper = mocker.patch('src.main.scraper')
    mock_insert_data = mocker.patch('src.main.insert_data')

    subreddit, posts, comments = mock_praw_objects
    mock_scraper.fetch_subreddit.return_value = subreddit
    mock_scraper.fetch_posts_for_subreddit.return_value = posts
    mock_scraper.fetch_comments_for_post.return_value = comments

    main()

    mock_init_db.assert_called_once()
    mock_session_local.assert_called_once()
    mock_scraper.fetch_subreddit.assert_called()
    mock_scraper.fetch_posts_for_subreddit.assert_called()
    mock_scraper.fetch_comments_for_post.assert_called()
    mock_insert_data.assert_called()
