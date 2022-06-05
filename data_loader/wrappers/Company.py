import json

from jsonschema import validate
from jsonschema import ValidationError

from data_loader.wrappers.Wrapper import Wrapper
from data_loader.models import Company


COMPANY_SCHEMA = {
    "type": "object",
    "properties": {
        "index": {"type": "number"},
        "company": {"type": "string", "minLength": 1},
    },
    "required": [
        "index",
        "company",
    ],
}


@Wrapper.register_subclass('companies')
class CompanyWrapper(Wrapper):
    """
    CompanyWrapper class will validate and save companies
    """
    def __init__(self):
        pass

    def handle_record(self, index, record) -> None:
        """
        This function will handle each record in the json file, validate and save the records

        :param index: int
        :param record: json
        :return:
        """
        try:
            # validate the record with the schema above
            validate(instance=record, schema=COMPANY_SCHEMA)

            # check if same person exists to avoid duplicates
            company_exists = Company.objects.filter(index=record['index']).all()
            if company_exists:
                return

            company = Company()
            company.index = record['index']
            company.company = record['company']
            company.save()
        except ValidationError as validation_error:
            print(f"Skipping record number: {index} due to validation error")
        except Exception as e:
            print(e)

    def handle_file_upload(self, file_path) -> None:
        """
        Open the file using the file path, read it as json records and send each record
        to handle_record function
        :param file_path: string
        :return: None
        """
        with open(file_path) as file:
            data = json.load(file)
            for index, record in enumerate(data):
                self.handle_record(index, record)
