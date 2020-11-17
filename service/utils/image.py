from io import BytesIO

from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile


def make_thumbnail(size, image, name):
    f = BytesIO()
    image.thumbnail(size, Image.ANTIALIAS)
    image.format = image.format or 'JPEG'
    image.save(f, format=image.format)
    f.seek(0)
    return InMemoryUploadedFile(f, 'ImageField', name, f'image/{image.format.lower()}', f.__sizeof__(), None)


def rotate(image):
    try:
        exif = image._getexif()
    except:
        return image
    if not exif:
        return image
    exif = dict(exif.items())
    orientation = 274

    if not exif.get(orientation):
        return image

    if exif[orientation] == 3:
        image = image.rotate(180, expand=True)
    elif exif[orientation] == 6:
        image = image.rotate(270, expand=True)
    elif exif[orientation] == 8:
        image = image.rotate(90, expand=True)
    return image

