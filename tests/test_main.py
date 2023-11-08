import main
import argparse
import pathlib
import unittest
from unittest.mock import patch
from cloud import CloudImage
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
        """Prueba el manejo de errores cuando se proporciona una imagen con un
        formato incorrecto.
        """

        # Verifica que la operación lanze una excepción
        self.assertRaises(Exception, lambda: CloudImage(
            pathlib.Path('tests/bad_format.png')))

    def test_tiempo_procesamiento(self):
        image = CloudImage(pathlib.Path('tests/test_image.jpg'))
        tiempo = timeit.timeit(lambda: image.write_conv(), number=1)

        # Define un límite de tiempo razonable en segundos (
        limite_tiempo = 960.0 # 16 minutos como limite

        # Verifica que el tiempo de procesamiento no supere el límite definido
        self.assertLessEqual(tiempo,limite_tiempo)
