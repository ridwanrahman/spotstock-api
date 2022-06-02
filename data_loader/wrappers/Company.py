import json
from pathlib import Path
from data_loader.wrappers.Wrapper import Wrapper
# from ingestion.models import Company
# from ingestion.validator import Validator


@Wrapper.register_subclass('companies')
class CompanyWrapper(Wrapper):
    def __init__(self):
        pass

    # def handle_file_upload(self, file_name):
    #     BASE_DIR = Path(__file__).resolve().parent.parent.parent
    #     FILE_PATH = Path.joinpath(BASE_DIR, f'files/{file_name}')
    #
    #     with open(FILE_PATH) as file:
    #         data = json.load(file)
    #         for index, record in enumerate(data):
    #             try:
    #                 validator = Validator()
    #                 company = Company()
    #
    #                 if_company_exists = Company.objects.filter(index=record['index']).all()
    #                 if if_company_exists:
    #                     continue
    #
    #                 company.index = validator.is_integer(record['index'])
    #                 company.company = validator.is_string(record['company'])
    #                 company.save()
    #             except Exception as e:
    #                 print(f"Data type incorrect, skipping record index: {index}")
