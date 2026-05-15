import unittest
from io import BytesIO
from app import app


class TestMostCommonWordApp(unittest.TestCase):

    def setUp(self):
        """Подготовка к тестированию"""
        self.app = app.test_client()
        self.app.testing = True

    def test_most_common_word(self):
        """Тест: поиск самого частого слова в файле"""
        data = {
            'file': (
                BytesIO('кот собака кот дом кот'.encode('utf-8')),
                'test.txt'
            )
        }

        response = self.app.post(
            '/',
            data=data,
            content_type='multipart/form-data'
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn('кот'.encode('utf-8'), response.data)
        self.assertIn('3'.encode('utf-8'), response.data)

    def test_words_with_different_case(self):
        """Тест: слова с разным регистром считаются одинаковыми"""
        data = {
            'file': (
                BytesIO('Python python PYTHON flask'.encode('utf-8')),
                'test.txt'
            )
        }

        response = self.app.post(
            '/',
            data=data,
            content_type='multipart/form-data'
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn('python'.encode('utf-8'), response.data)
        self.assertIn('3'.encode('utf-8'), response.data)

    def test_text_with_punctuation(self):
        """Тест: знаки препинания не считаются словами"""
        data = {
            'file': (
                BytesIO('дом, дом! дом? кот.'.encode('utf-8')),
                'test.txt'
            )
        }

        response = self.app.post(
            '/',
            data=data,
            content_type='multipart/form-data'
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn('дом'.encode('utf-8'), response.data)
        self.assertIn('3'.encode('utf-8'), response.data)

    def test_several_same_frequency_words(self):
        """Тест: несколько слов встречаются одинаковое количество раз"""
        data = {
            'file': (
                BytesIO('кот кот собака собака дом'.encode('utf-8')),
                'test.txt'
            )
        }

        response = self.app.post(
            '/',
            data=data,
            content_type='multipart/form-data'
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn('кот'.encode('utf-8'), response.data)
        self.assertIn('собака'.encode('utf-8'), response.data)
        self.assertIn('2'.encode('utf-8'), response.data)

    def test_wrong_file_format(self):
        """Тест: загрузка файла неверного формата"""
        data = {
            'file': (
                BytesIO('кот собака кот'.encode('utf-8')),
                'test.docx'
            )
        }

        response = self.app.post(
            '/',
            data=data,
            content_type='multipart/form-data'
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn('Можно загружать только файлы .txt'.encode('utf-8'), response.data)
        self.assertIn('0'.encode('utf-8'), response.data)

    def test_no_words_in_file(self):
        """Тест: если в файле нет слов"""
        data = {
            'file': (
                BytesIO('... !!! 12345'.encode('utf-8')),
                'test.txt'
            )
        }

        response = self.app.post(
            '/',
            data=data,
            content_type='multipart/form-data'
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn('Слова не найдены'.encode('utf-8'), response.data)
        self.assertIn('0'.encode('utf-8'), response.data)

    def test_empty_file(self):
        """Тест: пустой файл"""
        data = {
            'file': (
                BytesIO(''.encode('utf-8')),
                'empty.txt'
            )
        }

        response = self.app.post(
            '/',
            data=data,
            content_type='multipart/form-data'
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn('Слова не найдены'.encode('utf-8'), response.data)
        self.assertIn('0'.encode('utf-8'), response.data)


if __name__ == '__main__':
    unittest.main()