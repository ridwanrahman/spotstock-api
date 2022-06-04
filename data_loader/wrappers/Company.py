import json
from pathlib import Path
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
    def __init__(self):
        pass

    def handle_record(self, index, record):
        try:
            validate(instance=record, schema=COMPANY_SCHEMA)

            if_company_exists = Company.objects.filter(index=record['index']).all()
            if if_company_exists:
                return

            company = Company()
            company.index = record['index']
            company.company = record['company']
            company.save()
        except ValidationError as validation_error:
            print(f"Skipping record number: {index} due to validation error")
        except Exception as e:
            print(e)

    def handle_file_upload(self, file_path):

        with open(file_path) as file:
            data = json.load(file)
            for index, record in enumerate(data):
                self.handle_record(index, record)
