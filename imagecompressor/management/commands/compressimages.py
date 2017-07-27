import json
import shutil
import uuid
from pathlib import Path

from PIL import Image
from django.conf import settings
from django.core.management.base import BaseCommand

EXTENSION_OPTIONS = {'.jpg': ('optimize', 'quality', 'progressive'),
                     '.jpeg': ('optimize', 'quality', 'progressive'),
                     '.webp': ('lossless',),
                     '.png': ('optimize',)}


class Command(BaseCommand):
    help = 'Compresses images using Pillow'

    def add_arguments(self, parser):
        parser.add_argument('path', nargs='?', default=Path(), help='The path relative to STATIC_ROOT, or app name, whose images you want compressed.')
        parser.add_argument('--optimize', action="store_true", help="If present and true, indicates that the encoder should make an extra pass over the image in order to select optimal encoder settings.")
        parser.add_argument('--quality', type=int, help="The image quality, on a scale from 1 (worst) to 95 (best).")
        parser.add_argument('--progressive', action="store_true", help="If present and true, indicates that this image should be stored as a progressive JPEG file.")
        parser.add_argument('--lossless', action="store_true", help="If present and true, instructs the WEBP writer to use lossless compression.")

    def handle(self, *args, **options):

        STATIC_ROOT = Path(settings.STATIC_ROOT)
        try:
            IMAGE_COMPRESS_ROOT = Path(settings.IMAGE_COMPRESS_ROOT)
        except AttributeError:
            IMAGE_COMPRESS_ROOT = Path('IMAGES')

        staticfiles_manifest_path = STATIC_ROOT / 'staticfiles.json'
        images_directory = STATIC_ROOT / IMAGE_COMPRESS_ROOT
        search_path = STATIC_ROOT / options['path']

        try:
            shutil.rmtree(str(images_directory))
        except FileNotFoundError:
            pass
        images_directory.mkdir()

        with open(staticfiles_manifest_path) as staticfiles_manifest:
            manifest = json.load(staticfiles_manifest)
            for file_key in manifest.get('paths', {}):
                file_path = Path(file_key)
                ext = file_path.suffix.lower()
                if ext in EXTENSION_OPTIONS:
                    original_image_path = STATIC_ROOT / file_path
                    if search_path in original_image_path.parents:

                        self.stdout.write('Processing: %s' % original_image_path)

                        new_image_name = ''.join((str(uuid.uuid4()), ext))
                        relative_new_image_path = IMAGE_COMPRESS_ROOT / new_image_name
                        full_new_image_path = STATIC_ROOT / relative_new_image_path

                        new_image_options = get_image_options(options, ext)
                        if new_image_options:
                            image = Image.open(original_image_path)
                            image.save(full_new_image_path, **new_image_options)
                        else:
                            shutil.copyfile(str(original_image_path), str(full_new_image_path))

                        manifest['paths'][file_key] = str(relative_new_image_path)

        with open(staticfiles_manifest_path, 'w') as staticfiles_manifest:
            json.dump(manifest, staticfiles_manifest)


def get_image_options(options, ext):
    try:
        return dict((k, options[k]) for k in EXTENSION_OPTIONS[ext] if options.get(k))
    except KeyError:
        return {}
