import json

from easy_thumbnails.files import get_thumbnailer
import filer
from filer.models import Image, Folder


def get_thumbnail(obj, width=492, height=1000, crop=False):
    options = {
        'size': (width, height),
        'crop': crop,
        'quality': 60,
    }
    thumbnailer = get_thumbnailer(obj)
    return thumbnailer.get_thumbnail(options).url


def gallery_dir(cols, path):
    files = []
    width = (1120 / int(cols)) * 2
    try:
        parent = None
        for component in path.split('/'):
            parent = Folder.objects.get(name=component, parent=parent)

        images = []
        for file in sorted(parent.files):
            images.append(
                '<a href="{}"><img src="{}" /></a>'.format(file.url, get_thumbnail(file, width, 999999))
            )
    except filer.models.foldermodels.Folder.DoesNotExist:
        pass
    return '<ul class="gallery gallery-{}-cols">{}</ul>'.format(cols, ''.join(images))
