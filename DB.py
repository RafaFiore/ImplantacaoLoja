import mysql.connector
from dotenv import load_dotenv
import logger
import os


class Database:
    def __init__(self):
        load_dotenv()
        self.__db_host = os.getenv("db_host")
        self.__db_user = os.getenv("db_user")
        self.__db_pass = os.getenv("db_pass")
        self.__database = os.getenv("db")

    def init_conn(self):
        log = logger.Logger()
        try:
            database = mysql.connector.connect(
                host=self.__db_host,
                user=self.__db_user,
                password=self.__db_pass,
                database=self.__database
            )
            cursor = database.cursor(buffered=True)
            return database, cursor
        except mysql.connector.Error as err:
            log.error('db_error.log', err)

    def select_rd_tickets(self, rd_ticket_id):
        log = logger.Logger()
        conn, cursor = self.init_conn()
        query = ("SELECT rd_ticket_id "
                 "FROM implantacoes "
                 "WHERE rd_ticket_id = %s")
        try:
            cursor.execute(query, (rd_ticket_id,))
            result = cursor.fetchone()
            return result
        except mysql.connector.Error as err:
            log.error('db_error.log', err)
        finally:
            cursor.close()
            conn.close()
            