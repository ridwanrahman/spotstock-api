import json
from django.test import TestCase

from rest_framework.test import APITestCase
from rest_framework.test import APIRequestFactory

from data_loader.models import Company, Person, Fruit, Vegetable
from data_loader.wrappers.Wrapper import Wrapper

from api.endpoints.feature_endpoints import AllCompanyEmployees, CommonPeople, FavoriteFruitsVeges

from django.urls import reverse


class TestAPI(APITestCase):
    """
    Test the individual APIs
    """
    def setUp(self) -> None:
        self.company = Company.objects.create(
            index=10,
            company='test company'
        )
        self.person = Person.objects.create(
            index=100,
            guid='test',
            name='test',
            age=50,
            address='test',
            phone='test',
            eye_color='test',
            has_died=True,
            company_id=self.company
        )

    def test_get_company_employees_api(self):
        url = reverse("all_company_employees", kwargs={"company_index": self.company.index})
        response = self.client.get(url)
        resp_json = json.loads(response.content)
        assert (resp_json[0]['name'] == self.person.name)

    def test_post_company_employees_api(self):
        """
        Since only get request is allowed, this will return 'Method not allowed' error which is 405
        """
        url = reverse("all_company_employees", kwargs={"company_index": self.company.index})
        response = self.client.post(url)
        assert (response.status_code == 405)

    def test_common_people_api(self):
        # Create people with their friends,
        # Make at least one friend have brown eyes and alive
        # This should return the common friend
        # A similar test is given below
        pass

    def test_person_liked_fruits_veges_api(self):
        # create person with favorite food including fruits and veges
        # get it using this api then assert
        # similar test is provided below
        pass


class TestAllCompanyEmployees(TestCase):

    def test_no_company_employees(self):
        """
        Test to determine no employees exist for a random company_index
        """
        random_company_index = 19
        question_one = AllCompanyEmployees()
        response = question_one.get_response(random_company_index)
        resp_json = json.loads(json.dumps(response))
        assert (resp_json['response'] == f'No employees found for company index: {random_company_index}')

    def test_all_company_employees(self):
        """
        Test to determine if company has employee
        """
        # add a company
        company = Company(
            index=-10,
            company='test company'
        )
        company.save()

        # add second company
        company2 = Company(
            index=-20,
            company='second test company'
        )
        company2.save()

        # add person and relate it to company
        person = Person(
            index=-10,
            guid='test',
            name='test',
            age=50,
            address='test',
            phone='test',
            eye_color='test',
            has_died=True,
            company_id=company
        )
        person.save()

        # assert the first user was added to first company
        question_one = AllCompanyEmployees()
        response = question_one.get_response(company.index)
        resp_json = json.loads(json.dumps(response))
        assert (resp_json[0]['name'] == 'test')


