import json
import sqlite3
from typing import Any, Dict, List, Optional

from app.services.config import DATABASE_PATH


def get_connection():
    connection = sqlite3.connect(
        DATABASE_PATH,
        check_same_thread=False
    )

    connection.row_factory = sqlite3.Row

    return connection


def init_db():
    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS recommendations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            planner_type TEXT NOT NULL,
            input_data TEXT NOT NULL,
            result_data TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
        """
    )

    connection.commit()
    connection.close()


def create_user(
    username: str,
    email: str,
    password_hash: str
) -> int:

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO users
        (username, email, password_hash)
        VALUES (?, ?, ?)
        """,
        (
            username,
            email.lower().strip(),
            password_hash
        )
    )

    connection.commit()

    user_id = cursor.lastrowid

    connection.close()

    return user_id


def get_user_by_email(email: str) -> Optional[Dict[str, Any]]:

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT *
        FROM users
        WHERE email = ?
        """,
        (email.lower().strip(),)
    )

    row = cursor.fetchone()

    connection.close()

    if row is None:
        return None

    return dict(row)


def get_user_by_id(user_id: int) -> Optional[Dict[str, Any]]:

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT *
        FROM users
        WHERE id = ?
        """,
        (user_id,)
    )

    row = cursor.fetchone()

    connection.close()

    if row is None:
        return None

    return dict(row)


def save_recommendation(
    user_id: int,
    planner_type: str,
    input_data: Dict[str, Any],
    result_data: Dict[str, Any]
) -> int:

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO recommendations
        (
            user_id,
            planner_type,
            input_data,
            result_data
        )
        VALUES (?, ?, ?, ?)
        """,
        (
            user_id,
            planner_type,
            json.dumps(input_data),
            json.dumps(result_data)
        )
    )

    connection.commit()

    recommendation_id = cursor.lastrowid

    connection.close()

    return recommendation_id


def get_user_recommendations(
    user_id: int
) -> List[Dict[str, Any]]:

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT *
        FROM recommendations
        WHERE user_id = ?
        ORDER BY created_at DESC
        """,
        (user_id,)
    )

    rows = cursor.fetchall()

    connection.close()

    results = []

    for row in rows:

        item = dict(row)

        try:
            item["input_data"] = json.loads(
                item["input_data"]
            )
        except Exception:
            item["input_data"] = {}

        try:
            item["result_data"] = json.loads(
                item["result_data"]
            )
        except Exception:
            item["result_data"] = {}

        results.append(item)

    return results


def get_recommendation(
    recommendation_id: int,
    user_id: int
) -> Optional[Dict[str, Any]]:

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT *
        FROM recommendations
        WHERE id = ?
        AND user_id = ?
        """,
        (
            recommendation_id,
            user_id
        )
    )

    row = cursor.fetchone()

    connection.close()

    if row is None:
        return None

    result = dict(row)

    try:
        result["input_data"] = json.loads(
            result["input_data"]
        )
    except Exception:
        result["input_data"] = {}

    try:
        result["result_data"] = json.loads(
            result["result_data"]
        )
    except Exception:
        result["result_data"] = {}

    return result