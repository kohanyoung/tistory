import requests
import xml.etree.ElementTree as ET
from datetime import datetime

# 티스토리 RSS 피드 주소 (본인 블로그 주소로 변경)
RSS_FEED_URL = "https://isayyeah.tistory.com/rss"
SITEMAP_FILE = "sitemap-custom.xml"

def fetch_rss_feed():
    response = requests.get(RSS_FEED_URL)
    if response.status_code != 200:
        print("❌ RSS 피드 가져오기 실패")
        return None
    return response.text

def generate_sitemap(rss_xml):
    root = ET.fromstring(rss_xml)
    sitemap_root = ET.Element("urlset", xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")

    for item in root.findall(".//item"):
        url = item.find("link").text
        pub_date = item.find("pubDate").text
        lastmod = datetime.strptime(pub_date, "%a, %d %b %Y %H:%M:%S %z").strftime("%Y-%m-%d")

        url_element = ET.SubElement(sitemap_root, "url")
        ET.SubElement(url_element, "loc").text = url
        ET.SubElement(url_element, "lastmod").text = lastmod
        ET.SubElement(url_element, "changefreq").text = "daily"
        ET.SubElement(url_element, "priority").text = "0.8"

    tree = ET.ElementTree(sitemap_root)
    tree.write(SITEMAP_FILE, encoding="utf-8", xml_declaration=True)
    print(f"✅ 사이트맵 생성 완료: {SITEMAP_FILE}")

if __name__ == "__main__":
    rss_xml = fetch_rss_feed()
    if rss_xml:
        generate_sitemap(rss_xml)
