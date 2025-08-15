
import pytest
import sys
sys.path.append('.')
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.models import Base
from src.database import init_db


@pytest.fixture(scope="session")
def db_engine():
    """yields a SQLAlchemy engine which is suppressed after the test session"""
    engine_ = create_engine("sqlite:///:memory:")
    init_db(engine_)
    yield engine_
    engine_.dispose()


@pytest.fixture(scope="function")
def db_session(db_engine):
    """yields a SQLAlchemy session which is rollbacked after the test"""
    connection = db_engine.connect()
    # begin a non-ORM transaction
    trans = connection.begin()

    # bind an individual Session to the connection
    Session = sessionmaker(bind=connection)
    session = Session()

    yield session

    session.close()
    # rollback - everything that happened with the
    # session above (including calls to commit()) is rolled back.
    trans.rollback()
    connection.close()
