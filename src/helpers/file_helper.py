from pdf2image import convert_from_path
from pathlib import Path

import os

IMAGE_EXTENSIONS = {
    ".png",
    ".jpg",
    ".jpeg",
    ".webp",
    ".bmp",
    ".tiff"
}

PDF_EXTENSIONS = {
    ".pdf"
}



def pdf_to_images(pdf_path: str, output_dir: str):
    pages = convert_from_path(pdf_path)

    image_paths = []

    for index, page in enumerate(pages):
        output_path = os.path.join(
            output_dir,
            f"{Path(pdf_path).stem}_page_{index + 1}.png"
        )

        page.save(output_path, "PNG")
        image_paths.append(output_path)

    return image_paths

def is_hidden_file(filename):

    return filename.startswith(".")

def is_pdf(file_path: str) -> bool:
    return Path(file_path).suffix.lower() in PDF_EXTENSIONS


def is_image(file_path: str) -> bool:
    return Path(file_path).suffix.lower() in IMAGE_EXTENSIONS