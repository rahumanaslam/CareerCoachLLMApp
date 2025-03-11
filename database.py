import sqlite3
import hashlib

class DatabaseUtils:
    def __init__(self):
        self.conn = sqlite3.connect('career_coach.db')
        self.c = self.conn.cursor()
        self.c.execute('''
            CREATE TABLE IF NOT EXISTS users
            (id INTEGER PRIMARY KEY,
            username TEXT UNIQUE,
            password TEXT,
            email TEXT UNIQUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)
        ''')
        self.conn.commit()
        self.conn.close()
    
    def hash_password(self, password):
        return hashlib.sha256(
            password.encode()
        ).hexdigest()
    
    def authenticate(self, username, password):
        self.conn = sqlite3.connect('career_coach.db')
        self.c = self.conn.cursor()
        self.c.execute(
        "SELECT * FROM users WHERE username=? AND password=?",
        (username, self.hash_password(password))
        )
        self.user = self.c.fetchone()
        self.conn.close()
        return self.user is not None
    
    def create_user(self, username, password, email):
        try:
            self.conn = sqlite3.connect('career_coach.db')
            self.c = self.conn.cursor()
            self.c.execute(
                "INSERT INTO users (username, password, email) VALUES (?, ?, ?)",
                (username, self.hash_password(password), email)
            )
            self.conn.commit()
            self.conn.close()
            return True
        except sqlite3.IntegrityError:
            return False