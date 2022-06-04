import json
from jsonschema import validate
from jsonschema import ValidationError
from pathlib import Path
from data_loader.wrappers.Wrapper import Wrapper
from data_loader.models import Person, Fruit, Vegetable, Company, PersonFriend

PERSON_SCHEMA = {
    "type": "object",
    "properties": {
        "index": {"type": "number"},
        "guid": {"type": "string", "minLength": 1},
        "name": {"type": "string"},
        "age": {"type": "number"},
        "address": {"type": "string"},
        "phone": {"type": "string"},
        "eyeColor": {"type": "string"},
        "has_died": {"type": "boolean"},
        "company_id": {"type": "number"},
        "friends": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "index": {"type": "number"}
                }
            }
        },
        "favouriteFood": {
            "type": "array",
            "items": {
                "type": "string",
            }
        }
    },
    "required": [
        "index",
        "guid",
        "name",
        "age",
        "address",
        "phone",
        "eyeColor",
        "has_died",
        "company_id",
        "friends",
        "favouriteFood"
    ],
}


@Wrapper.register_subclass('people')
class PeopleWrapper(Wrapper):
    def __init__(self):
        self.friends = []
        self.food = []
        self.fruit = Fruit()
        self.vegetable = Vegetable()

    def friend_extractor(self, person, friends):
        friend_obj = {
            'person_id': person.id,
            'friends': friends
        }
        self.friends.append(friend_obj)

    def favorite_food_extractor(self, person, food):
        for item in food:
            is_fruit = Fruit.objects.filter(fruit_name=item).first()
            if is_fruit:
                is_fruit.person.add(person)
                continue

            is_vegetable = Vegetable.objects.filter(vegetable_name=item).first()
            if is_vegetable:
                is_vegetable.person.add(person)
                continue

    def friends_fillup(self):
        for friend_record in self.friends:
            person = Person.objects.get(id=friend_record['person_id'])
            for friend in friend_record['friends']:
                person_friend = PersonFriend()
                if friend['index'] == person.index:
                    continue
                person_friend.person_id = person
                person_friend.friend_id = Person.objects.get(index=friend['index'])
                person_friend.save()

    def assign_company(self, company_id):
        try:
            company_exists = Company.objects.get(index=company_id)
            if company_exists:
                return company_exists
        except Exception as e:
            print(f"Company with company id: {company_id} doesnt exist")
            return None

    def handle_record(self, index, record):
        try:
            validate(instance=record, schema=PERSON_SCHEMA)

            if_guid_exists = Person.objects.filter(guid=(record['guid'])).all()
            if if_guid_exists:
                return
            person = Person()
            person.index = record['index']
            person.guid = record['guid']
            person.name = record['name']
            person.age = record['age']
            person.address = record['address']
            person.phone = record['phone']
            person.eye_color = record['eyeColor']
            person.has_died = record['has_died']
            person.company_id = self.assign_company(record['company_id'])
            person.save()
            self.friend_extractor(person, record['friends'])
            self.favorite_food_extractor(person, record['favouriteFood'])
        except ValidationError as validation_error:
            print(f"Skipping record number: {index} due to validation error")
        except Exception as e:
            print(e)

    def handle_file_upload(self, file_path):
        with open(file_path) as file:
            data = json.load(file)
            for index, record in enumerate(data):
                self.handle_record(index, record)

            # Fill up the friends table for each person record
            self.friends_fillup()

# if __name__ == '__main__':
