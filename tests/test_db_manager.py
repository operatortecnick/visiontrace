import pytest
import sqlite3
from database import db_manager


@pytest.fixture
def conn():
    connection = sqlite3.connect(":memory:")
    db_manager.initialize_db(connection)
    yield connection
    connection.close()


def test_insert_and_fetch_log(conn):
    db_manager.insert_log(conn, "Test log entry")
    logs = db_manager.fetch_logs(conn, limit=1, offset=0)
    assert len(logs) == 1
    assert "Test log entry" in logs[0][1]


def test_count_logs(conn):
    db_manager.insert_log(conn, "Log 1")
    db_manager.insert_log(conn, "Log 2")
    count = db_manager.count_logs(conn)
    assert count == 2
