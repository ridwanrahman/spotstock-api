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
    """
    FruitWrapper class will validate and save fruits
    """
    def __init__(self):
        pass

    def handle_record(self, index, record) -> None:
        """
         This function will handle each record in the json file, validate and save the records

        :param index: int
        :param record: json
        :return: None
        """
        try:
            validate(instance=record, schema=FRUIT_SCHEMA)

            fruit_exists = Fruit.objects.filter(fruit_name=record['name']).all()
            if fruit_exists:
                return

            fruit = Fruit()
            fruit.fruit_name = record['name']
            fruit.save()
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
