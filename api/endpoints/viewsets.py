from rest_framework import viewsets
from api.serializers import CompanySerializer, PersonSerializer, PersonFriendSerializer, FruitSerializer, \
    VegetableSerializer
from data_loader.models import Company, Person, PersonFriend, Fruit, Vegetable




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