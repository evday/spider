import requests
import re
import time
import hashlib

from requests.exceptions import RequestException
movie_path = "E:\校花视频\MP4"
def get_page(url):
    """获取页面"""
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.content
    except RequestException as e:
        raise ('访问的页面不存在')

#根据首页内容获取视频页面url
def index_url(res):
    '''解析主页'''
    try:
        details_urls = re.findall('class="items".*?<a href="(.*?)"',res,re.S)
        for detail_url in details_urls:
            if not detail_url.startswith('http'):
                detail_url = 'http://www.xiaohuar.com/'+detail_url
            yield detail_url
    except Exception:
        pass

#根据视频页面内容获取MP4 url
def movie(res):
    movie_urls = re.findall('id="media".*?src="(.*?)"',res,re.S)
    if movie_urls:
        movie_url = movie_urls[0]
        if movie_url.endswith("mp4"):
            yield movie_url

# 存储
def get_movie(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            m = hashlib.md5()
            m.update(str(time.time()).encode("utf-8"))
            m.update(url.encode("utf-8"))
            filename = "%s%s.mp4"%(movie_path,m.hexdigest()) # 生成文件名
            print(filename)
            with open(filename,"wb") as f:
                f.write(response.content) # response.content  获取二进制数据
                print("下载成功")
    except Exception:
        pass
def main():
    url = 'http://www.xiaohuar.com/list-3-{page_num}.html'
    for i in range(5):
        #爬取主页
        index_page = get_page(url.format(page_num=i))
        #解析主页，拿到视频所在的地址列表
        detail_urls = index_url(index_page)
        #循环爬取视频页
        for detail_url in detail_urls:
            #爬取视频页
            detail_page = get_page(detail_url)
            #拿到视频的url
            movie_urls = movie(detail_page)
            for movie_url in movie_urls:
                # 保存视频
                get_movie(movie_url)
if __name__ == '__main__':
    main()
