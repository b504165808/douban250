import datetime
import logging

from django.http import JsonResponse
from django.shortcuts import render
from douban_web_app.spiders.douban_spider import DouBanSpiderCls
# Create your views here.
from douban_web_app.db_piplines.mysql_db_controller import MysqlDbControllerCls

def index(request):
    try:
        exist_data = MysqlDbControllerCls().get_today_top_book_data(page=1, date=datetime.date.today())
        # 检索数据库中是否已经存在所需数据 如不存在则重新爬取 如存在则直接返回
        if not exist_data:
            douban_new_data = DouBanSpiderCls(page=1, proxies=None).get_response()
            return render(request, 'static/index_files/index.html', context={"douban_data": douban_new_data})
        else:
            douban_old_data = []
            for book_cursor in exist_data:
                book_data = {
                        "book_id": book_cursor[0],
                        "page_cursor": book_cursor[1],
                        "book_link": book_cursor[2],
                        "book_title": book_cursor[3],
                        "book_img_link": book_cursor[4],
                        "book_info": book_cursor[5],
                        "book_rating": book_cursor[6],
                        "book_comments_num": book_cursor[7],
                        "create_time": book_cursor[8]
                    }
                douban_old_data.append(book_data)
            return render(request, 'static/index_files/index.html', context={"douban_data": douban_old_data})
    except Exception as e:
        logging.error(msg="首页获取错误"+ str(e) + str(e.__traceback__.tb_lineno) + e.__traceback__.tb_frame.f_globals["__file__"])
        return JsonResponse({"douban_data": "首页获取失败"})
def get_douban_book_data(request):
    try:
        page = request.GET.get("page")
        # 检索数据库中是否已经存在所需数据 如不存在则重新爬取 如存在则直接返回
        exist_data = MysqlDbControllerCls().get_today_top_book_data(page=page, date=str(datetime.date.today()))
        if not exist_data:
            douban_new_data = DouBanSpiderCls(page=int(page), proxies=None).get_response()
            return render(request, 'static/index_files/index.html', context={"douban_data": douban_new_data})
        else:
            douban_old_data = []
            for book_cursor in exist_data:
                book_data = {
                    "book_id": book_cursor[0],
                    "page_cursor": book_cursor[1],
                    "book_link": book_cursor[2],
                    "book_title": book_cursor[3],
                    "book_img_link": book_cursor[4],
                    "book_info": book_cursor[5],
                    "book_rating": book_cursor[6],
                    "book_comments_num": book_cursor[7],
                    "create_time": book_cursor[8]
                }
                douban_old_data.append(book_data)
            return render(request, 'static/index_files/index.html', context={"douban_data": douban_old_data})
    except Exception as e:
        logging.error(
            msg="其他页获取错误" + str(e) + str(e.__traceback__.tb_lineno) + e.__traceback__.tb_frame.f_globals["__file__"])
        return JsonResponse({"douban_data": "其他页获取失败"})
