
import pytest
import datetime
from src.database import insert_data
from src.models import Subreddit, Post, Comment

def test_insert_data_happy_path(db_session):
    subreddit_data = {
        'id': 't5_2qh1i',
        'name': 'python',
        'created_utc': datetime.datetime.now(datetime.timezone.utc),
        'description': 'Python programming language',
        'subscribers': 1000000
    }
    posts_data = [{
        'id': 't3_1',
        'title': 'Test Post',
        'selftext': 'This is a test post.',
        'created_utc': datetime.datetime.now(datetime.timezone.utc),
        'score': 100,
        'upvote_ratio': 0.99,
        'num_comments': 10,
        'url': 'http://test.com/post',
        'author': 'testuser',
        'subreddit_id': 't5_2qh1i'
    }]
    comments_data = [{
        'id': 't1_1',
        'body': 'This is a test comment.',
        'created_utc': datetime.datetime.now(datetime.timezone.utc),
        'score': 50,
        'author': 'testuser2',
        'post_id': 't3_1',
        'parent_id': 't3_1'
    }]

    insert_data(db_session, subreddit_data, posts_data, comments_data)
    db_session.commit()

    subreddit = db_session.query(Subreddit).filter_by(id='t5_2qh1i').first()
    assert subreddit is not None
    assert subreddit.name == 'python'

    post = db_session.query(Post).filter_by(id='t3_1').first()
    assert post is not None
    assert post.title == 'Test Post'

    comment = db_session.query(Comment).filter_by(id='t1_1').first()
    assert comment is not None
    assert comment.body == 'This is a test comment.'

def test_insert_data_idempotency(db_session):
    subreddit_data = {
        'id': 't5_2qh1i',
        'name': 'python',
        'created_utc': datetime.datetime.now(datetime.timezone.utc),
        'description': 'Python programming language',
        'subscribers': 1000000
    }
    posts_data = [{
        'id': 't3_1',
        'title': 'Test Post',
        'selftext': 'This is a test post.',
        'created_utc': datetime.datetime.now(datetime.timezone.utc),
        'score': 100,
        'upvote_ratio': 0.99,
        'num_comments': 10,
        'url': 'http://test.com/post',
        'author': 'testuser',
        'subreddit_id': 't5_2qh1i'
    }]

    # First insert
    insert_data(db_session, subreddit_data, posts_data, [])
    db_session.commit()

    # Second insert with updated data
    updated_subreddit_data = {
        'id': 't5_2qh1i',
        'name': 'python-updated',
        'created_utc': datetime.datetime.now(datetime.timezone.utc),
        'description': 'Updated description',
        'subscribers': 1200000
    }
    updated_posts_data = [{
        'id': 't3_1',
        'title': 'Test Post Updated',
        'selftext': 'This is an updated test post.',
        'created_utc': datetime.datetime.now(datetime.timezone.utc),
        'score': 150,
        'upvote_ratio': 0.98,
        'num_comments': 15,
        'url': 'http://test.com/post-updated',
        'author': 'testuser',
        'subreddit_id': 't5_2qh1i'
    }]
    insert_data(db_session, updated_subreddit_data, updated_posts_data, [])
    db_session.commit()

    subreddit_count = db_session.query(Subreddit).count()
    assert subreddit_count == 1

    post_count = db_session.query(Post).count()
    assert post_count == 1

    updated_subreddit = db_session.query(Subreddit).filter_by(id='t5_2qh1i').first()
    assert updated_subreddit.name == 'python-updated'
    assert updated_subreddit.subscribers == 1200000

    updated_post = db_session.query(Post).filter_by(id='t3_1').first()
    assert updated_post.title == 'Test Post Updated'
    assert updated_post.score == 150

def test_insert_data_empty_lists(db_session):
    insert_data(db_session, {}, [], [])
    db_session.commit()

    subreddit_count = db_session.query(Subreddit).count()
    assert subreddit_count == 0

    post_count = db_session.query(Post).count()
    assert post_count == 0

    comment_count = db_session.query(Comment).count()
    assert comment_count == 0
