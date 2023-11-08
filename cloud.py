from PIL import Image
from pathlib import Path


class CloudImage:
    black = (0, 0, 0)
    white = (255, 255, 255)
    pink = (228, 0, 124)

    def __init__(self, path):
        self.path = path
        self.name = path.stem
        self.suffix = path.suffix
        self._cloud_cov = None

    @property
    def cloud_cov(self):
        if self._cloud_cov is None:
            pass
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
                if b == 0 or r / b  >= 0.95:
                    px[x, y] = CloudImage.white
                else:
                    px[x, y] = CloudImage.black

    def convolution(self, image):
        pass
