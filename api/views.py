from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from api.serializers import CompanySerializer, PersonSerializer, PersonFriendSerializer, FruitSerializer, \
    VegetableSerializer
from data_loader.models import Company, Person, PersonFriend, Fruit, Vegetable

from rest_framework.views import APIView
from rest_framework.response import Response


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
        person1_obj = Person.objects.get(
            index=int(self.request.query_params.get('person1'))
        )
        person2_obj = Person.objects.get(
            index=int(self.request.query_params.get('person2'))
        )

        color = 'brown'
        final_list = []
        for i in Person.objects.raw(
            'select ip.id, ip.name from data_loader_person p '
            'join data_loader_personfriend pf on p.id=pf.person_id_id '
            'join data_loader_person ip on ip.id=pf.friend_id_id '
            'where p.name in (%s, %s) '
            'and ip.eye_color=%s and ip.has_died=0 group by ip.id', [person1_obj.name, person2_obj.name, color]
        ):
            final_list.append(i.name)

        final_response = [
            {
                "Name": person1_obj.name,
                "Age": person1_obj.age,
                "Address": person1_obj.address,
                "Phone": person1_obj.phone
            },
            {
                "Name": person2_obj.name,
                "Age": person2_obj.age,
                "Address": person2_obj.address,
                "Phone": person2_obj.phone
            },
            {
                "common_friends": final_list
            }
        ]

        return Response(final_response)

