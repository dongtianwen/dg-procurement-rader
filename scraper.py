import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
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


def create_session():
    """创建带重试机制的 session"""
    session = requests.Session()
    retry = Retry(
        total=5,
        backoff_factor=1,
        status_forcelist=[500, 502, 503, 504],
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session


def fetch_notices(page=1, session=None):
    params = {
        "districtCode": "441900",
        "pageNo": page,
        "pageSize": 20,
        "noticeType": "001",
    }
    
    if session is None:
        session = create_session()
    
    try:
        resp = session.get(SEARCH_URL, params=params, headers=HEADERS, timeout=30)
        print(f"Response status: {resp.status_code}")
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
    session = create_session()
    all_notices = []
    
    for page in range(1, 6):
        print(f"正在抓取第 {page} 页...")
        items, total = fetch_notices(page, session)
        if not items:
            print(f"第 {page} 页无数据，停止抓取")
            break
        for item in items:
            all_notices.append(parse_notice(item))
        print(f"  本页 {len(items)} 条，累计 {len(all_notices)} 条")
        time.sleep(random.uniform(3, 5))
    
    print(f"抓取完成，共 {len(all_notices)} 条")
    return all_notices
