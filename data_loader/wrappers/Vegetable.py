import json
from jsonschema import validate
from jsonschema import ValidationError
from data_loader.wrappers.Wrapper import Wrapper
from data_loader.models import Vegetable


VEGETABLE_SCHEMA = {
    "type": "object",
    "properties": {
        "name": {"type": "string", "minLength": 1},
    },
    "required": [
        "name",
    ],
}


@Wrapper.register_subclass('vegetables')
class VegetableWrapper(Wrapper):
    def __init__(self):
        pass

    def handle_record(self, index, record):
        try:
            validate(instance=record, schema=VEGETABLE_SCHEMA)

            if_vegetable_exists = Vegetable.objects.filter(vegetable_name=record['name']).all()
            if if_vegetable_exists:
                return

            vegetable = Vegetable()
            vegetable.vegetable_name = record['name']
            vegetable.save()
        except ValidationError as validation_error:
            print(f"Skipping record number: {index} due to validation error")
        except Exception as e:
            print(e)

    def handle_file_upload(self, file_path):

        with open(file_path) as file:
            data = json.load(file)
            for index, record in enumerate(data):
                self.handle_record(index, record)
