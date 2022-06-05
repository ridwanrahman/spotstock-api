import json
from django.test import TestCase

from data_loader.models import Company, Person, Fruit, Vegetable
from data_loader.wrappers.Wrapper import Wrapper

from api.endpoints.feature_endpoints import AllCompanyEmployees, CommonPeople, FavoriteFruitsVeges


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
                    },
                    {
                        "index": 3
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
                    },
                    {
                        "index": 2
                    },
                    {
                        "index": 3
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
                    },
                    {
                        "index": 3
                    }
                ],
                "favouriteFood": [],
            },
            {
                "index": 3,
                "guid": "5e71dc5d--4f3b-8b92-d77310fa43",
                "has_died": False,
                "age": 61,
                "eyeColor": "brown",
                "name": "TEST USER_4",
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
                    },
                    {
                        "index": 2
                    }
                ],
                "favouriteFood": [],
            }
        ]

        # add the 4 people and their friends
        for index, record in enumerate(records):
            file_wrapper.handle_record(index, record)
        file_wrapper.friends_fillup()

        test_common_peopple = CommonPeople()
        response = test_common_peopple.get_response(0, 2)
        common_friends = response[2]['common_friends']
        assert (common_friends[0] == 'TEST USER_4')

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
