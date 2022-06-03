from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from api.serializers import CompanySerializer, PersonSerializer, PersonFriendSerializer, FruitSerializer, VegetableSerializer
from data_loader.models import Company, Person, PersonFriend, Fruit, Vegetable

from rest_framework.views import APIView
from rest_framework.response import Response
# from django.http.HttpRequest import Request

from rest_framework.decorators import api_view


class CompanyViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows companies to be viewed or edited.
    """
    queryset = Company.objects.all()
    serializer_class = CompanySerializer


class PersonViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows people to be viewed or edited.
    """
    queryset = Person.objects.all()
    serializer_class = PersonSerializer


class PersonFriendViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows person and friend relation to be viewed or edited.
    """
    queryset = PersonFriend.objects.all()
    serializer_class = PersonFriendSerializer


class FruitViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows fruits to be viewed or edited.
    """
    queryset = Fruit.objects.all()
    serializer_class = FruitSerializer


class VegetableViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows vegetables to be viewed or edited.
    """
    queryset = Vegetable.objects.all()
    serializer_class = VegetableSerializer


# @api_view(['GET'])
# def question_one(request):
#     return Response({
#         'status': 200,
#         'message': 'success'
#     })
class QuestionOne(APIView):
    def get(self, request, company_index):
        """
        Return a list of all users.
        """
        serializer_context = {
            'request': request,
        }

        id = company_index or request.query_params.get('company_index')
        people_working_in_company = Person.objects.filter(company_id__index=id)
        if not people_working_in_company:
            return Response({
                'response': "Nobody working in this company"
            })
        serializer = PersonSerializer(people_working_in_company, many=True, context=serializer_context)
        return Response(serializer.data)

class QuestionTwo(APIView):
    def get(self, request):
        person1 = self.request.query_params.get('person1')
        person2 = self.request.query_params.get('person1')

        print(person1)
        print(person2)
