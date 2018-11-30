from selenium import webdriver
from lxml import etree
import time
import random


class parse(object):
    def __init__(self):
        self.start_url = "https://www.lagou.com/jobs/list_python?px=default&city=%E6%9D%AD%E5%B7%9E"
        self.drive = webdriver.Chrome(executable_path=r"C:\Users\WDXCQ\Desktop\Learning\spiderTool/chromedriver.exe")
        self.urls = []
        self.fp = open("./doc/urls.txt", "a", encoding="utf-8")

    def parse_first(self):
        self.drive.get(url=self.start_url)
        i = 1
        second = random.randint(1, 4)
        while True:
            try:
                time.sleep(second)
                self.get_url(self.drive.page_source)
                time.sleep(second)
                next_btn = self.drive.find_element_by_class_name('pager_next')
                next_btn.click()
                time.sleep(second)
                i += 1
            except:
                print("第%s页：error"%i)
            if i > 30:
                self.write_urls()
                break
        self.drive.close()

    def write_urls(self):
        i = 1
        for url in self.urls:
            print("第%d页链接数：%d"%(i, len(url)))
            i += 1
            for link in url:
                print(link)
                self.fp.write(link + "\n")
        self.fp.close()


    def get_url(self, response):
        html_sourse = etree.HTML(response)
        # 得到详细页面URL列表
        url_links = html_sourse.xpath('//a[@class="position_link"]/@href')
        self.urls.append(url_links)


if __name__ == '__main__':
    p = parse()
    p.parse_first()