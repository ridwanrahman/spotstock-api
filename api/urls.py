from django.urls import include, path
from rest_framework import routers
from . import views


router = routers.DefaultRouter()
router.register(r'company', views.CompanyViewSet)
router.register(r'person', views.PersonViewSet)
router.register(r'personfriend', views.PersonFriendViewSet)
router.register(r'fruit', views.FruitViewSet)
router.register(r'vegetable', views.VegetableViewSet)

urlpatterns = [
    path('', include(router.urls)),
    # path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]