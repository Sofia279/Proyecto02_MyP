from PIL import Image
from functools import lru_cache
from pathlib import Path


class CloudImage:
    black = (0, 0, 0)
    white = (255, 255, 255)
    pink = (228, 0, 124)

    def __init__(self, path):
        self.path = path
        self.name = path.stem
        self.suffix = path.suffix
        if not self.suffix in [".jpg", ".jpeg"]:
            raise(Exception("Necesita un archivo .jpg"))
        self._cloud_cov = None

    @property
    def cloud_cov(self):
        if self._cloud_cov is None:
            with Image.open(self.path) as image, \
                 Image.open("mask.png") as mask:
                image.paste(CloudImage.pink, mask=mask)
                self.rb_filter(image)
                self.convolution(image)
        return self._cloud_cov

    def write_conv(self):
        with Image.open(self.path) as image, Image.open("mask.png") as mask:
            image.paste(CloudImage.pink, mask=mask)
            self.rb_filter(image)
            self.convolution(image)
            output_dir = Path("output")
            if not output_dir.exists():
                output_dir.mkdir()
            output_file = Path(f"{self.name}-seg{self.suffix}")
            image.save(output_dir / output_file)

    def rb_filter(self, image):
        width, height = image.size
        px = image.load()
        for x in range(width):
            for y in range(height):
                if (pixel := px[x, y]) == CloudImage.pink:
                    continue
                r, g, b = pixel
                if b == 0 or r / b >= 0.95:
                    px[x, y] = CloudImage.white
                else:
                    px[x, y] = CloudImage.black

    def convolution(self, image):
        width, height = image.size
        temp = image.copy()
        px = temp.load()
        pxout = image.load()
        sky = cloud = 0
        for x in range(width):
            for y in range(height):
                if px[x, y] == CloudImage.pink:
                    pxout[x, y] = CloudImage.black
                    continue
                weight = 0
                for i in range(x - 2, x + 3):
                    for j in range(y - 2, y + 3):
                        p = self.cached_access(px, i, j)
                        if p == CloudImage.white:
                            weight += 1
                if weight <= 7:
                    pxout[x, y] = CloudImage.black
                    sky += 1
                elif weight > 16:
                    pxout[x, y] = CloudImage.white
                    cloud += 1
                elif pxout[x, y] == CloudImage.white:
                    cloud += 1
                else:
                    sky += 1
        self._cloud_cov = cloud / (cloud + sky)

    @lru_cache(maxsize=12500)
    def cached_access(self, px, x, y):
        return px[x, y]
