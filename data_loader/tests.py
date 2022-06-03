from django.test import TestCase

from data_loader.management.commands.load_data import Command


class TestCommand(TestCase):
    def test_wrong_file_name(self):
        command = Command()
        file_name = 'test_file_name'
        response = command.load_file(file_name)
        assert(response == None)
