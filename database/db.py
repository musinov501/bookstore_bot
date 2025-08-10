import sqlite3


class Database:
    def __init__(self, db_name: str = 'main.db'):
        self.database = db_name


    def execute(self, sql, *args, commit: bool = False, fetchone: bool = False, fetchall: bool = False):
        with sqlite3.connect(self.database) as db:
            cursor = db.cursor()
            cursor.execute(sql, args)


            result = None
            if commit:
                db.commit()

            if fetchone:
                result = cursor.fetchone()
            elif fetchall:
                result = cursor.fetchall()


        return result



    def create_table_users(self):
        sql = ''' CREATE TABLE IF NOT EXISTS users(
            telegram_id BIGINT NOT NULL UNIQUE,
            full_name VARCHAR(100),
            phone_number VARCHAR(15)
            )
            '''
        self.execute(sql, commit=True)

    def insert_telegram_id(self, telegram_id):
        sql = '''INSERT INTO users(telegram_id) VALUES (?)'''
        self.execute(sql, telegram_id, commit=True)

    def update_user(self, telegram_id, full_name,phone_number):
        sql = '''UPDATE users SET full_name = ?, phone_number = ? WHERE telegram_id = ?'''
        self.execute(sql, full_name, phone_number, telegram_id, commit=True)


    def get_user(self, telegram_id):
        sql = '''SELECT * FROM users WHERE telegram_id = ?'''
        return self.execute(sql, telegram_id, fetchone=True)



    def create_table_genres(self):
        sql = '''CREATE TABLE IF NOT EXISTS genres(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT
            )
        '''
        self.execute(sql, commit=True)

    def insert_genre(self, name):
        sql = '''INSERT INTO genres(name) VALUES (?)'''
        self.execute(sql, name, commit=True)

    def select_genres(self):
        sql = '''SELECT id, name from genres'''
        return self.execute(sql, fetchall=True)

    def update_genre(self, genre_id, new_name):
        sql = '''UPDATE genres SET name = ? WHERE id = ?'''
        self.execute(sql, new_name, genre_id, commit=True)

    def delete_genre(self, genre_id):
        sql = '''DELETE FROM genres WHERE id = ?'''
        self.execute(sql, genre_id, commit=True)


    def create_table_books(self):
        sql = '''CREATE TABLE IF NOT EXISTS books(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            genre_id INTEGER,
            name TEXT,
            author TEXT,
            description TEXT,
            date_of_release TEXT,
            cover_photo TEXT,
            FOREIGN KEY(genre_id) REFERENCES genres(id)
            )
        '''
        self.execute(sql, commit=True)

    def drop_table_books(self):
        sql = '''DROP TABLE IF EXISTS books'''
        self.execute(sql, commit=True)

    def insert_book(self, genre_id, name, author, description, date_of_release, cover_photo):
        sql = '''INSERT INTO books(genre_id, name, author, description, date_of_release, cover_photo) VALUES(?,?,?,?,?,?)'''
        self.execute(sql, genre_id, name, author, description, date_of_release, cover_photo, commit=True)



    def select_books(self):
        sql = '''SELECT id, name FROM books'''
        return self.execute(sql , fetchall=True)


    def get_book_by_id(self, book_id):
        sql = '''SELECT id, genre_id, name, author, description, date_of_release , cover_photo FROM books WHERE id = ?'''
        return self.execute(sql, book_id, fetchone=True)


    def update_book(self, book_id, name , author, description, date_of_release, cover_photo):
        sql = '''UPDATE books 
        SET name = ?, author = ?, description = ?, date_of_release = ?, cover_photo = ? WHERE id = ?'''
        self.execute(sql, name, author, description, date_of_release, cover_photo, book_id, commit=True)


    def delete_book(self, book_id):
        sql = '''DELETE FROM books WHERE id = ?'''
        self.execute(sql, book_id, commit=True)


    def genre_exists(self, name):
        sql = '''SELECT id FROM genres WHERE name = ?'''
        return self.execute(sql, name, fetchone=True) is not None


    def get_genre_id(self, name):
        sql = '''SELECT id FROM genres WHERE name = ?'''
        result = self.execute(sql, name, fetchone=True)
        return result[0] if result else None

    def select_books_by_genre(self, genre_id):
        sql = '''SELECT id, name FROM books WHERE genre_id = ?'''
        return self.execute(sql, genre_id, fetchall=True)


    def book_exists(self, name):
        sql = '''SELECT id  FROM books WHERE name = ?'''
        return self.execute(sql, name, fetchone=True) is not None


    def get_book_by_name(self, name):
        sql = '''SELECT id, name, author, description, date_of_release, cover_photo FROM books WHERE name = ?'''
        return self.execute(sql, name, fetchone = True)
