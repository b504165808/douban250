import datetime
import hashlib
import logging
import re
from bs4 import BeautifulSoup
from douban_web_app.db_piplines.mysql_db_controller import MysqlDbControllerCls

class DouBanHandlersCls:

    def __init__(self):
        pass

    def handlers(self, data, page_cursor):
        html = BeautifulSoup(data, "lxml")
        tb_list = html.find_all("table")
        book_data_insert_list = []
        book_data_list = []
        for tb in tb_list:
            try:
                book_link = tb.find("div", attrs=("class", "pl2")).find("a").get("href")
                book_title = tb.find("div", attrs=("class", "pl2")).find("a").get("title")
                book_img = tb.find("a", attrs=("class", "nbg")).find("img").get("src")
                book_info = tb.find("p", attrs=("class", "pl")).text
                book_rating = tb.find("div", attrs=("class", "star")).find("span", attrs=("class", "rating_nums")).text
                book_comments = tb.find("div", attrs=("class", "star")).find("span", attrs=("class", "pl")).text
                book_comments = re.sub("[(人评价)\n ]", "", book_comments)
                create_time = datetime.date.today()

                hl = hashlib.md5()
                hl.update((book_title + book_link + book_info + str(create_time)).encode("utf-8"))
                # book_id  为每本书各维度进行md5后的唯一特征值，用于索引去重，在数据库入库时作为主键
                book_data = {
                    "book_id": hl.hexdigest(),
                    "page_cursor": page_cursor,
                    "book_link": book_link,
                    "book_title": book_title,
                    "book_img_link": book_img,
                    "book_info": book_info,
                    "book_rating": book_rating,
                    "book_comments_num": book_comments,
                    "create_time": create_time
                }

                book_data_list.append(book_data)
                book_data_insert_list.append((book_data["book_id"], book_data["page_cursor"],book_data["book_link"], book_data["book_title"], book_data["book_img_link"], book_data["book_info"], book_data["book_rating"], book_data["book_comments_num"], book_data["create_time"]))
            except Exception as e:
                logging.error(msg="数据格式化处理错误" + str(e) + str(e.__traceback__.tb_lineno) + e.__traceback__.tb_frame.f_globals["__file__"])
        # 将数据批量存储到数据库
        MysqlDbControllerCls().insert_data_list(data_list=book_data_insert_list)
        return book_data_list