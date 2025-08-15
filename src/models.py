
import datetime
from sqlalchemy import create_engine, Column, String, TEXT, TIMESTAMPTZ, INTEGER, REAL, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Subreddit(Base):
    __tablename__ = 'subreddits'

    id = Column(String(10), primary_key=True)
    name = Column(String(255), nullable=False, unique=True)
    created_utc = Column(TIMESTAMPTZ, nullable=False)
    description = Column(TEXT)
    subscribers = Column(INTEGER)
    fetched_at = Column(TIMESTAMPTZ, nullable=False, default=datetime.datetime.utcnow)

    posts = relationship("Post", back_populates="subreddit")

class Post(Base):
    __tablename__ = 'posts'

    id = Column(String(10), primary_key=True)
    title = Column(TEXT, nullable=False)
    selftext = Column(TEXT)
    created_utc = Column(TIMESTAMPTZ, nullable=False)
    score = Column(INTEGER, nullable=False)
    upvote_ratio = Column(REAL)
    num_comments = Column(INTEGER, nullable=False)
    url = Column(TEXT)
    author = Column(String(255))
    subreddit_id = Column(String(10), ForeignKey('subreddits.id'), nullable=False)
    fetched_at = Column(TIMESTAMPTZ, nullable=False, default=datetime.datetime.utcnow)

    subreddit = relationship("Subreddit", back_populates="posts")
    comments = relationship("Comment", back_populates="post")


class Comment(Base):
    __tablename__ = 'comments'

    id = Column(String(10), primary_key=True)
    body = Column(TEXT, nullable=False)
    created_utc = Column(TIMESTAMPTZ, nullable=False)
    score = Column(INTEGER, nullable=False)
    author = Column(String(255))
    post_id = Column(String(10), ForeignKey('posts.id'), nullable=False)
    parent_id = Column(String(20))
    fetched_at = Column(TIMESTAMPTZ, nullable=False, default=datetime.datetime.utcnow)

    post = relationship("Post", back_populates="comments")
