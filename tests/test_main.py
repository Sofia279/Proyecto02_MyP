import main
import argparse
import pathlib
import unittest
from unittest.mock import patch
from cloud import write_conv
from cloud import cloud_cov
import timeit

class MainTestCase(unittest.TestCase):
    @patch('argparse.ArgumentParser.parse_args',
                return_value=argparse.Namespace(
                    images=[pathlib.Path("tests/test_image.jpg")],
                    save=True
                ))
    def test_args(self, parse_args):
        main.main()
        self.assertTrue(pathlib.Path("output/test_image-seg.jpg").exists())

    def test_formato_incorrecto(self):
        # Prueba el manejo de errores cuando se proporciona una imagen con un formato incorrecto
        imagen_path = '11838.png'  # Cambia la ruta a una imagen con un formato incorrecto
        resultado = write_conv(imagen_path)

        # Verifica que el resultado sea None, lo que indica que se produjo un error
        self.assertIsNone(resultado)

    def test_tiempo_procesamiento(self):
        imagen_path = 'ruta/a/imagen_de_rendimiento.jpg'  # Cambia la ruta a una imagen de rendimiento
        tiempo = timeit.timeit(lambda: write_conv(imagen_path), number=1)

        # Define un límite de tiempo razonable en segundos (
        limite_tiempo = 960.0 #son 16 minutos como limite

        # Verifica que el tiempo de procesamiento no supere el límite definido
        self.assertLessEqual(tiempo,limite_tiempo)
