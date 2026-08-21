"""番茄小说搜索接口。

注：接口需要 msToken 与 a_bogus 两个动态加密参数，通常通过前端 JS
（webmssdk）生成。本项目尚未实现参数生成，调用时需自行传入。
"""

import requests

SEARCH_URL = "https://fanqienovel.com/api/author/search/search_book/v1"

HEADERS = {
    "accept": "application/json, text/plain, */*",
    "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
    "priority": "u=1, i",
    "sec-ch-ua": '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
}


def search_book(
    keyword: str,
    ms_token: str,
    a_bogus: str,
    page_index: int = 0,
    page_count: int = 10,
) -> dict:
    """搜索小说。

    Args:
        keyword: 搜索关键词。
        ms_token: 动态加密参数 msToken。
        a_bogus: 动态加密参数 a_bogus。
        page_index: 页码（从 0 开始）。
        page_count: 每页数量。

    Returns:
        接口返回的 JSON 数据。
    """
    headers = dict(HEADERS)
    headers["referer"] = f"https://fanqienovel.com/search/{keyword}"

    params = {
        "filter": "127,127,127,127",
        "page_count": str(page_count),
        "page_index": str(page_index),
        "query_type": "0",
        "query_word": keyword,
        "msToken": ms_token,
        "a_bogus": a_bogus,
    }

    response = requests.get(SEARCH_URL, headers=headers, params=params, timeout=10)
    response.raise_for_status()
    return response.json()


if __name__ == "__main__":
    # 示例：需自行提供有效的 msToken 与 a_bogus
    data = search_book(
        keyword="惊鸿",
        ms_token="<your_ms_token>",
        a_bogus="<your_a_bogus>",
    )
    print(data)
