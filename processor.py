import json
import time
import random
import os
from openai import OpenAI

GLM_API_KEY = os.environ.get("ZHIPUAI_API_KEY", "")
SCORE_THRESHOLD = 6

if GLM_API_KEY:
    client = OpenAI(
        api_key=GLM_API_KEY,
        base_url="https://open.bigmodel.cn/api/paas/v4/"
    )
else:
    client = None

PROMPT = """你是一个商业顾问，判断政府采购项目是否适合一人AI应用开发公司承接。

适合：软件开发、AI应用、数字化系统、智能化改造、数据分析、小程序/APP开发、信息化建设
不适合：建筑工程、纯硬件设备采购、大型系统集成、医疗设备、车辆采购、绿化工程

项目名称：{title}

返回JSON格式（只返回JSON，不要其他内容）：
{{"score": 0-10, "suitable": true/false, "reason": "一句话理由"}}"""


def filter_notice(notice):
    if not client:
        notice["AI评分"] = 8
        notice["是否适合"] = True
        notice["AI理由"] = "跳过AI过滤（未配置API Key）"
        return notice
    
    try:
        resp = client.chat.completions.create(
            model="glm-4.7-flash",
            messages=[{
                "role": "user",
                "content": PROMPT.format(title=notice["项目名称"])
            }],
            temperature=0.1,
        )
        raw = resp.choices[0].message.content.strip()
        raw = raw.replace("```json", "").replace("```", "").strip()
        result = json.loads(raw)
        notice["AI评分"] = result.get("score", 0)
        notice["是否适合"] = result.get("suitable", False)
        notice["AI理由"] = result.get("reason", "")
    except Exception as e:
        print(f"[GLM失败] {notice['项目名称']}: {e}")
        notice["AI评分"] = -1
        notice["是否适合"] = False
        notice["AI理由"] = f"过滤失败: {e}"
    return notice


def run(notices):
    print(f"=== 开始过滤，共 {len(notices)} 条 ===")
    filtered = []
    for i, notice in enumerate(notices):
        print(f"  过滤 {i+1}/{len(notices)}: {notice['项目名称'][:30]}...")
        result = filter_notice(notice)
        if result["AI评分"] >= SCORE_THRESHOLD:
            filtered.append(result)
        time.sleep(random.uniform(0.5, 1))
    filtered.sort(key=lambda x: x["AI评分"], reverse=True)
    print(f"过滤完成，符合条件 {len(filtered)} 条")
    return filtered
