import random

import requests

from douban_web_app.spiders import spider_settings
from douban_web_app.spiders.data_handlers.douban_handlers import DouBanHandlersCls


class DouBanSpiderCls:

    def __init__(self, page=1, proxies=None):
        """
            豆瓣爬虫主程序
             page: 当前需要爬取的页数索引
        """
        if page < 1:
            page = 1
        self.url = "https://book.douban.com/top250"
        # 豆瓣每翻动1页则索引增加25  根据此特征则得出start=page*25-25 当第一页时为start=0
        self.params = {
            "start": page * 25 - 25
        }
        # 随机选取UA 构造headers
        self.headers = {
            "Host": "book.douban.com",
            "Connection": "keep-alive",
            "sec-ch-ua": '"Chromium";v="92", " Not A;Brand";v="99", "Microsoft Edge";v="92"',
            "sec-ch-ua-mobile": "?0",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": random.choice(spider_settings.PC_UA_POOL),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-User": "?1",
            "Sec-Fetch-Dest": "document",
            # "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
            # "Cookie": "bid=l8fw_m180D4; ap_v=0,6.0; __utma=30149280.1109102405.1691374931.1691374931.1691374931.1; __utmc=30149280; __utmz=30149280.1691374931.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utma=81379588.1359215193.1691374931.1691374931.1691374931.1; __utmc=81379588; __utmz=81379588.1691374931.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmt_douban=1; __utmt=1; _pk_id.100001.3ac3=5e043aa2dea36a7a.1691374931.; _pk_ses.100001.3ac3=1; __utmb=30149280.5.10.1691374931; __utmb=81379588.5.10.1691374931"
        }
        self.page_cursor = page
        self.proxies = proxies
    def get_response(self):
        # 发起模拟请求， 如需要添加代理则在proxies进行设置
        db_html_res = requests.get(url=self.url, params=self.params, headers=self.headers, proxies=self.proxies)
        # 判断是否请求成功 响应内容是否正常
        if db_html_res.status_code == 200 and "出版社" in db_html_res.text:
            # 对数据进行清洗和处理入库
            DouBanHandlersCls().handlers(data=db_html_res.content, page_cursor=self.page_cursor)


if __name__ == '__main__':
    DouBanSpiderCls(page=1).get_response()
