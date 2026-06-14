"""
批量生成配图 — 职责业绩篇
一次性提交 4 张图，自动等待下载
"""

import os
import time
import requests
import json
import sys

API_KEY = os.environ.get("HUNYUAN_API_KEY", "")
if not API_KEY:
    raise ValueError("请设置环境变量 HUNYUAN_API_KEY")

BASE_URL = "https://tokenhub.tencentmaas.com/v1/api/image"
MODEL = "hy-image-v3.0"
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

PROMPTS = [
    {
        "name": "02-target-management",
        "prompt": """Generate one standalone 16:9 horizontal Chinese article illustration.

Visual DNA:
Pure white / slight rice-paper texture background. Chinese watercolor and ink painting style (水彩水墨). Black ink line art with slight wobbly hand-drawn feel. Soft watercolor wash color blocks with bleeding and blending edges. Lots of empty white space, like a child's drawing on rice paper. Sparse handwritten Chinese annotations in ink black or warm red. Clean whimsical child-illustration feeling. No gradients, no shadows, no commercial vector style, no PPT infographic look, no anime exaggeration, no realistic photo style, no complex background.

Recurring character required:
A 6-year-old Chinese girl. Core visual anchor: double hair buns (双丸子头) — two round black hair buns on top of head, with some loose bangs and stray hairs. Round chubby face. Large warm brown eyes with long lashes, curious and sincere expression. Light pink blush on cheeks. Wearing a blue-and-white Chinese hanfu with watercolor color-block patterns — cross-collar robe with waist sash, the fabric has visible ink-blue watercolor bleeding. Simple blue cloth shoes. Body proportion: about 2.5-3 head tall, chibi-style but not exaggerated. Ink line outlines with slight hand-drawn wobble. Expressions: curious, slightly confused, cheerful, quietly focused — never overly dramatic or cute. She must perform the core conceptual action, not decorate the scene. Keep her serious, curious, slightly lost-in-thought, not mascot-cute.

Theme:
部门管理与目标落地 (Department Management and Goal Execution)

Core idea:
把年度目标拆解成可落地的任务，一步一步执行达成。

Composition:
双丸子头蓝白汉服小女孩站在画面中央偏左，周围散落着几个大小不一的水墨方盒子（代表部门目标），每个盒子上有简单符号。她一只手高举着一面小旗子（代表目标旗帜），另一只手正在打开或检查其中一个盒子。她的表情是认真好奇的，歪着头思考。画面以蓝白为主，主体占左半边，右边大量留白。

Suggested elements:
水墨方盒子若干 / 小旗子 / 简单符号 / 几条虚线（代表连接）

Chinese handwritten labels:
目标 / 落地 / 执行

Color use:
Dominant blues (watercolor ink-blue). Black ink outlines. Warm brown skin tones. Warm red for key labels only. Rice-paper white background.

Constraints:
One image explains only one core structure. Keep main subject around 40%-60% of canvas. Preserve at least 35% blank white space. Use at most 3-6 short handwritten Chinese labels. The character with double hair buns and blue hanfu must be performing the central action. No title in top-left corner. No structure type labels. No character names in image. It should be clear but not instructional, whimsical but not childish."""
    },
    {
        "name": "03-closed-loop-feedback",
        "prompt": """Generate one standalone 16:9 horizontal Chinese article illustration.

Visual DNA:
Pure white / slight rice-paper texture background. Chinese watercolor and ink painting style (水彩水墨). Black ink line art with slight wobbly hand-drawn feel. Soft watercolor wash color blocks with bleeding and blending edges. Lots of empty white space, like a child's drawing on rice paper. Sparse handwritten Chinese annotations in ink black or warm red. Clean whimsical child-illustration feeling. No gradients, no shadows, no commercial vector style, no PPT infographic look, no anime exaggeration, no realistic photo style, no complex background.

Recurring character required:
A 6-year-old Chinese girl. Core visual anchor: double hair buns (双丸子头) — two round black hair buns on top of head, with some loose bangs and stray hairs. Round chubby face. Large warm brown eyes with long lashes, curious and sincere expression. Light pink blush on cheeks. Wearing a blue-and-white Chinese hanfu with watercolor color-block patterns — cross-collar robe with waist sash, the fabric has visible ink-blue watercolor bleeding. Simple blue cloth shoes. Body proportion: about 2.5-3 head tall, chibi-style but not exaggerated. Ink line outlines with slight hand-drawn wobble. Expressions: curious, slightly confused, cheerful, quietly focused — never overly dramatic or cute. She must perform the core conceptual action, not decorate the scene. Keep her serious, curious, slightly lost-in-thought, not mascot-cute.

Theme:
经销商调研与闭环改进 (Distributor Research and Closed-Loop Improvement)

Core idea:
调研→收集反馈→改进→再调研，形成一个永不完结的圆环。

Composition:
双丸子头蓝白汉服小女孩站在画面中央偏左，手里牵着一根细细的墨线（代表反馈链路），线的另一端系着一个小水墨圆环，圆环上有几个小节点（代表：调研→反馈→改进→再调研）。小女孩正沿着圆环走着，像在追踪这条路径。圆环线条是墨色的，留白充足，主体占约50%。

Suggested elements:
水墨圆环 / 细墨线 / 小节点 / 几个箭头符号

Chinese handwritten labels:
调研 / 反馈 / 改进

Color use:
Dominant blues (watercolor ink-blue). Black ink outlines for the loop. Warm brown skin tones. Warm red for key labels. Rice-paper white background.

Constraints:
One image explains only one core structure. Keep main subject around 40%-60% of canvas. Preserve at least 35% blank white space. Use at most 3-6 short handwritten Chinese labels. The character with double hair buns and blue hanfu must be performing the central action. No title in top-left corner. No structure type labels. No character names in image. It should be clear but not instructional, whimsical but not childish."""
    },
    {
        "name": "05-cost-savings",
        "prompt": """Generate one standalone 16:9 horizontal Chinese article illustration.

Visual DNA:
Pure white / slight rice-paper texture background. Chinese watercolor and ink painting style (水彩水墨). Black ink line art with slight wobbly hand-drawn feel. Soft watercolor wash color blocks with bleeding and blending edges. Lots of empty white space, like a child's drawing on rice paper. Sparse handwritten Chinese annotations in ink black or warm red. Clean whimsical child-illustration feeling. No gradients, no shadows, no commercial vector style, no PPT infographic look, no anime exaggeration, no realistic photo style, no complex background.

Recurring character required:
A 6-year-old Chinese girl. Core visual anchor: double hair buns (双丸子头) — two round black hair buns on top of head, with some loose bangs and stray hairs. Round chubby face. Large warm brown eyes with long lashes, curious and sincere expression. Light pink blush on cheeks. Wearing a blue-and-white Chinese hanfu with watercolor color-block patterns — cross-collar robe with waist sash, the fabric has visible ink-blue watercolor bleeding. Simple blue cloth shoes. Body proportion: about 2.5-3 head tall, chibi-style but not exaggerated. Ink line outlines with slight hand-drawn wobble. Expressions: curious, slightly confused, cheerful, quietly focused — never overly dramatic or cute. She must perform the core conceptual action, not decorate the scene. Keep her serious, curious, slightly lost-in-thought, not mascot-cute.

Theme:
激励政策精准管控 (Precision Incentive Management)

Core idea:
统筹全省1000余名业务人员的激励政策核算，通过精准数据校验，为企业节约成本500余万元。

Composition:
双丸子头蓝白汉服小女孩站在画面左前方，面前堆着一座小山一样大小不一的水墨数字块（代表1000+人员数据核算）。小女孩双手捧着一颗闪亮的小星星（代表节约的500万成本），举过头顶，表情惊喜又认真。数字小山旁边有简单的加号和等号符号。画面主体占左半边，右边大片留白，蓝白水墨为主色调。

Suggested elements:
水墨数字小山 / 小星星 / 加号等号符号 / 小计算符号

Chinese handwritten labels:
数据 / 精准 / 节约

Color use:
Dominant blues (watercolor ink-blue). Black ink for numbers and outlines. Warm brown skin tones. Warm red only for the star or key labels. Rice-paper white background.

Constraints:
One image explains only one core structure. Keep main subject around 40%-60% of canvas. Preserve at least 35% blank white space. Use at most 3-6 short handwritten Chinese labels. The character with double hair buns and blue hanfu must be performing the central action. No title in top-left corner. No structure type labels. No character names in image. It should be clear but not instructional, whimsical but not childish."""
    }
]

