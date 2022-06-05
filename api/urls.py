from django.urls import include, path

from rest_framework import routers

from api.endpoints.viewsets import (CompanyViewSet, PersonFriendViewSet,
                                    PersonViewSet, FruitViewSet, VegetableViewSet)
from .services import get_all_company_employees, common_people, get_person_liked_fruits_veges

# Urls for the apiroot that can be accessed by going to `localhost:8000`
router = routers.DefaultRouter()
router.register(r'company', CompanyViewSet)
router.register(r'person', PersonViewSet)
router.register(r'personfriend', PersonFriendViewSet)
router.register(r'fruit', FruitViewSet)
router.register(r'vegetable', VegetableViewSet)

# urls for the different apis
urlpatterns = [
    path('', include(router.urls)),
    path('all_company_employees/<int:company_index>', get_all_company_employees, name='all_company_employees'),
    path('common_people', common_people, name='common_people'),
    path('person_liked_fruits_veges/<int:person_index>', get_person_liked_fruits_veges, name='person_liked_fruits_veges'),
]
urlpatterns += router.urls
