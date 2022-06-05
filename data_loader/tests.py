from django.test import TestCase

from unittest.mock import patch

from jsonschema import ValidationError

from data_loader.management.commands.load_data import Command
from data_loader.wrappers.Wrapper import Wrapper
from data_loader.models import Company


class TestDataLoaderCommand(TestCase):
    """
    The data loader command is tested here
    """
    def test_wrong_file_name(self):
        command = Command()
        file_name = 'test_file_name'
        response = command.load_file(file_name)
        assert(response is None)

    def test_correct_file_name(self):
        # create a json file with one record. Keep names like either companies/people/fruits/vegetables.json
        # same as the wrappers
        # initialize the wrapper class, which should load up all the wrappers
        # filename = companies.json
        # send the file name to wrapper.create(filenmae)
        # this should load the file and save the record
        # assert no exceptions
        pass


class TestWrappersValidation(TestCase):
    """
    This class checks for both positive and negative validation for each model like Companies, People, fruits and veges.

    It sends a valid record which is saved to database, then queried and asserted with the records of the sample data
    to assert positive

    For negative validation, try saving an invalid record, which should print a message, that is asserted
    """
    def test_company_positive_validation(self):
        test_wrapper = Wrapper()
        test = test_wrapper.create('companies')
        index = 1
        record = {
            "index": 10,
            "company": "TEST_COMPANY"
        }
        response = test.handle_record(index, record)
        company = Company.objects.filter(index=record['index']).first()
        assert(company.company == record['company'])

    @patch('builtins.print')
    def test_company_negative_validation(self, mock_print):
        test_wrapper = Wrapper()
        test = test_wrapper.create('companies')
        index = 1
        record = {
            "index": 10,
            "company": 34
        }
        response = test.handle_record(index, record)

        mock_print.assert_called_with(f'Skipping record number: {index} due to validation error')
        print("hejrer")

    # same validation logic for other table like people, fruits, vegetables