class TestCommonPeople(TestCase):

    def test_person_doest_exist(self):
        """
        Add people then query by a wrong person_index to see person does not exist
        """
        company = Company(
            index=-10,
            company='test company'
        )
        company.save()

        wrapper = Wrapper()
        file_wrapper = wrapper.create('people')
        records = [
            {
                "index": 0,
                "guid": "5e71dc5d-61c0-4f3b-8b92-d77310c7fa43",
                "has_died": True,
                "age": 61,
                "eyeColor": "blue",
                "name": "TEST USER_1",
                "company_id": company.index,
                "email": "carmellalambert@earthmark.com",
                "phone": "+1 (910) 567-3630",
                "address": "628 Sumner Place, Sperryville, American Samoa, 9819",
                "friends": [
                    {
                        "index": 1
                    }
                ],
                "favouriteFood": [],
            },
            {
                "index": 1,
                "guid": "5e71dc5d-61c0-4f3b-8b92-d77310fa43",
                "has_died": True,
                "age": 61,
                "eyeColor": "brown",
                "name": "TEST USER_2",
                "company_id": company.index,
                "email": "carmellalambert@earthmark.com",
                "phone": "+1 (910) 567-3630",
                "address": "628 Sumner Place, Sperryville, American Samoa, 9819",
                "friends": [
                    {
                        "index": 0
                    }
                ],
                "favouriteFood": [],
            },
        ]
        for index, record in enumerate(records):
            file_wrapper.handle_record(index, record)
        file_wrapper.friends_fillup()

        test_common_peopple = CommonPeople()
        response = test_common_peopple.get_response(0, 3)
        assert (response['error'] == 'person does not exist')

    def test_common_people(self):
        """
        Add people then use business logic to see if the right common friend is returned with brown eyes
        and is alive.
        """
        company = Company(
            index=-10,
            company='test company'
        )
        company.save()

        wrapper = Wrapper()
        file_wrapper = wrapper.create('people')

        # record contains 4 people, all friends with each other
        # and two have brown eyes (index=1, index=3)
        # person index 0 & 2 should return person index 3 who has brown eye
        records = [
            {
                "_id": "595eeb9b96d80a5bc7afb106",
                "index": 0,
                "guid": "5e71dc5d-61c0-4f3b-8b92-d77310c7fa43",
                "has_died": True,
                "balance": "$2,418.59",
                "picture": "http://placehold.it/32x32",
                "age": 61,
                "eyeColor": "blue",
                "name": "Carmella Lambert",
                "gender": "female",
                "company_id": 58,
                "email": "carmellalambert@earthmark.com",
                "phone": "+1 (910) 567-3630",
                "address": "628 Sumner Place, Sperryville, American Samoa, 9819",
                "about": "Non duis dolore ad enim. Est id reprehenderit cupidatat tempor excepteur. Cupidatat labore incididunt nostrud exercitation ullamco reprehenderit dolor eiusmod sit exercitation est. Voluptate consectetur est fugiat magna do laborum sit officia aliqua magna sunt. Culpa labore dolore reprehenderit sunt qui tempor minim sint tempor in ex. Ipsum aliquip ex cillum voluptate culpa qui ullamco exercitation tempor do do non ea sit. Occaecat laboris id occaecat incididunt non cupidatat sit et aliquip.\r\n",
                "registered": "2016-07-13T12:29:07 -10:00",
                "tags": [
                    "id",
                    "quis",
                    "ullamco",
                    "consequat",
                    "laborum",
                    "sint",
                    "velit"
                ],
                "friends": [
                    {
                        "index": 0
                    },
                    {
                        "index": 1
                    },
                    {
                        "index": 2
                    }
                ],
                "greeting": "Hello, Carmella Lambert! You have 6 unread messages.",
                "favouriteFood": [
                    "orange",
                    "apple",
                    "banana",
                    "strawberry"
                ]
            },
            {
                "_id": "595eeb9b1e0d8942524c98ad",
                "index": 1,
                "guid": "b057bb65-e335-450e-b6d2-d4cc859ff6cc",
                "has_died": False,
                "balance": "$1,562.58",
                "picture": "http://placehold.it/32x32",
                "age": 60,
                "eyeColor": "brown",
                "name": "Decker Mckenzie",
                "gender": "male",
                "company_id": 98,
                "email": "deckermckenzie@earthmark.com",
                "phone": "+1 (893) 587-3311",
                "address": "492 Stockton Street, Lawrence, Guam, 4854",
                "about": "Consectetur aute consectetur dolor aliquip dolor sit id. Sint consequat anim occaecat ad mollit aliquip ut aute eu culpa mollit qui proident eu. Consectetur ea et sit exercitation aliquip officia ea aute exercitation nulla qui sunt labore. Enim veniam labore do irure laborum aute exercitation consectetur. Voluptate adipisicing velit sunt consectetur id sint adipisicing elit elit pariatur officia amet officia et.\r\n",
                "registered": "2017-06-25T10:03:49 -10:00",
                "tags": [
                    "veniam",
                    "irure",
                    "mollit",
                    "sunt",
                    "amet",
                    "fugiat",
                    "ex"
                ],
                "friends": [
                    {
                        "index": 0
                    },
                    {
                        "index": 1
                    },
                    {
                        "index": 2
                    }
                ],
                "greeting": "Hello, Decker Mckenzie! You have 2 unread messages.",
                "favouriteFood": [
                    "cucumber",
                    "beetroot",
                    "carrot",
                    "celery"
                ]
            },
            {
                "_id": "595eeb9bb3821d9982ea44f9",
                "index": 2,
                "guid": "49c04b8d-0a96-4319-b310-d6aa8269adca",
                "has_died": False,
                "balance": "$2,119.44",
                "picture": "http://placehold.it/32x32",
                "age": 54,
                "eyeColor": "blue",
                "name": "Bonnie Bass",
                "gender": "female",
                "company_id": 59,
                "email": "bonniebass@earthmark.com",
                "phone": "+1 (823) 428-3710",
                "address": "455 Dictum Court, Nadine, Mississippi, 6499",
                "about": "Non voluptate reprehenderit ad elit veniam nulla ut ea ex. Excepteur exercitation aliquip Lorem nisi duis. Ex cillum commodo labore sint non velit aliquip cupidatat sint. Consequat est sint do in eiusmod minim exercitation do consectetur incididunt culpa deserunt. Labore veniam elit duis minim magna et laboris sit labore eu velit cupidatat cillum cillum.\r\n",
                "registered": "2017-06-08T04:23:18 -10:00",
                "tags": [
                    "quis",
                    "sunt",
                    "sit",
                    "aliquip",
                    "pariatur",
                    "quis",
                    "nulla"
                ],
                "friends": [
                    {
                        "index": 0
                    },
                    {
                        "index": 1
                    },
                    {
                        "index": 2
                    }
                ],
                "greeting": "Hello, Bonnie Bass! You have 10 unread messages.",
                "favouriteFood": [
                    "orange",
                    "beetroot",
                    "banana",
                    "strawberry"
                ]
            }
        ]

        # add the 4 people and their friends
        for index, record in enumerate(records):
            file_wrapper.handle_record(index, record)
        file_wrapper.friends_fillup()

        test_common_peopple = CommonPeople()
        response = test_common_peopple.get_response(0, 2)
        common_friends = response[2]['common_friends']
        assert (common_friends[0] == 'Decker Mckenzie')

    def test_common_people_same_query_person(self):
        """
        Querying with person 0 and person 1. Person 1 has brown eyes and is alive. They are friends with each other.
        This test should return an empty array as they don't have common friends with brown eyes and is alive.
        """
        company = Company(
            index=-10,
            company='test company'
        )
        company.save()

        wrapper = Wrapper()
        file_wrapper = wrapper.create('people')

        # record contains 3 people, all friends with each other
        # and one has brown eyes (index=1) and is alive
        # person_index=0 & person_index=1 should not return any common friends who has brown eyes and is alive
        # as person_index=1 is in the query
        records = [
            {
                "index": 0,
                "guid": "5e71dc5d-61c0-4f3b-8b92-d77310c7fa43",
                "has_died": True,
                "age": 61,
                "eyeColor": "blue",
                "name": "TEST USER_1",
                "company_id": company.index,
                "email": "carmellalambert@earthmark.com",
                "phone": "+1 (910) 567-3630",
                "address": "628 Sumner Place, Sperryville, American Samoa, 9819",
                "friends": [
                    {
                        "index": 1
                    },
                    {
                        "index": 2
                    }
                ],
                "favouriteFood": [],
            },
            {
                "index": 1,
                "guid": "5e71dc5d-61c0-4f3b-8b92-d77310fa43",
                "has_died": False,
                "age": 61,
                "eyeColor": "brown",
                "name": "TEST USER_2",
                "company_id": company.index,
                "email": "carmellalambert@earthmark.com",
                "phone": "+1 (910) 567-3630",
                "address": "628 Sumner Place, Sperryville, American Samoa, 9819",
                "friends": [
                    {
                        "index": 0
                    },
                    {
                        "index": 2
                    }
                ],
                "favouriteFood": [],
            },
            {
                "index": 2,
                "guid": "5e71dc5d-61c0-4f3b",
                "has_died": True,
                "age": 61,
                "eyeColor": "blue",
                "name": "TEST USER_3",
                "company_id": company.index,
                "email": "carmellalambert@earthmark.com",
                "phone": "+1 (910) 567-3630",
                "address": "628 Sumner Place, Sperryville, American Samoa, 9819",
                "friends": [
                    {
                        "index": 0
                    },
                    {
                        "index": 1
                    }
                ],
                "favouriteFood": [],
            },
        ]

        # add the 4 people and their friends
        for index, record in enumerate(records):
            file_wrapper.handle_record(index, record)
        file_wrapper.friends_fillup()

        test_common_peopple = CommonPeople()
        response = test_common_peopple.get_response(0, 1)
        common_friends = response[2]['common_friends']
        assert (len(common_friends) == 0)


