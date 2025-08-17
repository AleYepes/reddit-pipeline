from sqlalchemy import create_engine, Column, String, TEXT, TIMESTAMP, INTEGER, REAL, ForeignKey, BOOLEAN, func
from sqlalchemy.orm import declarative_base, relationship


Base = declarative_base()

class Subreddit(Base):
    __tablename__ = 'subreddits'

    name = Column(String(12), primary_key=True)
    display_name = Column(String(21), nullable=False, unique=True)
    created_utc = Column(TIMESTAMP(timezone=True), nullable=False)
    description = Column(TEXT)
    subscribers = Column(INTEGER)
    fetched_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    over_18 = Column(BOOLEAN)

    submissions = relationship("Submission", back_populates="subreddit")

class Submission(Base):
    __tablename__ = 'submissions'

    name = Column(String(12), primary_key=True)
    title = Column(String(300), nullable=False)
    selftext = Column(TEXT)
    created_utc = Column(TIMESTAMP(timezone=True), nullable=False)
    score = Column(INTEGER, nullable=False)
    upvote_ratio = Column(REAL)
    num_comments = Column(INTEGER, nullable=False)
    url = Column(TEXT)
    author = Column(String(20))
    subreddit_name = Column(String(12), ForeignKey('subreddits.name'), nullable=False)
    fetched_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    locked = Column(BOOLEAN)
    over_18 = Column(BOOLEAN)
    flair_text = Column(String(64))

    subreddit = relationship("Subreddit", back_populates="submissions")
    comments = relationship("Comment", back_populates="submission")


class Comment(Base):
    __tablename__ = 'comments'

    name = Column(String(12), primary_key=True)
    body = Column(TEXT, nullable=False)
    created_utc = Column(TIMESTAMP(timezone=True), nullable=False)
    score = Column(INTEGER, nullable=False)
    author = Column(String(20))
    submission_name = Column(String(12), ForeignKey('submissions.name'), nullable=False)
    parent_name = Column(String(12))

    submission = relationship("Submission", back_populates="comments")