# 已生成的图片1跳过，重新提交剩余3张
def submit(prompt, name):
    payload = {"model": MODEL, "prompt": prompt}
    resp = requests.post(f"{BASE_URL}/submit", headers=HEADERS, json=payload, timeout=30)
    data = resp.json()
    task_id = data.get("id") or (data.get("data") or {}).get("id")
    print(f"  [{name}] 提交成功，ID: {task_id}")
    return task_id

def query(task_id):
    payload = {"model": MODEL, "id": task_id}
    resp = requests.post(f"{BASE_URL}/query", headers=HEADERS, json=payload, timeout=30)
    data = resp.json()
    status = data.get("status", "").lower()
    url = None
    if isinstance(data.get("data"), list) and data["data"]:
        url = data["data"][0].get("url")
    return status, url

def wait_for(task_id, name, max_wait=180):
    start = time.time()
    while time.time() - start < max_wait:
        status, url = query(task_id)
        elapsed = int(time.time() - start)
        print(f"  [{name}] {elapsed}s — {status}")
        if status in ("completed", "success", "done"):
            return url
        if status in ("failed", "error"):
            raise Exception(f"[{name}] 生成失败")
        time.sleep(5)
    raise TimeoutError(f"[{name}] 等待超时")

def download(url, path):
    resp = requests.get(url, timeout=60)
    with open(path, "wb") as f:
        f.write(resp.content)
    print(f"  ✅ 已保存: {path} ({len(resp.content)//1024}KB)")

os.makedirs("/workspace/assets/illustrations", exist_ok=True)

print("=" * 50)
print("开始批量生成 3 张图片...")
print("=" * 50)

# 提交全部
print("\n📤 提交任务...")
task_ids = {}
for item in PROMPTS:
    task_ids[item["name"]] = submit(item["prompt"], item["name"])

# 等待全部完成（轮询所有任务）
print("\n⏳ 等待生成完成...")
completed = {}
while len(completed) < len(PROMPTS):
    for item in PROMPTS:
        name = item["name"]
        if name in completed:
            continue
        status, url = query(task_ids[name])
        elapsed = "(polling)"
        print(f"  [{name}] {status}")
        if status in ("completed", "success", "done"):
            if url:
                path = f"/workspace/assets/illustrations/{name}.png"
                download(url, path)
                completed[name] = path
        elif status in ("failed", "error"):
            print(f"  ❌ [{name}] 生成失败")
            completed[name] = None
    if len(completed) < len(PROMPTS):
        time.sleep(8)

print("\n" + "=" * 50)
print("全部完成！")
for name, path in completed.items():
    if path:
        print(f"  ✅ {path}")
    else:
        print(f"  ❌ {name} 失败")
print("=" * 50)
