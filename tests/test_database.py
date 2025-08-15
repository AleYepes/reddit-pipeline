from sqlalchemy.inspection import inspect

def test_db_init(db_session):
    inspector = inspect(db_session.bind)
    assert inspector.has_table("subreddits")
    assert inspector.has_table("posts")
    assert inspector.has_table("comments")
