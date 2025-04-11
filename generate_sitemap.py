import requests
import xml.etree.ElementTree as ET
from datetime import datetime

# 블로그 RSS 주소 (티스토리 블로그 기준)
BLOG_RSS_URL = "https://isayyeah.tistory.com/rss"  # 본인 블로그 주소로 변경

# 사이트맵 파일명
SITEMAP_FILE = "sitemap.xml"

def fetch_blog_posts():
    """RSS 피드를 가져와서 게시물 URL을 추출"""
    try:
        response = requests.get(BLOG_RSS_URL)
        response.raise_for_status()  # HTTP 오류 발생 시 예외를 발생시킴
    except requests.exceptions.RequestException as e:
        print(f"RSS 피드를 가져오는 중 오류가 발생했습니다: {e}")
        return []

    root = ET.fromstring(response.content)
    urls = []

    for item in root.findall(".//item"):
        link = item.find("link").text
        pub_date = item.find("pubDate").text

        try:
            # 날짜 형식이 맞지 않으면 오류가 발생할 수 있음
            date = datetime.strptime(pub_date, "%a, %d %b %Y %H:%M:%S %z").date()
        except ValueError as e:
            print(f"날짜 형식 오류: {pub_date}")
            continue

        urls.append((link, date))
    
    return urls

def generate_sitemap(urls):
    """사이트맵 XML 생성"""
    sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n'
    sitemap += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'

    for url, date in urls:
        sitemap += f"  <url>\n"
        sitemap += f"    <loc>{url}</loc>\n"
        sitemap += f"    <lastmod>{date}</lastmod>\n"
        sitemap += f"    <changefreq>daily</changefreq>\n"
        sitemap += f"    <priority>0.8</priority>\n"
        sitemap += f"  </url>\n"

    sitemap += "</urlset>"

    try:
        with open(SITEMAP_FILE, "w", encoding="utf-8") as file:
            file.write(sitemap)
        print(f"✅ {SITEMAP_FILE} 생성 완료!")
    except IOError as e:
        print(f"파일 저장 중 오류가 발생했습니다: {e}")

# 실행
if __name__ == "__main__":
    urls = fetch_blog_posts()
    if urls:
        generate_sitemap(urls)
    else:
        print("게시물을 가져오는 데 실패했습니다.")
