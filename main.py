import argparse
from cloud import CloudImage
import pathlib

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("images", help="archivos de imagenes", nargs='+', type=pathlib.Path)
    parser.add_argument("-s", "-S", "--save", help="escribir archivos procesados con sufijo -seg", action="store_true")
    args = parser.parse_args()
    images = []

for file_path in args.images:
    images.append(CloudImage(str(file_path)))  # Convierte el objeto Path a una cadena de texto

    for img in images:
        if args.save:
            img.rgb_conv()
        print(f"{img.name}: {img.cloud_cov()}")