class TestFavoriteFruitsVeges(TestCase):

    def test_person_fav_fruits_veges(self):
        """
        Add fruit and vegetable, using a person record, relate those fruit and vegetable to
        the person, call the business logic and assert to see if the person has those fruits and veges
        """
        # add a company
        company = Company(
            index=-10,
            company='test company'
        )
        company.save()

        # add a fruit
        fruit = Fruit()
        fruit.fruit_name = "orange"
        fruit.save()

        # add a vegetable
        vegetable = Vegetable()
        vegetable.vegetable_name = "celery"
        vegetable.save()

        # add a person record with their favorite food being orange and celery
        wrapper = Wrapper()
        file_wrapper = wrapper.create('people')
        index = 1
        record = {
            "index": 0,
            "guid": "5e71dc5d-61c0-4f3b-8b92-d77310c7fa43",
            "has_died": True,
            "age": 61,
            "eyeColor": "blue",
            "name": "TEST USER",
            "company_id": company.index,
            "email": "carmellalambert@earthmark.com",
            "phone": "+1 (910) 567-3630",
            "address": "628 Sumner Place, Sperryville, American Samoa, 9819",
            "friends": [],
            "favouriteFood": [
                "orange",
                "celery"
            ]
          }
        file_wrapper.handle_record(index, record)

        test_fav_fruits_veges = FavoriteFruitsVeges()
        response = test_fav_fruits_veges.get_response(record['index'])

        # assert if fruits and vegetables are in the right list
        assert (response['username'] == 'TEST USER')
        assert (response['fruits'][0] == 'orange')
        assert (response['vegetables'][0] == 'celery')
