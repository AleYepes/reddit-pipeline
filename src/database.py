
import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects.postgresql import insert
from src.models import Base, Subreddit, Post, Comment
from src.config import DATABASE_URL

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    """Initializes the database and creates tables."""
    Base.metadata.create_all(bind=engine)

def insert_data(session, subreddit_data, posts_data, comments_data):
    """
    Inserts subreddit, posts, and comments data into the database idempotently.
    Uses ON CONFLICT DO UPDATE to handle existing records.
    """
    if not subreddit_data:
        return

    # Upsert Subreddit
    subreddit_stmt = insert(Subreddit).values(**subreddit_data)
    subreddit_update_stmt = subreddit_stmt.on_conflict_do_update(
        index_elements=['id'],
        set_={
            'name': subreddit_stmt.excluded.name,
            'description': subreddit_stmt.excluded.description,
            'subscribers': subreddit_stmt.excluded.subscribers,
            'fetched_at': datetime.datetime.utcnow()
        }
    )
    session.execute(subreddit_update_stmt)

    if not posts_data:
        return

    # Upsert Posts
    posts_stmt = insert(Post).values(posts_data)
    posts_update_stmt = posts_stmt.on_conflict_do_update(
        index_elements=['id'],
        set_={
            'title': posts_stmt.excluded.title,
            'selftext': posts_stmt.excluded.selftext,
            'score': posts_stmt.excluded.score,
            'upvote_ratio': posts_stmt.excluded.upvote_ratio,
            'num_comments': posts_stmt.excluded.num_comments,
            'fetched_at': datetime.datetime.utcnow()
        }
    )
    session.execute(posts_update_stmt)

    if not comments_data:
        return

    # Upsert Comments
    comments_stmt = insert(Comment).values(comments_data)
    comments_update_stmt = comments_stmt.on_conflict_do_update(
        index_elements=['id'],
        set_={
            'body': comments_stmt.excluded.body,
            'score': comments_stmt.excluded.score,
            'fetched_at': datetime.datetime.utcnow()
        }
    )
    session.execute(comments_update_stmt)
