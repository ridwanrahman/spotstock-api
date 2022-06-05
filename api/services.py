from django.http import JsonResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.endpoints.feature_endpoints import (AllCompanyEmployees,
                                             CommonPeople, FavoriteFruitsVeges)


def handler404(request, exception):
    return JsonResponse(
        {'status_code': 404,
         'error': 'The resource was not found'
         }
    )


@api_view(['GET'])
def get_all_company_employees(request, company_index) -> dict:
    """
    Calls the business logic class with the company_index and returns the company's employees

    :param request: drf request
    :param company_index: int
    :return: dict
    """
    all_company_employees = AllCompanyEmployees()
    response = all_company_employees.get_response(company_index)
    return Response(response)


@api_view(['GET'])
def common_people(request) -> dict:
    """
    Calls the business logic class with the 2 people's index and returns their information and common friend

    :param request drf request:
    :return: dict
    """
    try:
        person_1_index = int(request.query_params.get('person1'))
        person_2_index = int(request.query_params.get('person2'))

        if person_1_index is None or person_2_index is None:
            raise ValueError("Error")

        common_people_obj = CommonPeople()
        response = common_people_obj.get_response(person_1_index, person_2_index)
        return Response(response)
    except Exception as e:
        print(e)
        return {'error': 'data error'}


@api_view(['GET'])
def get_person_liked_fruits_veges(request, person_index):
    """
    Calls the business logic with a person_index to load a list of their favorite fruits and veges

    :param request: drf request
    :param person_index: int
    :return:
    """
    fav_fruits_veges_obj = FavoriteFruitsVeges()
    response = fav_fruits_veges_obj.get_response(person_index)
    return Response(response)
