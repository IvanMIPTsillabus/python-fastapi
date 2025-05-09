import contextlib
import os
import sqlite3


class Database:
    def __init__(self, db_path, schema_path):
        self.__connection = None
        self.__cursor = None
        self.__db_path = db_path
        self.__schema_path = schema_path

    def create(self,):
        try:
            is_it_new = os.path.exists(self.__db_path)
            self.__connection = sqlite3.connect(self.__db_path)
            self.__cursor = self.__connection.cursor()

            if not is_it_new:
                with open(self.__schema_path, "r") as db_schema:
                    structure = db_schema.read()
                    queries = structure.split(";")
                    for query in queries:
                        query = query.strip()
                        if query:
                            self.__cursor.execute(query)
                    self.__connection.commit()

        except sqlite3.Error as e:
            print(f"Ошибка при подключении к базе данных: {e}")

    def close_connection(self):
        if self.__connection:
            self.__connection.close()

    def add_user(self, login: str, password: str, name: str):
        try:
            sql = "INSERT INTO users (username, password, email) VALUES (?, ?, ?)"
            self.__cursor.execute(sql, (login, password, name))
            self.__connection.commit()
            return True, self.__cursor.lastrowid
        except sqlite3.Error as e:
            print(f"Произошла ошибка при добавлении нового пользователя в базу данных. Подробнее: {e}")
            return False, None

    def get_user_info(self, user_id: str) -> list | None:
        try:
            sql = "SELECT username, password, email FROM users WHERE user_id = ?"
            self.__cursor.execute(sql, (user_id,))
            results = self.__cursor.fetchone()
            return results
        except sqlite3.Error as e:
            print(f"Произошла ошибка при получении информации пользователя из базы данных. Подробнее: {e}")
            return None

    def update_user_password(self, user_id, new_password):
        try:
            sql = "UPDATE users SET password = ? WHERE user_id = ?"
            self.__cursor.execute(sql, (new_password, user_id,))
            self.__connection.commit()
            return True
        except sqlite3.Error as e:
            print(f"Произошла ошибка при смене пароля пользователя в базе данных. Подробнее: {e}")
            return False

    def delete_user(self, user_id):
        try:
            sql = "DELETE FROM users WHERE user_id = ?"
            self.__cursor.execute(sql, (user_id,))
            self.__connection.commit()
            return True
        except sqlite3.Error as e:
            print(f"Произошла ошибка при удалении пользователя из базы данных. Подробнее: {e}")
            return False

    def get_user_id(self, login: str):
        try:
            sql = "SELECT user_id FROM users WHERE username = ?"
            self.__cursor.execute(sql, (login,))
            results = self.__cursor.fetchone()
            if results:
                return True, results[0]
            else:
                return False, None
        except sqlite3.Error as e:
            print(f"Произошла ошибка при поиске логина в базе данных. Подробнее: {e}")
            return None

    def add_user_result(self, user_id, data, computed_at):
        try:
            sql = "INSERT INTO results (user_id, data, computed_at) VALUES (?, ?, ?)"
            self.__cursor.execute(sql, (user_id, data, computed_at))
            self.__connection.commit()
            return True
        except sqlite3.Error as e:
            print(f"Произошла ошибка при добавлении логов пользователя в базу данных. Подробнее: {e}")
            return False

    def get_user_results(self, user_id):
        try:
            sql = "SELECT data, computed_at FROM results WHERE user_id = ?"
            self.__cursor.execute(sql, (user_id,))
            results = self.__cursor.fetchall()
            if results:
                return results
        except sqlite3.Error as e:
            print(f"Произошла ошибка при поиске логина в базе данных. Подробнее: {e}")
        return None

    def delete_user_result(self, user_id):
        try:
            sql = "DELETE FROM results WHERE user_id = ?"
            self.__cursor.execute(sql, (user_id,))
            self.__connection.commit()
            return True
        except sqlite3.Error as e:
            print(f"Произошла ошибка при удалении пользователя из базы данных. Подробнее: {e}")
            return False

    def add_user_auth_log(self, user_id, auth_at):
        try:
            sql = "INSERT INTO auth_logs (user_id, auth_at) VALUES (?, ?)"
            self.__cursor.execute(sql, (user_id, auth_at))
            self.__connection.commit()
            return True
        except sqlite3.Error as e:
            print(f"Произошла ошибка при добавлении логов пользователя в базу данных. Подробнее: {e}")
            return False

    def get_user_auth_logs(self, user_id) -> list | None:
        try:
            sql = "SELECT auth_at FROM auth_logs WHERE user_id = ?"
            self.__cursor.execute(sql, (user_id,))
            results = self.__cursor.fetchall()
            return results
        except sqlite3.Error as e:
            print(f"Произошла ошибка при получении логов входа пользователя из базы данных. Подробнее: {e}")
            return None

    @contextlib.contextmanager
    def get_session(self):
        try:
            yield self
        finally:
            self.close_connection()
