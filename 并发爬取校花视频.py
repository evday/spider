import requests,re,hashlib,time
from concurrent.futures import ThreadPoolExecutor

poll = ThreadPoolExecutor(50)
movie_path = 'E:\校花视频\MP4'

#获取网页内容
def get_page(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
    except Exception:
        pass

# 解析 主页
def parse_page(index_page):
    index_page = index_page.result() # 回调函数的结果存放在result中
    urls = re.findall('class="items".*?href="(.*?)"',index_page.re.S)
    for detail_url in urls:
        if not detail_url.startswith("http"):
            detail_url = 'http://www.xiaohuar.com/'+detail_url
        poll.submit(get_page,detail_url).add_done_callback(movie_url)


def movie_url(detail_page):
    detail_page = detail_page.result()
    movie_urls = re.findall('id="media".*?src="(.*?)"',detail_page,re.S)
    if movie_urls:
        movie_url = movie_urls[0]
        if movie_url.startswith(".mp4"):
            poll.submit(movie_save,movie_url)

def movie_save(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            m = hashlib.md5()
            m.update(str(time.time()).encode("utf-8"))
            m.update(url.encode("utf-8"))
            filename = "%s%s.mp4"%(movie_path,m.hexdigest())
            with open(filename,'wb') as f:
                f.write(response.content)
                print("%s,下载完成"%url)
    except Exception:
        pass

def main():
    url = "http://www.xiaohuar.com/list-3-{page_num}.html"
    for i in range(5):
        url = url.format(page_num = i)
        poll.submit(get_page,url).add_done_callback(parse_page)

if __name__ == '__main__':
    main()

