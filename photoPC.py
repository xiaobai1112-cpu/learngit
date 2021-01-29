import requests
from bs4 import BeautifulSoup
import os
import time

all_url = 'http://www.mzitu.com'


#http请求头
Hostreferer = {
    'User-Agent': 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)',
    'Referer': 'http://www.mzitu.com'
               }
Picreferer = {
    'User-Agent': 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)',
    'Referer': 'http://i.meizitu.net'
}
#此请求头破解盗链



#保存地址
path = 'E:\Python学习过程\爬虫图片'

#记录文件
data = 'E:\Python学习过程\爬虫图片'

#读取保存记录
def get_log(file):
    page = 1
    line = 0
    try:
        with open(file, 'r') as f:
            l = f.readline()
            page, line = [int(i) for i in l.split('|')]
    except Exception as e:
        print(e)
        print('读取记录失败，从初始开始')
    return page, line


#保存记录
def put_log(file, page, line):
    try:
        with open(file, "w") as f:
            f.write('{}|{}'.format(page, line))
    except Exception as e:
        print('保存记录失败：[{}]'.format(e))


#找寻最大页数
def find_max_page():
    start_html = requests.get(all_url, headers=Hostreferer)
    soup = BeautifulSoup(start_html.text, "html.parser")
    page = soup.find_all('a', class_='page-numbers')
    max_page = page[-2].text
    max_page = int(max_page)
    return max_page

if __name__ == "__main__":
    same_url = 'https://www.mzitu.com/best/'
    max_page = find_max_page()
    page, line = get_log(data)
    print('从{}页，{}行开始缓存'.format(page, line))
    for n in range(page, int(max_page)+1):
        ul = same_url+str(n)
        start_html = requests.get(ul, headers=Hostreferer)
        soup = BeautifulSoup(start_html.text, "html.parser")
        all_a = soup.find('div', class_='postlist').find_all('a', target='_blank')
        for lines in range(line, len(all_a)):
            a = all_a[lines]
            title = a.get_text() #提取文本
            if(title != ''):
                print("准备扒取："+title)

                #win不能创建带？的目录
                if(os.path.exists(path+title.strip().replace('?',''))):
                        #print('目录已存在')
                        flag = 1
                else:
                    os.makedirs(path+title.strip().replace('?',''))
                    flag = 0
                os.chdir(path + title.strip().replace('?', ''))
                href = a['href']
                html = requests.get(href, headers=Hostreferer)
                mess = BeautifulSoup(html.text, "html.parser")
                # 最大也在class='pagenavi'div中的第6个span
                pic_max = mess.find("div", class_='pagenavi').find_all('span')
                pic_max = pic_max[6].text #最大页数
                if(flag == 1 and len(os.listdir(path+title.strip().replace('?',''))) >= int(pic_max)):
                    print('已经保存完毕，跳过')
                    continue
                for num in range(1, int(pic_max)+1):
                    while True:
                        pic = href+'/'+str(num)
                        html = requests.get(pic, headers=Hostreferer)
                        mess = BeautifulSoup(html.text, "html.parser")
                        pic_url = mess.find('img', alt=title)
                        if(pic_url):
                            break
                    # print(pic_url['src'])
                    html = requests.get(pic_url['src'], headers=Picreferer)
                    file_name = pic_url['src'].split(r'/')[-1]
                    f = open(file_name, 'wb')
                    f.write(html.content)
                    f.close()
                put_log(data, n, lines)
                time.sleep(0.5)
        print('第',n,'页完成')
        line = 0
        time.sleep(10)
