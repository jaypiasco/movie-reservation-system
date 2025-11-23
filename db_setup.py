from __future__ import annotations

import argparse
import os
import sys
from typing import Optional

try:
    import psycopg2
    from psycopg2 import sql
except ImportError:
    print("Missing dependency: psycopg2. Install with: pip install psycopg2-binary")
    sys.exit(1)


CREATE_TABLES_SQL = [
    # Users
    """
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        username VARCHAR(150) UNIQUE NOT NULL,
        password_hash VARCHAR(255),
        email VARCHAR(255),
        created_at TIMESTAMP WITH TIME ZONE DEFAULT now()
    );
    """,

    # Movies
    """
    CREATE TABLE IF NOT EXISTS movies (
        id SERIAL PRIMARY KEY,
        title VARCHAR(255) NOT NULL,
        duration_minutes INTEGER,
        description TEXT
    );
    """,

    # Cinemas
    """
    CREATE TABLE IF NOT EXISTS cinemas (
        id SERIAL PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        location VARCHAR(255)
    );
    """,

    # Seats - seat definitions per cinema (e.g., row, number)
    """
    CREATE TABLE IF NOT EXISTS seats (
        id SERIAL PRIMARY KEY,
        cinema_id INTEGER NOT NULL REFERENCES cinemas(id) ON DELETE CASCADE,
        seat_label VARCHAR(32) NOT NULL,
        row_number INTEGER,
        col_number INTEGER,
        UNIQUE(cinema_id, seat_label)
    );
    """,

    # Schedules (showings)
    """
    CREATE TABLE IF NOT EXISTS schedules (
        id SERIAL PRIMARY KEY,
        movie_id INTEGER NOT NULL REFERENCES movies(id) ON DELETE CASCADE,
        cinema_id INTEGER NOT NULL REFERENCES cinemas(id) ON DELETE CASCADE,
        start_time TIMESTAMP WITH TIME ZONE NOT NULL,
        created_at TIMESTAMP WITH TIME ZONE DEFAULT now()
    );
    """,

    # Seat availability per schedule (status: available, held, reserved)
    """
    CREATE TABLE IF NOT EXISTS schedule_seats (
        id SERIAL PRIMARY KEY,
        schedule_id INTEGER NOT NULL REFERENCES schedules(id) ON DELETE CASCADE,
        seat_id INTEGER NOT NULL REFERENCES seats(id) ON DELETE CASCADE,
        status VARCHAR(16) NOT NULL DEFAULT 'available',
        hold_until TIMESTAMP WITH TIME ZONE,
        UNIQUE(schedule_id, seat_id)
    );
    """,

    # Reservations
    """
    CREATE TABLE IF NOT EXISTS reservations (
        id SERIAL PRIMARY KEY,
        user_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
        schedule_id INTEGER NOT NULL REFERENCES schedules(id) ON DELETE CASCADE,
        status VARCHAR(16) NOT NULL DEFAULT 'pending',
        total_amount NUMERIC(10,2) DEFAULT 0,
        created_at TIMESTAMP WITH TIME ZONE DEFAULT now()
    );
    """,

    # Reservation seats (many-to-many)
    """
    CREATE TABLE IF NOT EXISTS reservation_seats (
        reservation_id INTEGER NOT NULL REFERENCES reservations(id) ON DELETE CASCADE,
        schedule_seat_id INTEGER NOT NULL REFERENCES schedule_seats(id) ON DELETE CASCADE,
        price NUMERIC(10,2) DEFAULT 0,
        PRIMARY KEY (reservation_id, schedule_seat_id)
    );
    """,

    # Payments
    """
    CREATE TABLE IF NOT EXISTS payments (
        id SERIAL PRIMARY KEY,
        reservation_id INTEGER NOT NULL REFERENCES reservations(id) ON DELETE CASCADE,
        method VARCHAR(32) NOT NULL,
        amount NUMERIC(10,2) NOT NULL,
        status VARCHAR(32) NOT NULL,
        transaction_ref VARCHAR(255),
        created_at TIMESTAMP WITH TIME ZONE DEFAULT now()
    );
    """,
]


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Create DB tables for movie reservation app")
    p.add_argument("--host", default=os.environ.get("DB_HOST", "localhost"))
    p.add_argument("--port", default=int(os.environ.get("DB_PORT", "5435")), type=int)
    p.add_argument("--dbname", default=os.environ.get("DB_NAME", "postgres"))
    p.add_argument("--user", default=os.environ.get("DB_USER", "postgres"))
    p.add_argument("--password", default=os.environ.get("DB_PASSWORD", "postgres"))
    return p.parse_args()


def create_tables(conn) -> None:
    with conn.cursor() as cur:
        for stmt in CREATE_TABLES_SQL:
            cur.execute(stmt)
        conn.commit()


def main(host: str, port: int, dbname: str, user: str, password: Optional[str]) -> int:
    conn = None
    try:
        print(f"Connecting to {user}@{host}:{port}/{dbname} ...")
        conn = psycopg2.connect(host=host, port=port, dbname=dbname, user=user, password=password)
        print("Connected. Creating tables...")
        create_tables(conn)
        print("Tables created successfully.")
        return 0
    except Exception as e:
        print("Error during DB setup:", str(e))
        return 2
    finally:
        if conn:
            conn.close()


if __name__ == "__main__":
    args = parse_args()
    rc = main(args.host, args.port, args.dbname, args.user, args.password)
    sys.exit(rc)
