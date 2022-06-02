from django.test import TestCase

from data_loader.management.commands.load_data import Command


class TestCommand(TestCase):
    def test_wrong_file_name(self):
        with self.assertRaises(FileNotFoundError):
            command = Command()
            file_name = 'test_file_name'
            command.load_file(file_name)
