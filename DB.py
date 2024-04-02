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

    def select_customers(self, cst_email):
        log = logger.Logger()
        conn, cursor = self.init_conn()
        query = ("SELECT rd_ticket_id "
                 "FROM implantacoes "
                 "WHERE cst_email = %s "
                 "AND status = %s")
        try:
            cursor.execute(query, (cst_email, 'pending'))
            result = cursor.fetchone()
            return result
        except mysql.connector.Error as err:
            log.error('db_error.log', err)
        finally:
            cursor.close()
            conn.close()

    def insert_ticket(self, values):
        log = logger.Logger()
        conn, cursor = self.init_conn()
        query = ("INSERT INTO implantacoes "
                 "(ticket_id, rd_ticket_id, cst_email, cst_name, rd_ticket_date, ticket_date, status) "
                 "VALUES (%s, %s, %s, %s, %s, %s, %s)")
        try:
            cursor.executemany(query, values)
        except mysql.connector.Error as err:
            log.error('db_error.log', err)
        finally:
            conn.commit()
            cursor.close()
            conn.close()

    def update_ticket(self, ticket_id):
        log = logger.Logger()
        conn, cursor = self.init_conn()
        query = ("UPDATE implantacoes "
                 "SET status = 'finished' "
                 "WHERE ticket_id = %s")
        try:
            cursor.execute(query, (ticket_id,))
        except mysql.connector.Error as err:
            log.error('db_error.log', err)
        finally:
            conn.commit()
            cursor.close()
            conn.close()
