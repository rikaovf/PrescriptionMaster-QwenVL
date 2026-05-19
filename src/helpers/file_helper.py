def is_image(file_path):

    extensoes = (
        '.png',
        '.jpg',
        '.jpeg',
        '.bmp',
        '.tiff'
    )

    return file_path.lower().endswith(extensoes)

def is_pdf(file_path):

    return file_path.lower().endswith('.pdf')