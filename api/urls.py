from django.urls import include, path
from rest_framework import routers
from . import views


router = routers.DefaultRouter()
router.register(r'company', views.CompanyViewSet)
router.register(r'person', views.PersonViewSet)
router.register(r'personfriend', views.PersonFriendViewSet)
router.register(r'fruit', views.FruitViewSet)
router.register(r'vegetable', views.VegetableViewSet)
# router.register(r'question_one', views.QuestionOne)

urlpatterns = [
    path('', include(router.urls)),
    path('q1/<int:company_index>', views.QuestionOne.as_view()),
    path('q2', views.QuestionTwo.as_view()),
    # path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
urlpatterns += router.urls