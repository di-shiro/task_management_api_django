from django.urls import path, include
from rest_framework import routers

''' # path名とViewsを連携させる。下のrouterにModelViewSetを追加していく。 '''
router = routers.DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
]
