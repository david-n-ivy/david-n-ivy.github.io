import argparse
from copy import copy
import io
import logging
import math
import typing as t

from imgz_cli.cli import upload
from PIL import ImageOps, Image
import yaml


POST_ASPECT_RATIO = 4 / 3

log = logging.getLogger(__name__)


def resize_image(image: Image) -> Image:
    current_ar = image.width / image.height
    if math.isclose(current_ar, POST_ASPECT_RATIO, abs_tol=0.01):
        return image
    return ImageOps.pad(image, size=(int(image.height * POST_ASPECT_RATIO), image.height), color="white")

def make_thumbnail(image):
    image_copy = copy(image)
    image_copy.thumbnail(size=(200 * POST_ASPECT_RATIO, 200))
    return image_copy


def parse_args():
    parser = argparse.ArgumentParser(description="standardize and upload some images")
    parser.add_argument("-f", "--files", help="file to upload", type=str, nargs='+')
    parser.add_argument("-a", "--api-key", help="imgz API key", type=str)
    parser.add_argument("-d", "--dry-run", help="don't actually upload anything", action='store_true')

    return parser.parse_args()


def upload_image(api_key, image):
    f = io.BytesIO()
    image.save(f, format="jpeg")
    return upload(api_key, f.getvalue())["urls"]["image"]

def pprint_yaml(results: t.List[t.Dict]):
    print(yaml.dump(
        {"images": results}
    ))


def main():
    logging.basicConfig(level=logging.INFO)
    args = parse_args()
    results = []
    for file in args.files:
        logging.info("reading: %s", file)
        if not args.dry_run:
            image = Image.open(file)
            resized = resize_image(image)
            try:
                thumbnail = make_thumbnail(resized)
                thumbnail_path = upload_image(args.api_key, thumbnail)
                image_path = upload_image(args.api_key, resized)
                results.append({"caption": "TODO()", "src": image_path, "thumbnail": thumbnail_path})
            except Exception:
                log.exception("error_uploading_image")

    pprint_yaml(results)


if __name__ == "__main__":
    main()


# ['https://imgz.org/i9e8mbVp.jpg', 'https://imgz.org/i3smmaCm.jpg']
