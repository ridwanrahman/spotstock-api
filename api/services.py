from django.http import JsonResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.endpoints.question_endpoints import QuestionOne, QuestionTwo, QuestionThree


def handler404(request, exception):
    return JsonResponse(
        {'status_code': 404,
         'error': 'The resource was not found'
         }
    )


@api_view(['GET'])
def question_one(request, company_index):
    one = QuestionOne()
    response = one.get_response(company_index)
    return Response(response)


@api_view(['GET'])
def question_two(request):
    try:
        person_1_index = int(request.query_params.get('person1'))
        person_2_index = int(request.query_params.get('person2'))

        if person_1_index is None or person_2_index is None:
            raise ValueError("Error")

        two = QuestionTwo()
        response = two.get_response(person_1_index, person_2_index)
        return Response(response)
    except Exception as e:
        print(e)
        return {'error': 'data error'}


@api_view(['GET'])
def question_three(request, person_index):
    three = QuestionThree()
    response = three.get_response(person_index)
    return Response(response)
