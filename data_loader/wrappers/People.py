import json

from jsonschema import validate
from jsonschema import ValidationError

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
    """
    PeopleWrapper class will validate and save people.

    For each people record, additional data includes the people a person is friend with and their favorite food.
    The people a person is friends with is stored in a list for each person then saved after all the people are
    saved.
    """
    def __init__(self):
        self.friends = []
        self.food = []
        self.fruit = Fruit()
        self.vegetable = Vegetable()

    def friend_extractor(self, person: Person, friends: list) -> None:
        """
        Creates a friend_obj dict containing the person id and their friends (index).
        This will be used to save the friends to PersonFriend table.

        :param person: Person object
        :param friends: list
        :return: None
        """
        friend_obj = {
            'person_id': person.id,
            'friends': friends
        }
        self.friends.append(friend_obj)

    def favorite_food_extractor(self, person: Person, food: list) -> None:
        """
        Checks if the fruit or vegetable exists then adds it to the PersonFruit/PersonVegetable
        table accordingly

        :param person: Person object
        :param food: list
        :return: None
        """
        for item in food:
            is_fruit = Fruit.objects.filter(fruit_name=item).first()
            if is_fruit:
                is_fruit.person.add(person)
                continue

            is_vegetable = Vegetable.objects.filter(vegetable_name=item).first()
            if is_vegetable:
                is_vegetable.person.add(person)
                continue

    def friends_fillup(self) -> None:
        """
        Adds the person's friend to the PersonFriend table with the person_id and
        the friend_id which is essentially another person_id

        :return: None
        """
        for friend_record in self.friends:
            person = Person.objects.get(id=friend_record['person_id'])
            for friend in friend_record['friends']:
                person_friend = PersonFriend()
                if friend['index'] == person.index:
                    continue
                person_friend.person_id = person
                person_friend.friend_id = Person.objects.get(index=friend['index'])
                person_friend.save()

    def assign_company(self, company_index) -> Company:
        """
        Returns if the company exits using the company_index. Otherwise returns None
        so the record does not contain a company_id

        :param company_index: int
        :return: Company object
        """
        try:
            company = Company.objects.get(index=company_index)
            if company:
                return company
        except Exception as e:
            print(f"Company with company index: {company_index} doesnt exist")
            return None

    def handle_record(self, index, record) -> None:
        """
        This function will handle each record in the json file, validate and save the records.

        It will store the friends of each person record in a list

        :param index: int
        :param record: json
        :return: None
        """
        try:
            # validate the record with the schema above
            validate(instance=record, schema=PERSON_SCHEMA)

            # check if same person exists to avoid duplicates
            guid_exists = Person.objects.filter(guid=(record['guid'])).all()
            if guid_exists:
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
            # add the friends of a person to a different list
            self.friend_extractor(person, record['friends'])

            self.favorite_food_extractor(person, record['favouriteFood'])
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

            # Fill up the friends table for each person record
            self.friends_fillup()
