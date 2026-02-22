import requests
from bs4 import BeautifulSoup
import time
import random
import json
from datetime import datetime

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Referer": "https://gdgpo.czt.gd.gov.cn",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Language": "zh-CN,zh;q=0.9",
}

BASE_URL = "https://gdgpo.czt.gd.gov.cn"
SEARCH_URL = f"{BASE_URL}/freecms/rest/cm/notice/selectInfoMoreByParam.do"


def fetch_notices(page=1):
    params = {
        "districtCode": "441900",
        "pageNo": page,
        "pageSize": 20,
        "noticeType": "001",
    }
    try:
        resp = requests.get(SEARCH_URL, params=params, headers=HEADERS, timeout=15)
        print(f"Response status: {resp.status_code}")
        print(f"Response content: {resp.text[:500]}")
        resp.raise_for_status()
        data = resp.json()
        items = data.get("result", {}).get("data", [])
        total = data.get("result", {}).get("total", 0)
        print(f"第{page}页: 获取到 {len(items)} 条, 总计 {total} 条")
        return items, total
    except Exception as e:
        print(f"[抓取失败] 第{page}页: {e}")
        return [], 0


def parse_notice(item):
    return {
        "项目名称": item.get("noticeName", "").strip(),
        "采购人": item.get("tenderee", "").strip(),
        "代理机构": item.get("agentName", "").strip(),
        "项目编号": item.get("projectCode", "").strip(),
        "发布时间": item.get("publishDate", "").strip(),
        "详情URL": f"{BASE_URL}/freecms/site/1/notice/{item.get('noticeId','')}.html",
    }


def run():
    print("=== 开始抓取东莞市政府采购公告 ===")
    all_notices = []
    for page in range(1, 6):
        print(f"正在抓取第 {page} 页...")
        items, total = fetch_notices(page)
        if not items:
            break
        for item in items:
            all_notices.append(parse_notice(item))
        print(f"  本页 {len(items)} 条，累计 {len(all_notices)} 条")
        time.sleep(random.uniform(2, 3))
    print(f"抓取完成，共 {len(all_notices)} 条")
    return all_notices
