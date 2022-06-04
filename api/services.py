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
    response = one.get_response(request, company_index)
    return Response(response)


@api_view(['GET'])
def question_two(request):
    two = QuestionTwo()
    response = two.get_response(request)
    return Response(response)


@api_view(['GET'])
def question_three(request, person_index):
    three = QuestionThree()
    response = three.get_response(person_index)
    return Response(response)
