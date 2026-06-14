"""
王果果配图自动化工具 — 对接腾讯混元 API
用法: python wangguoguo_pipeline.py "如何才能暴富"
"""

import os
import sys
import subprocess

PROMPT_TEMPLATE = """Generate one standalone 16:9 horizontal Chinese article illustration.

Visual DNA:
Pure white / slight rice-paper texture background. Chinese watercolor and ink painting style (水彩水墨). Black ink line art with slight wobbly hand-drawn feel. Soft watercolor wash color blocks with bleeding and blending edges. Lots of empty white space, like a child's drawing on rice paper. Sparse handwritten Chinese annotations in ink black or warm red. Clean whimsical child-illustration feeling. No gradients, no shadows, no commercial vector style, no PPT infographic look, no anime exaggeration, no realistic photo style, no complex background.

Recurring character required:
A 6-year-old Chinese girl. Core visual anchor: double hair buns (双丸子头) — two round black hair buns on top of head, with some loose bangs and stray hairs. Round chubby face. Large warm brown eyes with long lashes, curious and sincere expression. Light pink blush on cheeks. Wearing a blue-and-white Chinese hanfu with watercolor color-block patterns — cross-collar robe with waist sash, the fabric has visible ink-blue watercolor bleeding. Simple blue cloth shoes. Body proportion: about 2.5-3 head tall, chibi-style but not exaggerated. Ink line outlines with slight hand-drawn wobble. Expressions: curious, slightly confused, cheerful, quietly focused — never overly dramatic or cute. She must perform the core conceptual action, not decorate the scene. Keep her serious, curious, slightly lost-in-thought, not mascot-cute.

Theme:
{theme}

Structure type:
概念隐喻 / Conceptual metaphor

Core idea:
{core_idea}

Composition:
{composition}

Suggested elements:
花盆 / 嫩芽 / 种子袋 / 小石子 / 几片叶子

Chinese handwritten labels:
播种 / 发芽 / 等待

Color use:
Dominant blues (watercolor ink-blue in varying shades, like blue ink bleeding on rice paper). Black ink for outlines and the character's hair. Warm brown / skin tones for character. Warm red only for key labels, warnings, or small emotional accents. Rice-paper white background.

Constraints:
One image explains only one core structure. Keep the main subject around 40%-60% of the canvas. Preserve at least 35% blank white space. Use at most 3-6 short handwritten Chinese labels. The character with her double hair buns and blue hanfu must be clearly visible and performing the central action. Do not write a title in the top-left corner. Do not write the structure type on the image. Do not write any character names or Chinese labels that look like names. Do not make it a formal diagram, course slide, or dense explainer. Do not make her into a cute mascot sticker; keep her as a child exploring the system. It should be clear but not instructional, whimsical but not childish, strange but clean and beautiful."""


def analyze_topic(topic: str) -> dict:
    """根据中文主题，自动推断构图元素"""
    # 这里可以放更复杂的主题分析逻辑
    return {
        "theme": topic,
        "core_idea": f"把'{topic}'这个抽象概念转化成一个童趣的物理隐喻",
        "composition": (
            f"双丸子头蓝白汉服小女孩蹲在地上，"
            f"正在用双手把 '{topic}' 的概念'种'进一个有趣的地方，"
            f"比如捧着它、埋进土里、装进盒子或举到空中。 "
            f"她的表情是认真好奇的，歪着头好像在思考。 "
            f"画面留白充足，一边主体，一边空旷。"
        )
    }


def main():
    if len(sys.argv) < 2:
        print("用法: python wangguoguo_pipeline.py \"你的主题\" [输出文件名]")
        print("示例: python wangguoguo_pipeline.py \"如何才能暴富\"")
        sys.exit(1)

    topic = sys.argv[1]
    output = sys.argv[2] if len(sys.argv) > 2 else f"wangguoguo_{hash(topic) % 10000}.png"

    print(f"=" * 50)
    print(f"🎯 主题: {topic}")
    print(f"=" * 50)

    # 1. 组装 prompt
    analysis = analyze_topic(topic)
    prompt = PROMPT_TEMPLATE.format(
        theme=analysis["theme"],
        core_idea=analysis["core_idea"],
        composition=analysis["composition"]
    )

    print(f"\n📝 组装好的 Prompt:\n")
    print(prompt[:500] + "..." if len(prompt) > 500 else prompt)
    print(f"\n")

    # 2. 调用混元 API
    script_dir = os.path.dirname(os.path.abspath(__file__))
    hunyuan_script = os.path.join(script_dir, "hunyuan_image.py")

    cmd = [sys.executable, hunyuan_script, prompt, output]

    print(f"🚀 开始调用腾讯混元 API 生成图片...")
    print(f"=" * 50)

    result = subprocess.run(cmd)

    if result.returncode == 0:
        print(f"\n🎉 全部完成！")
    else:
        print(f"\n⚠️  API 调用失败，请检查 API Key 和网络连接")


if __name__ == "__main__":
    main()
