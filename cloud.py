from PIL import Image
from pathlib import Path


class CloudImage:
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
        pass

    def convolution(self, image):
        pass
