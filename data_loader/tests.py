from django.test import TestCase

from data_loader.management.commands.load_data import Command


class TestDataLoaderCommand(TestCase):
    def test_wrong_file_name(self):

        command = Command()
        file_name = 'test_file_name'
        response = command.load_file(file_name)
        assert(response is None)

    def test_correct_file_name(self):
        command = Command()
        file_name = 'companies.json'
        response = command.load_file(file_name)
        # TODO:finish this test, assert with response data or something
        assert (response is not None)
