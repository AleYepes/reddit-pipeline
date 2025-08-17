import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects.postgresql import insert
from src.models import Base, Subreddit, Submission, Comment
from src.config import DATABASE_URL


engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db(engine=engine):
    Base.metadata.create_all(bind=engine)

def insert_data(session, subreddit_data, submissions_data, comments_data):
    # Upsert Subreddit
    if not subreddit_data:
        return
    subreddit_stmt = insert(Subreddit).values(**subreddit_data)
    subreddit_update_stmt = subreddit_stmt.on_conflict_do_update(
        index_elements=['name'],
        set_={
            'display_name': subreddit_stmt.excluded.display_name,
            'description': subreddit_stmt.excluded.description,
            'subscribers': subreddit_stmt.excluded.subscribers,
            'over_18': subreddit_stmt.excluded.over18,
            'fetched_at': datetime.datetime.now(datetime.timezone.utc)
        }
    )
    session.execute(subreddit_update_stmt)

    # Upsert Submissions
    if not submissions_data:
        return
    submissions_stmt = insert(Submission).values(submissions_data)
    submissions_update_stmt = submissions_stmt.on_conflict_do_update(
        index_elements=['name'],
        set_={
            'title': submissions_stmt.excluded.title,
            'selftext': submissions_stmt.excluded.selftext,
            'score': submissions_stmt.excluded.score,
            'upvote_ratio': submissions_stmt.excluded.upvote_ratio,
            'num_comments': submissions_stmt.excluded.num_comments,
            'locked': submissions_stmt.excluded.locked,
            'over_18': submissions_stmt.excluded.over_18,
            'flair_text': submissions_stmt.excluded.flair_text,
            'fetched_at': datetime.datetime.now(datetime.timezone.utc)
        }
    )
    session.execute(submissions_update_stmt)

    # Upsert Comments
    if not comments_data:
        return
    comments_stmt = insert(Comment).values(comments_data)
    comments_update_stmt = comments_stmt.on_conflict_do_update(
        index_elements=['name'],
        set_={
            'body': comments_stmt.excluded.body,
            'score': comments_stmt.excluded.score,
        }
    )
    session.execute(comments_update_stmt)

def get_db_session():
    return SessionLocal()