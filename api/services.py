from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.exceptions import APIException

from django.http import JsonResponse
from api.endpoints.question_endpoints import QuestionOne, QuestionTwo


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


# class QuestionTwo(APIView):
#     def get(self, request):
#         person1_obj = Person.objects.get(
#             index=int(self.request.query_params.get('person1'))
#         )
#         person2_obj = Person.objects.get(
#             index=int(self.request.query_params.get('person2'))
#         )
#
#         color = 'brown'
#         final_list = []
#         for i in Person.objects.raw(
#             'select ip.id, ip.name from data_loader_person p '
#             'join data_loader_personfriend pf on p.id=pf.person_id_id '
#             'join data_loader_person ip on ip.id=pf.friend_id_id '
#             'where p.name in (%s, %s) '
#             'and ip.eye_color=%s and ip.has_died=0 group by ip.id', [person1_obj.name, person2_obj.name, color]
#         ):
#             final_list.append(i.name)
#
#         final_response = [
#             {
#                 "Name": person1_obj.name,
#                 "Age": person1_obj.age,
#                 "Address": person1_obj.address,
#                 "Phone": person1_obj.phone
#             },
#             {
#                 "Name": person2_obj.name,
#                 "Age": person2_obj.age,
#                 "Address": person2_obj.address,
#                 "Phone": person2_obj.phone
#             },
#             {
#                 "common_friends": final_list
#             }
#         ]
#
#         return Response(final_response)
#
#
# class QuestionThree(APIView):
#     def get(self, request, person_index):
#         person_obj = Person.objects.get(
#             index=int(person_index)
#         )
#         fruits_list = []
#         vegetables_list = []
#         fruits = Fruit.objects.filter(person=person_obj)
#         if fruits:
#             fruits_list = [fruit.fruit_name for fruit in fruits]
#
#         vegetables = Vegetable.objects.filter(person=person_obj)
#         if vegetables:
#             vegetables_list = [vege.vegetable_name for vege in vegetables]
#
#         final_response = {
#             "username": person_obj.name,
#             "age": person_obj.age,
#             "fruits": fruits_list,
#             "vegetables": vegetables_list
#         }
#         return Response(final_response)
