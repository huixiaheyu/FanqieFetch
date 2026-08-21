"""对字形图片进行 OCR 识别，输出 {unicode值.jpg: 真实文字} 字典。

支持两种模式：
- 全自动：直接使用 ddddocr 识别结果（识别率较高时推荐）。
- 手动确认：每张图弹出 GUI 确认，识别错误的可手动修改（更准确但繁琐）。
"""

from pathlib import Path

import ddddocr
from PIL import Image

from . import CHARMAP_FILE, IDENTIFY_IMG_DIR
from .UI import UI


def ocr_images_to_dict(
    folder_path: str | Path,
    manual: bool = False,
) -> dict[str, str]:
    """识别文件夹下所有图片为文字。

    Args:
        folder_path: 图片所在文件夹。
        manual: 是否启用 GUI 手动确认。默认全自动。

    Returns:
        {文件名: 文字} 字典。
    """
    folder = Path(folder_path)
    results: dict[str, str] = {}
    stop_loop = False
    ocr = ddddocr.DdddOcr()

    for file_path in sorted(folder.iterdir()):
        if stop_loop:
            break
        if not file_path.is_file():
            continue

        with Image.open(file_path) as image:
            ocr_result = ocr.classification(image)

        if manual:
            ui = UI(image, file_path.name, ocr_result, stop_loop)
            right_result = ui.final_result
            stop_loop = ui.stop_loop
        else:
            right_result = ocr_result

        results[file_path.name] = right_result
        print(f"{file_path.name}: {right_result}")

    return results


def save_charmap(results: dict[str, str], output_file: str | Path = CHARMAP_FILE) -> None:
    """保存字库字典到文件。"""
    output_file = Path(output_file)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_text(str(results), encoding="utf-8")
    print(f"字库字典已保存到 {output_file}")


if __name__ == "__main__":
    results = ocr_images_to_dict(IDENTIFY_IMG_DIR)
    save_charmap(results)
