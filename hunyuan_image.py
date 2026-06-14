"""
腾讯混元文生图自动化工具
用法: python hunyuan_image.py "你的prompt内容"
"""

import os
import sys
import time
import requests
import json

# ============ 配置区 ============
# 从环境变量读取 API Key，避免硬编码泄露
API_KEY = os.environ.get("HUNYUAN_API_KEY", "")
if not API_KEY:
    raise ValueError("请设置环境变量 HUNYUAN_API_KEY\nLinux/Mac: export HUNYUAN_API_KEY='sk-xxxxx'\nWindows: set HUNYUAN_API_KEY=sk-xxxxx")

BASE_URL = "https://tokenhub.tencentmaas.com/v1/api/image"
MODEL = "hy-image-v3.0"
# ============ 配置区结束 ============


def submit_image(prompt: str) -> str:
    """提交文生图任务，返回任务 ID"""
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": MODEL,
        "prompt": prompt
    }

    print(f"📤 正在提交任务...")
    resp = requests.post(f"{BASE_URL}/submit", headers=headers, json=payload, timeout=30)
    resp.raise_for_status()
    data = resp.json()

    if data.get("error"):
        raise Exception(f"提交失败: {data['error']}")

    task_id = data.get("id") or data.get("data", {}).get("id")
    print(f"✅ 任务已提交，ID: {task_id}")
    return task_id


def query_image(task_id: str) -> dict:
    """查询任务状态"""
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": MODEL,
        "id": task_id
    }

    resp = requests.post(f"{BASE_URL}/query", headers=headers, json=payload, timeout=30)
    resp.raise_for_status()
    return resp.json()


def wait_and_download(task_id: str, output_path: str, max_wait: int = 120) -> str:
    """轮询等待图片生成完成，然后下载"""
    print(f"⏳ 等待图片生成（最多 {max_wait} 秒）...")
    start = time.time()

    while time.time() - start < max_wait:
        result = query_image(task_id)
        status = (result.get("status") or result.get("data", {}).get("status") or "").lower()

        elapsed = int(time.time() - start)
        print(f"  [{elapsed}s] 状态: {status}")

        if status == "success" or status == "completed" or status == "done":
            # 取图片 URL
            image_url = (
                result.get("data", {}).get("image_url")
                or result.get("image_url")
                or result.get("url")
                or result.get("images", [{}])[0].get("url")
                or result.get("data", {}).get("url")
            )
            if image_url:
                print(f"🖼️  下载图片...")
                img_resp = requests.get(image_url, timeout=60)
                img_resp.raise_for_status()
                with open(output_path, "wb") as f:
                    f.write(img_resp.content)
                print(f"✅ 图片已保存: {output_path}")
                return output_path
            else:
                print(f"⚠️  状态成功但未找到图片 URL，返回内容: {json.dumps(result, ensure_ascii=False)[:300]}")

        elif status == "failed" or status == "error":
            raise Exception(f"生成失败: {json.dumps(result, ensure_ascii=False)}")

        time.sleep(5)

    raise TimeoutError(f"等待超时（{max_wait}s），请稍后手动查询任务 {task_id}")


def generate_image(prompt: str, output_path: str = "output.png") -> str:
    """
    完整流程：提交 → 等待 → 下载
    """
    task_id = submit_image(prompt)
    return wait_and_download(task_id, output_path)


def main():
    if len(sys.argv) < 2:
        print("用法: python hunyuan_image.py \"你的prompt内容\" [输出文件名]")
        print("示例: python hunyuan_image.py \"雨中, 竹林, 小路\"")
        sys.exit(1)

    prompt = sys.argv[1]
    output = sys.argv[2] if len(sys.argv) > 2 else "hunyuan_output.png"

    print(f"=" * 40)
    print(f"Prompt: {prompt}")
    print(f"输出: {output}")
    print(f"=" * 40)

    try:
        path = generate_image(prompt, output)
        print(f"\n🎉 完成！图片路径: {path}")
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
