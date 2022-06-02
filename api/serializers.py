from rest_framework import serializers
from data_loader.models import Company, Person, PersonFriend, Fruit, Vegetable


class CompanySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Company
        fields = ['id', 'index', 'company']


class PersonSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Person
        fields = ['id', 'index', 'guid', 'name', 'age', 'address', 'phone', 'eye_color', 'has_died', 'company_id']


class PersonFriendSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PersonFriend
        fields = ['person_id', 'friend_id']


class FruitSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Fruit
        fields = ['id', 'fruit_name']


class VegetableSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Vegetable
        fields = ['id', 'vegetable_name']
