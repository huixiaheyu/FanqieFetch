"""章节内容采集：获取正文并用字库字典解密反爬字符。"""

import ast
from pathlib import Path

import requests
from lxml import etree

from . import CHARMAP_FILE

# 请求头模拟浏览器
HEADERS = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
    "cache-control": "max-age=0",
    "priority": "u=0, i",
    "sec-ch-ua": '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "cross-site",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
}


def load_charmap(charmap_file: str | Path = CHARMAP_FILE) -> dict[str, str]:
    """读取字库字典 {unicode值.jpg: 真实文字}。"""
    path = Path(charmap_file)
    if not path.exists():
        return {}
    content = path.read_text(encoding="utf-8").strip()
    if not content:
        return {}
    return ast.literal_eval(content)


def fetch_chapter(url: str, charmap: dict[str, str] | None = None) -> str:
    """抓取章节正文并解密反爬字符。

    Args:
        url: 章节阅读页 URL。
        charmap: 字库字典；为空时自动读取默认文件。

    Returns:
        解密后的正文文本。
    """
    if charmap is None:
        charmap = load_charmap()

    response = requests.get(url, headers=HEADERS, timeout=10)
    response.raise_for_status()

    tree = etree.HTML(response.text)
    paragraphs = tree.xpath('//div[@class="muye-reader-content noselect"]//p')
    article = "\n".join(p.text for p in paragraphs if p.text)

    # 替换反爬字符：若字符对应字库有映射则替换，否则保留原文
    decrypted = "".join(
        charmap.get(f"{ord(letter)}.jpg", letter).strip() for letter in article
    )
    return decrypted


if __name__ == "__main__":
    url = "https://fanqienovel.com/reader/7076047336530510370"
    print(fetch_chapter(url))
