"""
串行批量生成 — 每张图提交后等5秒再提交下一张，避免限流
"""

import os
import time
import requests

API_KEY = os.environ.get("HUNYUAN_API_KEY", "")
BASE_URL = "https://tokenhub.tencentmaas.com/v1/api/image"
MODEL = "hy-image-v3.0"
HEADERS = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}

os.makedirs("/workspace/assets/illustrations", exist_ok=True)

TASKS = [
    {
        "name": "03-closed-loop-feedback",
        "prompt": """Generate one standalone 16:9 horizontal Chinese article illustration.

Visual DNA:
Pure white / slight rice-paper texture background. Chinese watercolor and ink painting style (水彩水墨). Black ink line art with slight wobbly hand-drawn feel. Soft watercolor wash color blocks with bleeding and blending edges. Lots of empty white space, like a child's drawing on rice paper. Sparse handwritten Chinese annotations in ink black or warm red. Clean whimsical child-illustration feeling. No gradients, no shadows, no commercial vector style, no PPT infographic look, no anime exaggeration, no realistic photo style, no complex background.

Recurring character required:
A 6-year-old Chinese girl. Core visual anchor: double hair buns (双丸子头) — two round black hair buns on top of head, with some loose bangs and stray hairs. Round chubby face. Large warm brown eyes with long lashes, curious and sincere expression. Light pink blush on cheeks. Wearing a blue-and-white Chinese hanfu with watercolor color-block patterns. Simple blue cloth shoes. Body proportion: about 2.5-3 head tall, chibi-style but not exaggerated. Ink line outlines with slight hand-drawn wobble. Expressions: curious, slightly confused, cheerful, quietly focused. She must perform the core conceptual action, not decorate the scene.

Theme:
经销商调研与闭环改进

Core idea:
调研→收集反馈→改进→再调研，形成一个永不完结的圆环。

Composition:
双丸子头蓝白汉服小女孩站在画面中央偏左，手里牵着一根细细的墨线，线的另一端系着一个小水墨圆环，圆环上有几个小节点（代表：调研→反馈→改进→再调研）。小女孩正沿着圆环走着。画面主体占约50%，右边大片留白。

Suggested elements:
水墨圆环 / 细墨线 / 小节点

Chinese handwritten labels:
调研 / 反馈 / 改进

Color use:
Dominant blues (watercolor ink-blue). Black ink outlines. Warm brown skin tones. Warm red for key labels only. Rice-paper white background.

Constraints:
Keep main subject around 40%-60% of canvas. Preserve at least 35% blank white space. Use at most 3-6 short handwritten Chinese labels. The character must be performing the central action. No title in top-left corner. No character names in image. Whimsical but not childish."""
    },
    {
        "name": "05-cost-savings",
        "prompt": """Generate one standalone 16:9 horizontal Chinese article illustration.

Visual DNA:
Pure white / slight rice-paper texture background. Chinese watercolor and ink painting style (水彩水墨). Black ink line art with slight wobbly hand-drawn feel. Soft watercolor wash color blocks with bleeding and blending edges. Lots of empty white space, like a child's drawing on rice paper. Sparse handwritten Chinese annotations in ink black or warm red. Clean whimsical child-illustration feeling. No gradients, no shadows, no commercial vector style, no PPT infographic look, no anime exaggeration, no realistic photo style, no complex background.

Recurring character required:
A 6-year-old Chinese girl. Core visual anchor: double hair buns (双丸子头) — two round black hair buns on top of head, with some loose bangs and stray hairs. Round chubby face. Large warm brown eyes with long lashes, curious and sincere expression. Light pink blush on cheeks. Wearing a blue-and-white Chinese hanfu with watercolor color-block patterns. Simple blue cloth shoes. Body proportion: about 2.5-3 head tall, chibi-style but not exaggerated. Ink line outlines with slight hand-drawn wobble. Expressions: curious, slightly confused, cheerful, quietly focused. She must perform the core conceptual action, not decorate the scene.

Theme:
激励政策精准管控

Core idea:
统筹全省1000余名业务人员的激励政策核算，通过精准数据校验，为企业节约成本500余万元。

Composition:
双丸子头蓝白汉服小女孩站在画面左前方，面前堆着一座小山一样的水墨数字块（代表1000+人员数据核算）。小女孩双手捧着一颗闪亮的小星星（代表节约的500万成本），举过头顶，表情惊喜又认真。数字小山旁边有简单的加号和等号符号。主体占左半边，右边大片留白。

Suggested elements:
水墨数字小山 / 小星星 / 加号等号符号

Chinese handwritten labels:
数据 / 精准 / 节约

Color use:
Dominant blues (watercolor ink-blue). Black ink for numbers and outlines. Warm brown skin tones. Warm red only for the star or key labels. Rice-paper white background.

Constraints:
Keep main subject around 40%-60% of canvas. Preserve at least 35% blank white space. Use at most 3-6 short handwritten Chinese labels. The character must be performing the central action. No title in top-left corner. No character names in image. Whimsical but not childish."""
    }
]

def submit(prompt):
    resp = requests.post(f"{BASE_URL}/submit", headers=HEADERS, json={"model": MODEL, "prompt": prompt}, timeout=30)
    data = resp.json()
    tid = data.get("id")
    if not tid:
        raise Exception(f"提交失败，返回: {data}")
    print(f"  📤 任务ID: {tid}")
    return tid

def query(task_id):
    resp = requests.post(f"{BASE_URL}/query", headers=HEADERS, json={"model": MODEL, "id": task_id}, timeout=30)
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
        print(f"  ⏳ [{name}] {elapsed}s — {status}")
        if status in ("completed", "success", "done"):
            return url
        if status in ("failed", "error"):
            raise Exception(f"[{name}] 生成失败: {data}")
        time.sleep(6)
    raise TimeoutError(f"[{name}] 等待超时")

def download(url, path):
    resp = requests.get(url, timeout=60)
    with open(path, "wb") as f:
        f.write(resp.content)
    print(f"  ✅ 已保存: {path} ({len(resp.content)//1024}KB)")

print("=" * 50)
print("开始串行生成 2 张图片...")
print("=" * 50)

for i, task in enumerate(TASKS):
    name = task["name"]
    prompt = task["prompt"]
    print(f"\n[{i+1}/{len(TASKS)}] 生成: {name}")

    # 提交
    tid = submit(prompt)
    print(f"  ✅ 已提交，等待生成...")
    time.sleep(5)  # 提交间隔5秒

    # 等待完成
    try:
        url = wait_for(tid, name)
        path = f"/workspace/assets/illustrations/{name}.png"
        download(url, path)
    except Exception as e:
        print(f"  ❌ 错误: {e}")

print("\n" + "=" * 50)
print("全部完成！")
print("=" * 50)
