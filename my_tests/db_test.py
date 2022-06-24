from setup.db import get_db_cursor
from setup.logger import CustomLogger


logger = CustomLogger.get_logger('bot')


def sql_test():
    sql_update = """SELECT * 
                    FROM customers
                                     """
    with get_db_cursor() as cur:
        try:
            cur.execute(sql_update)
            logger.info('Result %s', cur.fetchone())
        except Exception:
            logger.exception('DB ERROR')


if __name__ == '__main__':
    sql_test()