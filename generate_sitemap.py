import requests
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET

# 크롤링할 사이트의 URL을 입력
base_url = "https://isayyeah.tistory.com"  # 자신의 블로그 URL로 변경

# 크롤링할 URL 목록을 담을 리스트
urls = [base_url]  # 첫 번째 URL은 홈페이지로 시작

# 블로그 페이지에서 다른 링크들을 크롤링하여 추가
def crawl_site():
    response = requests.get(base_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # 예시: 블로그 내 모든 게시글 링크 찾기
    for link in soup.find_all('a', href=True):
        href = link['href']
        if href.startswith(base_url):
            if href not in urls:  # 중복되지 않게 추가
                urls.append(href)

# 사이트맵 XML 파일 생성
def generate_sitemap():
    urlset = ET.Element("urlset", xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")

    for url in urls:
        url_elem = ET.SubElement(urlset, "url")
        loc = ET.SubElement(url_elem, "loc")
        loc.text = url

    tree = ET.ElementTree(urlset)
    tree.write("sitemap-custom.xml")  # 파일명은 자유롭게 변경 가능

# 크롤링 후 사이트맵 생성
crawl_site()
generate_sitemap()
