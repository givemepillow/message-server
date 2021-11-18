import envfileparser
import psycopg2
from psycopg2 import Error


class Connection:
    __connection = None

    def __init__(self):
        envs = envfileparser.get_env_from_file()
        try:
            self.__connection = psycopg2.connect(
                user=envs['DB_USER'],
                password=envs['DB_PASSWORD'],
                host=envs['DB_HOST'],
                port=envs['DB_PORT'],
                database=envs['DB_NAME']
            )
        except (Exception, Error) as error:
            print("Ошибка при работе с PostgreSQL", error)

    def get_connection(self):
        return self.__connection


class Storage:

    def __init__(self):
        self.__connection = Connection().get_connection()

    def save_message(self, from_id, to_id, date_time, message):
        cursor = self.__connection.cursor()
        cursor.execute("INSERT INTO messages(id_from, id_to, date_time, message)"
                       "VALUES (%s, %s, %s, %s)", (from_id, to_id, date_time, message))
        self.__connection.commit()
