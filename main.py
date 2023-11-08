import argparse
from cloud import CloudImage
import pathlib

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("images", help="archivos de imagenes",
                        nargs='+', type=pathlib.Path)
    parser.add_argument("-s", "-S", "--save",
                        help="escribir archivos procesados con sufijo -seg",
                        action="store_true")
    args = parser.parse_args()

    for fname in args.images:
        if not fname.exists():
            print(f"No se encontró el archivo {fname}")
            continue
        img = CloudImage(fname)
        if args.save:
            img.write_conv()
        print(f"{img.name}: {img.cloud_cov}")
if __name__ == "__main__":
    main()
    
