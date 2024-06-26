import sqlite3
import os

def init_db():
    db_path = 'database.db'

    # Delete the existing database file if it exists
    if os.path.exists(db_path):
        os.remove(db_path)
        print(f"Deleted existing database file: {db_path}")

    db = sqlite3.connect(db_path)
    
    try:
        # Create users table
        db.execute('''
            CREATE TABLE users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                password TEXT NOT NULL
            )
        ''')
        
        # Create lists table
        db.execute('''
            CREATE TABLE lists (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                user_id INTEGER NOT NULL,
                is_public INTEGER NOT NULL CHECK(is_public IN (0, 1)),
                FOREIGN KEY(user_id) REFERENCES users(id)
            )
        ''')
        
        # Create list_movies table
        db.execute('''
            CREATE TABLE list_movies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                list_id INTEGER NOT NULL,
                movie_id TEXT NOT NULL,
                FOREIGN KEY(list_id) REFERENCES lists(id)
            )
        ''')
        
        # Create movies table
        db.execute('''
            CREATE TABLE IF NOT EXISTS movies (
                id INTEGER PRIMARY KEY,
                title TEXT NOT NULL,
                year INTEGER,
                poster TEXT
            )
        ''')

        db.commit()
        print("Database initialized successfully.")
    except sqlite3.DatabaseError as e:
        print(f"Database error: {e}")
    finally:
        db.close()

if __name__ == '__main__':
    init_db()
