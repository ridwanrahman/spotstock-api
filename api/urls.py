from django.urls import include, path
from rest_framework import routers
from .services import question_one, question_two
from api.endpoints.viewsets import (CompanyViewSet, PersonFriendViewSet,
                                        PersonViewSet, FruitViewSet, VegetableViewSet)


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
    # path('q3/<int:person_index>', views.QuestionThree.as_view()),
    # path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
urlpatterns += router.urls