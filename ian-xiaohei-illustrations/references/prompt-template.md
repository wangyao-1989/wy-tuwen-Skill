# 生图提示词模板

每张图单独生成。根据正文内容替换变量，不要把多张图拼在一起。

```text
Generate one standalone 16:9 horizontal Chinese article illustration.

Visual DNA:
Pure white / slight rice-paper texture background. Chinese watercolor and ink painting style (水彩水墨). Black ink line art with slight wobbly hand-drawn feel. Soft watercolor wash color blocks with bleeding and blending edges. Lots of empty white space, like a child's drawing on rice paper. Sparse handwritten Chinese annotations in ink black or warm red. Clean whimsical child-illustration feeling. No gradients, no shadows, no commercial vector style, no PPT infographic look, no anime exaggeration, no realistic photo style, no complex background.

Recurring character required:
A 6-year-old Chinese girl. **Core visual anchor: double hair buns (双丸子头)** — two round black hair buns on top of head, with some loose bangs and stray hairs. Round chubby face. Large warm brown eyes with long lashes, curious and sincere expression. Light pink blush on cheeks. Wearing a blue-and-white Chinese hanfu with watercolor color-block patterns — cross-collar robe with waist sash, the fabric has visible ink-blue watercolor bleeding. Simple blue cloth shoes. Body proportion: about 2.5-3 head tall, chibi-style but not exaggerated. Ink line outlines with slight hand-drawn wobble. Expressions: curious, slightly confused, cheerful, quietly focused — never overly dramatic or cute. She must perform the core conceptual action, not decorate the scene. Keep her serious, curious, slightly lost-in-thought, not mascot-cute.

Theme:
{正文配图主题}

Structure type:
{结构类型：Workflow / 系统局部 / 前后对比 / 角色状态 / 概念隐喻 / 方法分层 / 地图路线 / 小漫画分镜}

Core idea:
{这张图要表达的核心意思}

Composition:
{具体画面：双丸子头小女孩在哪里、正在做什么、主要物件是什么、信息如何流动}

Suggested elements:
{元素1} / {元素2} / {元素3} / {元素4}

Chinese handwritten labels:
{标注词1} / {标注词2} / {标注词3} / {标注词4} / {可选标注词5}

Color use:
Dominant blues (watercolor ink-blue in varying shades, like blue ink bleeding on rice paper). Black ink for outlines and the character's hair. Warm brown / skin tones for character. Warm red only for key labels, warnings, or small emotional accents. Rice-paper white background.

Constraints:
One image explains only one core structure. Keep the main subject around 40%-60% of the canvas. Preserve at least 35% blank white space. Use at most 3-6 short handwritten Chinese labels. The character with her double hair buns and blue hanfu must be clearly visible and performing the central action. Do not write a title in the top-left corner. Do not write the structure type on the image. Do not write any character names or Chinese labels that look like names. Do not make it a formal diagram, course slide, or dense explainer. Do not make her into a cute mascot sticker; keep her as a child exploring the system. It should be clear but not instructional, whimsical but not childish, strange but clean and beautiful.
```

## 图像编辑提示

去掉左上角标题：

```text
Edit the provided image. Remove only the handwritten title "{要删除的文字}" and its underline from the top-left corner. Fill that area with the same clean rice-paper white background, matching the surrounding blank paper. Preserve everything else exactly: characters, labels, paths, watercolor style, composition, aspect ratio, and image quality. Do not add any new text or objects.
```

增强童趣感：

```text
Regenerate this illustration with the same core meaning and simple layout, but make the double-hair-bun girl in blue hanfu more central to the conceptual action. She should be doing the curious work that explains the idea, not standing beside the diagram. Keep it watercolor-ink, sparse, hand-drawn, not cute.
```
