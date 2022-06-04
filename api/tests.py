import json
from django.test import TestCase


from data_loader.models import Company, Person, Fruit, Vegetable
from api.endpoints.question_endpoints import QuestionOne, QuestionTwo, QuestionThree
from data_loader.wrappers.Wrapper import Wrapper


class TestQuestionOne(TestCase):

    def test_question_one(self):

        # add a company
        company = Company()
        company.index = -10
        company.name = 'test company'
        company.save()

        # add second company
        company2 = Company()
        company2.index = -20
        company2.name = 'second test company'
        company2.save()

        # add person and relate it to company
        person = Person()
        person.index = -10
        person.guid = 'test'
        person.name = 'test'
        person.age = 50
        person.address = 'test'
        person.phone = 'test'
        person.eye_color = 'test'
        person.has_died = True
        person.company_id = company
        person.save()

        # add second person and also relate to first company
        person2 = Person()
        person2.index = -11
        person2.guid = 'test2'
        person2.name = 'test2'
        person2.age = 50
        person2.address = 'test2'
        person2.phone = 'test2'
        person2.eye_color = 'test2'
        person2.has_died = False
        person2.company_id = company
        person2.save()

        # assert the first user was added to first company
        question_one = QuestionOne()
        response = question_one.get_response(company.index)
        resp_json = json.loads(json.dumps(response))
        assert(resp_json[0]['name'] == 'test')
        assert (resp_json[0]['company_id'] == 1)

        # assert that the seonc company has no employees
        question_one_2 = QuestionOne()
        response_2 = question_one_2.get_response(company2.index)
        resp_json_2 = json.loads(json.dumps(response_2))
        assert (resp_json_2['response'] == 'No employees found for company index: -20')

        # move person2 to second company and assert second company to see if their employee is
        # person2
        person2.company_id = company2
        person2.save()
        question_one_2 = QuestionOne()
        response_2 = question_one_2.get_response(company2.index)
        resp_json_2 = json.loads(json.dumps(response_2))
        assert (resp_json_2[0]['name'] == 'test2')
        assert (resp_json_2[0]['company_id'] == 2)


class TestQuestionTwo(TestCase):

    def test_question_two(self):
        wrapper = Wrapper()
        file_wrapper = wrapper.create('people')

        # record contains 4 peope, all friends with each other
        # and two have brown eyes
        records = [
            {
                "index": 0,
                "guid": "5e71dc5d-61c0-4f3b-8b92-d77310c7fa43",
                "has_died": True,
                "age": 61,
                "eyeColor": "blue",
                "name": "TEST USER_1",
                "company_id": 58,
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
                "company_id": 58,
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
                "company_id": 58,
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
                "company_id": 58,
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

        question_two = QuestionTwo()
        response = question_two.get_response(0, 1)
        common_friends = response[2]['common_friends']
        assert (common_friends[0] == 'TEST USER_4')


class TestQuestionThree(TestCase):

    def test_question_three(self):
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
            "company_id": 58,
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

        question_three = QuestionThree()
        response = question_three.get_response(record['index'])

        # assert if fruits and vegetables are in the right list
        assert (response['username'] == 'TEST USER')
        assert (response['fruits'][0] == 'orange')
        assert (response['vegetables'][0] == 'celery')
