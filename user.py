import json
import sqlite3

class User:
    def __init__(self, username : str, user_id : int, firstname : str, lastname : str):
        self.username = username
        self.user_id = user_id
        self.firstname = firstname
        self.lastname = lastname
        self.filenames = []

    def get_user_id(self, username, firstname, lastname):
        if self.username == username and self.firstname == firstname and self.lastname == lastname:
            return self.user_id
        else:
            return None

    def get_username(self, user_id):
        if self.user_id == user_id:
            return self.username
        else:
            return None

    def get_firstname(self, user_id):
        if self.user_id == user_id:
            return self.firstname
        else:
            return None

    def get_lastname(self, user_id):
        if self.user_id == user_id:
            return self.lastname
        else:
            return None

    def to_json(self):    
        data = {
            'username': self.username,
            'user_id': self.user_id,
            'firstname': self.firstname,
            'lastname': self.lastname,
            'filenames': self.filenames
        }
        json_data = json.dumps(data, default=str, indent=4)
        
        try:
            with open(f'user_info/{self.user_id}_bereal.JSON', 'w') as file:
                file.write(json_data)
        except Exception as e:
            print(f"An error occurred while writing to the file: user_info/{self.user_id}_bereal.JSON")

class UserDatabase:
    def __init__(self, db_name : str):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                username TEXT NOT NULL,
                user_id INTEGER PRIMARY KEY,
                firstname TEXT NOT NULL,
                lastname TEXT NOT NULL
            )
        ''')
        self.conn.commit()

    def insert_user(self, username : str, user_id : int, firstname : str, lastname : str):
        self.cursor.execute('''
            INSERT INTO users (username, user_id, firstname, lastname) 
            VALUES (?, ?, ?, ?)
        ''', (username, user_id, firstname, lastname))
        self.conn.commit()

    def delete_user(self, user_id : int):
        self.cursor.execute('''
        DELETE FROM users 
        WHERE user_id = ?
        ''', (user_id,))
        self.conn.commit()
    
    def user_id_exists(self, user_id : int):
        self.cursor.execute('''
            SELECT 1 FROM users 
            WHERE user_id = ?
        ''', (user_id,))
        return self.cursor.fetchone() is not None

    def get_all_user_ids(self):
        self.cursor.execute('''
            SELECT user_id FROM users
        ''')
        result = self.cursor.fetchall()
        return [row[0] for row in result]

    def close(self):
        self.conn.close()