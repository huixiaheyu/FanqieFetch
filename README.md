# 番茄小说采集工具

一个用于采集番茄小说网站内容的工具。番茄小说通过自定义字体把正文中的常用字替换为私有字形来实现反爬，本项目通过解析这些 woff 字体文件，将字形渲染为图片并 OCR 识别，从而还原真实的正文内容。

## 项目结构

```plaintext
FanqieFetch/
├─ data/                    # 字体文件目录（woff2，运行时生成/下载，不入库）
├─ fanqie/                  # 核心包
│  ├─ __init__.py           # 路径常量（统一相对项目根定位）
│  ├─ woff_to_jpg.py        # 将 woff 字体字形渲染为图片
│  ├─ jpg_to_dic.py         # 对字形图片 OCR，生成 {unicode: 真实文字} 字典
│  ├─ UI.py                 # 手动确认字库识别的 GUI 界面
│  ├─ spider.py             # 章节内容采集（含反爬字符解密）
│  └─ search.py             # 搜索接口（msToken/a_bogus 需自行生成）
├─ output/                  # 产物目录
│  ├─ wait_for_identify_images/  # 字形图片缓存（不入库）
│  └─ charmap_dic.txt       # 生成的字库字典（不入库）
├─ main.py                  # 命令行入口
├─ pyproject.toml           # 项目元数据与依赖（uv）
├─ requirements.txt         # 依赖清单
└─ README.md
```

## 工作原理

1. 番茄小说的反爬字体会把正文中的常用字替换成私有字形；
2. 下载该 woff 字体，把每个字形渲染为图片；
3. 对图片做 OCR 识别，得到 `{Unicode值: 真实文字}` 的映射字典；
4. 采集章节正文，用字典把反爬字符替换回真实文字。

## 环境准备

项目使用 `uv` 管理依赖，并安装到 `.venv`。

```shell
# 安装 uv（如未安装）
curl -LsSf https://astral.sh/uv/install.sh | sh

# 进入项目目录，创建 .venv 并安装依赖（默认走国内清华源）
cd FanqieFetch
UV_INDEX_URL=https://pypi.tuna.tsinghua.edu.cn/simple uv sync
```

## 使用方法

```shell
# 端到端采集：自动生成字库并采集章节
uv run python main.py <章节URL>

# 如果字库识别不准，可启用 GUI 手动确认
uv run python main.py <章节URL> --manual

# 查看帮助
uv run python main.py --help
```

采集得到的正文会直接输出到终端；章节内容可进一步保存到 `output` 目录。

## 单独运行各模块

```shell
# 1. 字体转图片
uv run python -m fanqie.woff_to_jpg

# 2. 字形图片 OCR 生成字库（默认全自动）
uv run python -m fanqie.jpg_to_dic
```

## 未来计划

1. 实现 `msToken`、`a_bogus` 的自动生成（搜索接口所需）
2. 端到端批量采集整本小说
3. 自动化下载章节对应的字体文件

## 注意事项

1. 本项目仅用于学习交流，禁止用于商业用途。
2. 请遵守法律法规，不要采集违法资源。
3. 请勿频繁采集，以免对服务器造成压力。
