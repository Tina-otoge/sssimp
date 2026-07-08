from dataclasses import dataclass

from PIL import Image

import sssimp

IMAGE_DIR = sssimp.INPUT_DIR / "images"

SIZE_BY_TYPE = {
    "thumb": 128,
    "small": 256,
    "medium": 512,
    "large": 1024,
}


@dataclass
class Size:
    x: int | None
    y: int | None


def get_max_size(size_name: str) -> Size:
    if size_name in SIZE_BY_TYPE:
        return Size(SIZE_BY_TYPE[size_name], SIZE_BY_TYPE[size_name])
    values = size_name.split("x")
    if len(values) != 2:
        raise ValueError(
            f"Invalid size definition {size_name}, expected format: [width]x[height]"
        )
    try:
        for i in range(2):
            if values[i]:
                values[i] = int(values[i])
    except ValueError as e:
        raise ValueError(
            f"Invalid size definition {size_name}, could not read as integers: {e}"
        )
    return Size(x=values[0] or None, y=values[1] or None)


def get_target_size(size: Size, width: int, height: int) -> tuple[int, int]:
    if size.x and size.y:
        # fit within the box while preserving the aspect ratio
        scale = min(size.x / width, size.y / height)
    elif size.x:
        scale = size.x / width
    elif size.y:
        scale = size.y / height
    else:
        scale = 1
    return round(width * scale), round(height * scale)


def main():
    for file in IMAGE_DIR.glob("**/*"):
        if not file.is_file():
            continue
        name, ext = file.stem, file.suffix
        name, size_definitions = name.split("@", 1)
        if not size_definitions:
            raise ValueError(
                f"Invalid image filename {file}, expected format: <name>@<size1>[,size2,...sizeN].<ext>"
            )
        for size_definition in size_definitions.split(","):
            size = get_max_size(size_definition)
            target = (
                sssimp.OUTPUT_DIR / "images" / f"{name}@{size_definition}{ext}"
            )
            target.parent.mkdir(parents=True, exist_ok=True)
            sssimp.logger.info(
                f"Resizing {file} -> {target} ({size.x}x{size.y})"
            )
            with Image.open(file) as img:
                x, y = get_target_size(size, img.width, img.height)
                img.resize((x, y)).save(target)
