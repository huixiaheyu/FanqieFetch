"""番茄小说采集工具 - 命令行入口。

演示端到端流程：字体转图 -> OCR 生成字库 -> 采集章节并解密。

用法：
    python main.py <章节URL> [--manual]

--manual: 启用 GUI 手动确认字库识别（识别率不高时使用）。
"""

import argparse
import sys

from fanqie import CHARMAP_FILE, DATA_DIR, IDENTIFY_IMG_DIR
from fanqie.jpg_to_dic import ocr_images_to_dict, save_charmap
from fanqie.spider import fetch_chapter, load_charmap
from fanqie.woff_to_jpg import woff_to_images


def build_charmap(manual: bool = False) -> None:
    """下载字体后转图片并 OCR，生成字库字典。"""
    woff_files = sorted(DATA_DIR.glob("*.woff2"))
    if not woff_files:
        print("data 目录下没有 woff 字体文件，请先准备字体。")
        return

    woff_to_images(woff_files[-1], IDENTIFY_IMG_DIR)
    results = ocr_images_to_dict(IDENTIFY_IMG_DIR, manual=manual)
    save_charmap(results, CHARMAP_FILE)


def main() -> None:
    parser = argparse.ArgumentParser(description="番茄小说采集工具")
    parser.add_argument("url", nargs="?", help="章节阅读页 URL")
    parser.add_argument("--manual", action="store_true", help="启用 GUI 手动确认字库识别")
    args = parser.parse_args()

    if not args.url:
        parser.print_help()
        sys.exit(1)

    # 若字库尚未生成，先自动生成
    charmap = load_charmap()
    if not charmap:
        print("未找到字库字典，开始自动生成...")
        build_charmap(manual=args.manual)
        charmap = load_charmap()

    if not charmap:
        print("字库生成失败，无法解密章节内容。")
        sys.exit(1)

    article = fetch_chapter(args.url, charmap)
    print(article)


if __name__ == "__main__":
    main()
