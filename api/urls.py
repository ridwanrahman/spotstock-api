from django.urls import include, path

from rest_framework import routers

from api.endpoints.viewsets import (CompanyViewSet, PersonFriendViewSet,
                                        PersonViewSet, FruitViewSet, VegetableViewSet)
from .services import get_all_company_employees, common_people, question_three


router = routers.DefaultRouter()
router.register(r'company', CompanyViewSet)
router.register(r'person', PersonViewSet)
router.register(r'personfriend', PersonFriendViewSet)
router.register(r'fruit', FruitViewSet)
router.register(r'vegetable', VegetableViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('all_company_employees/<int:company_index>', get_all_company_employees),
    path('common_people', common_people),
    path('q3/<int:person_index>', question_three),
]
urlpatterns += router.urls