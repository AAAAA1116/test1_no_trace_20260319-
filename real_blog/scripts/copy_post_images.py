"""
把「新建文件夹」里的图片按顺序复制到 content/posts/做网站教程/
并重命名为 1.png, 2.png, ...
顺序：640.png → 1.png，然后 640 (1).png → 2.png，640 (2).png → 3.png …
"""
import re
from pathlib import Path

SRC = Path(__file__).parent.parent / "新建文件夹"
DST = Path(__file__).parent.parent / "content" / "posts" / "做网站教程"
EXT = {".png", ".jpg", ".jpeg", ".gif", ".webp"}

def _sort_key(f: Path) -> tuple:
    """640.png 排第一，然后 640 (1), 640 (2), ..."""
    name = f.stem  # 不含扩展名
    m = re.match(r"640\s*\(\s*(\d+)\s*\)", name)
    if m:
        return (1, int(m.group(1)))
    if name.strip() == "640":
        return (0, 0)
    return (2, name)

def main():
    if not SRC.exists():
        print(f"源文件夹不存在: {SRC}")
        return
    DST.mkdir(parents=True, exist_ok=True)
    files = [f for f in SRC.iterdir() if f.is_file() and f.suffix.lower() in EXT]
    images = sorted(files, key=_sort_key)
    if not images:
        print(f"在 {SRC} 里没有找到图片（支持 .png .jpg .gif .webp）")
        print("请先把对应这篇博客的图片放进「新建文件夹」，再运行本脚本。")
        return
    for i, f in enumerate(images, 1):
        dest = DST / f"{i}.png"
        if f.suffix.lower() != ".png":
            dest = DST / f"{i}{f.suffix}"
        import shutil
        shutil.copy2(f, dest)
        print(f"  {f.name} -> {dest.name}")
    print(f"已复制 {len(images)} 张到 {DST}")

if __name__ == "__main__":
    main()
