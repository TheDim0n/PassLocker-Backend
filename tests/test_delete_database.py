import os


def test_delete_database():
    os.remove("sql_app.db")
    assert not os.path.exists("sql_app.db")
