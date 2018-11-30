import time
from lxml import etree
from selenium import webdriver
import random


class parse():
    def __init__(self):
        self.urls = None
        self.drive = webdriver.Chrome(executable_path=r"C:\Users\WDXCQ\Desktop\Learning\spiderTool/chromedriver.exe")
        self.fail_url = []
        self.items = []

    def run(self):
        self.get_urls()
        i = 0
        for url in self.urls:
            item = {}
            url = url.strip()
            second = random.randint(1,5)
            try:
                # 发送请求
                self.drive.get(url)
                # 获取响应页面
                html = self.drive.page_source
                content = etree.HTML(html)
                # 获取指定数据字段
                position_salary = content.xpath('//div/span[@class="name"]/text()')
                position_name = content.xpath('//span[@class="salary"]/text()')
                position_conpany = content.xpath('//img[@class="b2"]/@alt')
                position_place = content.xpath('//div[@class="work_addr"]/a/text()')

                if position_salary == [] or position_name == [] or position_conpany == [] or position_place == []:
                    '''判断爬取的字段是否为空值，为空则把当前爬取失败的url加入到url失败列表'''
                    print(url, "error")
                    self.fail_url.append(url)
                    time.sleep(5)
                    continue
                # 将数据字段以字典类型保存
                item["position_salary"] = position_salary
                item["position_name"] = position_name
                item["position_conpay"] = position_conpany
                item["position_place"] = position_place[:-1]
                # 将数据添加到items中等待写入本地文件
                self.items.append(item)
                time.sleep(second)
            except:
                # 异常则抛出爬取失败的url，保存到fail列表
                print(url,"error")
                time.sleep(3)
                self.fail_url.append(url)
            # 设置爬取网页的数量
            if i > 448:
                break
            i += 1
        # 关闭Chrome浏览器
        self.drive.quit()
        self.write_data()
        self.wirte_fail_url()

    def wirte_fail_url(self):
        '''将爬取失败的url保存到本地，重新爬取'''
        fp = open("./doc/fail.txt", "w", encoding="utf-8")
        for i in self.fail_url:
            fp.write(i + "\n")
        fp.close()

    def write_data(self):
        '''写入数据，保存到本地'''
        fp = open("./doc/position.txt", "a", encoding="utf-8")
        for i in self.items:
            data = str(i)
            fp.write(data + "\n")
        fp.close()

    def get_urls(self):
        '''获取待爬取的url列表'''
        with open("./doc/urls.txt", "r") as fp:
            self.urls = fp.readlines()

        # 第二次，及以上时使用，重新爬取之前爬取失败的ur
        # with open("./doc/fail.txt", "r") as fp:
        #     self.urls = fp.readlines()


if __name__ == '__main__':
    p = parse()
    p.run()

