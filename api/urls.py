from django.urls import include, path

from rest_framework import routers

from api.endpoints.viewsets import (CompanyViewSet, PersonFriendViewSet,
                                        PersonViewSet, FruitViewSet, VegetableViewSet)
from .services import question_one, question_two, question_three


router = routers.DefaultRouter()
router.register(r'company', CompanyViewSet)
router.register(r'person', PersonViewSet)
router.register(r'personfriend', PersonFriendViewSet)
router.register(r'fruit', FruitViewSet)
router.register(r'vegetable', VegetableViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('q1/<int:company_index>', question_one),
    path('q2', question_two),
    path('q3/<int:person_index>', question_three),
]
urlpatterns += router.urls