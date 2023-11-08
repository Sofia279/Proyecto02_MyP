from PIL import Image
from functools import lru_cache
from pathlib import Path

class CloudImage:
    '''
    Clase que permite convertir imagenes y determinar cobertura de nubes
    '''
    black = (0, 0, 0)
    white = (255, 255, 255)
    pink = (228, 0, 124)

    def __init__(self, path):
        '''
        Constructor de la clase
        Args: Ruta del archivo
        Return: void
        '''
        self.path = path
        self.name = path.stem
        self.suffix = path.suffix
        self._cloud_cov = None

    @property
    def cloud_cov(self):
        '''
        Nos da el valor calculado de la covertura de imagenes y si no se ha calculado
        mediante el filtrado de pixeles y el metodo de convolucion lo calcula
        Return: Valor calculado de la covertura de imagenes
        '''
        if self._cloud_cov is None:
            sky = cloud = 0
            with Image.open(self.path) as image, \
                 Image.open("mask.png") as mask:
                image.paste(CloudImage.pink, mask=mask)
                self.rb_filter(image)
                self.convolution(image)
                width, height = image.size
                px = image.load()
                for x in range(width):
                    for y in range(height):
                        if px[x, y] == CloudImage.pink:
                            continue
                        elif px[x, y] == CloudImage.white:
                            cloud += 1
                        else:
                            sky += 1
                self._cloud_cov = cloud / (cloud + sky)
        return self._cloud_cov

    def write_conv(self):
        '''
        Guarda la imagen procesada en una ruta especifada en el directorio
        output de salida donde lo crea o ya existe
        '''
        with Image.open(self.path) as image, Image.open("mask.png") as mask:
            image.paste(CloudImage.pink, mask=mask)
            self.rb_filter(image)
            self.convolution(image)
            image.paste(CloudImage.black, mask=mask)
            output_dir = Path("output")
            if not output_dir.exists():
                output_dir.mkdir()
            output_file = Path(f"{self.name}-seg{self.suffix}")
            image.save(output_dir / output_file)

    def rb_filter(self, image):
        '''
        Identifica los pixeles relacionados con las nubes, y marca dependiendo
        su caso en rosa, blanco o negro
        Args: Imagen donde se realizan las operaciones
        '''
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
        '''
        Analiza la distribucion de pixeles en una imagen, para determinar que areas
        son del cielo y que areas son de la nube, mediante convolucion
        Args: imagen donde se realizan operaciones de convolucion
        '''
        width, height = image.size
        temp = image.copy()
        px = temp.load()
        pxout = image.load()
        for x in range(width):
            for y in range(height):
                if px[x, y] == CloudImage.pink:
                    continue
                weight = 0
                for i in range(x - 2, x + 3):
                    for j in range(y - 2, y + 3):
                        p = self.cached_access(px, i, j)
                        if p == CloudImage.white:
                            weight += 1
                if weight <= 7:
                    pxout[x, y] = CloudImage.black
                elif weight > 16:
                    pxout[x, y] = CloudImage.white

    @lru_cache(maxsize=12500)
    def cached_access(self, px, x, y):
        '''
        Almacena los pixeles en cache y accesa a ellos
        Args: Pixeles en una imagen en la que se desea accesar
        x,y coordenadas
        Return: pixel dado en la coordenada x,y
        '''
        return px[x, y]