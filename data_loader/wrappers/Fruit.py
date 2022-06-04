import json
from jsonschema import validate
from jsonschema import ValidationError
from data_loader.wrappers.Wrapper import Wrapper
from data_loader.models import Fruit


FRUIT_SCHEMA = {
    "type": "object",
    "properties": {
        "name": {"type": "string", "minLength": 1},
    },
    "required": [
        "name",
    ],
}


@Wrapper.register_subclass('fruits')
class FruitWrapper(Wrapper):
    def __init__(self):
        pass

    def handle_record(self, index, record):
        try:
            validate(instance=record, schema=FRUIT_SCHEMA)

            if_fruit_exists = Fruit.objects.filter(fruit_name=record['name']).all()
            if if_fruit_exists:
                return

            fruit = Fruit()
            fruit.fruit_name = record['name']
            fruit.save()
        except ValidationError as validation_error:
            print(f"Skipping record number: {index} due to validation error")
        except Exception as e:
            print(e)

    def handle_file_upload(self, file_path):

        with open(file_path) as file:
            data = json.load(file)
            for index, record in enumerate(data):
                self.handle_record(index, record)
