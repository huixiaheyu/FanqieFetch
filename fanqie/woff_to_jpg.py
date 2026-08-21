"""将 woff 字体文件中的每个字形渲染为图片，用于后续 OCR 识别。

番茄小说的反爬字体会把正文里的常用字替换成私有字形，
通过把字体每个字形导出为图片并 OCR 识别，得到 Unicode -> 真实文字 的映射。
"""

import io
from pathlib import Path

from fontTools.ttLib import TTFont
from PIL import Image, ImageDraw, ImageFont

from . import DATA_DIR, IDENTIFY_IMG_DIR


def woff_to_images(
    woff_file: str | Path,
    output_folder: str | Path,
    font_size: int = 120,
    image_size: tuple[int, int] = (224, 224),
) -> int:
    """把 woff 字体中每个字形渲染为图片。

    Args:
        woff_file: woff 字体文件路径。
        output_folder: 输出图片的文件夹。
        font_size: 字形绘制大小。
        image_size: 图片尺寸 (宽, 高)。

    Returns:
        成功导出的图片数量。
    """
    output_folder = Path(output_folder)
    output_folder.mkdir(parents=True, exist_ok=True)

    font = TTFont(str(woff_file))
    cmap = font["cmap"].getcmap(3, 1).cmap  # (PlatformID=3, EncodingID=1): Windows Unicode

    # 通过 BytesIO 加载字形，避免反复写临时 ttf 文件
    ttf_bytes = io.BytesIO()
    font.save(ttf_bytes)
    ttf_bytes.seek(0)
    pil_font = ImageFont.truetype(ttf_bytes, font_size)

    count = 0
    for unicode_val in cmap:
        char = chr(unicode_val)
        img = Image.new("RGB", image_size, "white")
        draw = ImageDraw.Draw(img)

        # 计算居中位置
        bbox = draw.textbbox((0, 0), char, font=pil_font)
        w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
        position = ((image_size[0] - w) // 2, (image_size[1] - h) // 2)
        draw.text(position, char, font=pil_font, fill="black")

        img_path = output_folder / f"{unicode_val}.jpg"
        img.save(img_path)
        count += 1

    print(f"已导出 {count} 张字形图片到 {output_folder}")
    return count


if __name__ == "__main__":
    # 默认使用 data 目录下最新下载的 woff 文件
    woff_files = sorted(DATA_DIR.glob("*.woff2"))
    if not woff_files:
        raise FileNotFoundError(f"{DATA_DIR} 下没有 woff 字体文件，请先下载。")
    _woff_file = woff_files[-1]
    woff_to_images(_woff_file, IDENTIFY_IMG_DIR)
