import pymysql
from douban_web_app.spiders import spider_settings
import logging


class MysqlDbControllerCls:

    def __init__(self):
        mysql_info = spider_settings.SERVER_MYSQL_INFO
        self.devices_table_name = mysql_info["table_name"]
        self.db = pymysql.connect(
            host=mysql_info["host"],
            port=mysql_info["port"],
            user=mysql_info["user"],
            passwd=mysql_info["password"],
            db=mysql_info["db_name"]
        )

        self.cursor = self.db.cursor()

    def insert_data_list(self, data_list):
        try:
            self.cursor.executemany(
                "insert into douban_data (book_id,page_cursor,book_link,book_title,book_info,book_img_link,book_rating,book_comments,create_time)"
                " values(%s,%s, %s,%s,%s,%s,%s,%s, %s)",
                data_list)
        except Exception as e:
            logging.error(msg="数据存储错误:" + str(e) + str(e.__traceback__.tb_lineno) + e.__traceback__.tb_frame.f_globals["__file__"])
        finally:
            self.cursor.close()
            self.db.commit()
            self.db.close()

    def get_today_top_book_data(self, page, date):
        try:
            print("select * from douban_data where page_cursor=%s and to_days(create_time) = to_days(now())"%(page))
            self.cursor.execute("select * from douban_data where page_cursor=%s and to_days(create_time) = to_days(now())"%(page))
            book_data = self.cursor.fetchall()
            return book_data
        except Exception as e:
            logging.error(msg="数据读取错误:" + str(e) + str(e.__traceback__.tb_lineno) + e.__traceback__.tb_frame.f_globals["__file__"])
        finally:
            self.cursor.close()
            self.db.close()