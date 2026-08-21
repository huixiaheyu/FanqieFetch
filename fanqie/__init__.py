"""番茄小说采集工具核心包。

提供统一的路径定位，脚本不再依赖运行目录，
资源（data/）与产物（output/）均相对包所在的项目根定位。
"""

from pathlib import Path

# 项目根目录：fanqie/__init__.py 的上级目录
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# 数据目录：存放 woff 字体文件
DATA_DIR = PROJECT_ROOT / "data"

# 输出目录：存放识别图片与字库字典
OUTPUT_DIR = PROJECT_ROOT / "output"
IDENTIFY_IMG_DIR = OUTPUT_DIR / "wait_for_identify_images"
CHARMAP_FILE = OUTPUT_DIR / "charmap_dic.txt"

__all__ = [
    "PROJECT_ROOT",
    "DATA_DIR",
    "OUTPUT_DIR",
    "IDENTIFY_IMG_DIR",
    "CHARMAP_FILE",
]
