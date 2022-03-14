
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register('profile', views.UserViewSet)
router.register('posts', views.UserViewSet)
router.register('users', views.UserViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('awardApp.urls')),
    path('api/', include(router.urls)),
]
