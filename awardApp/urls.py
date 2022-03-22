from django import views
from django.contrib import admin
from django.urls import path,include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('profile', views.Profile_viewSet)
router.register('posts', views.Post_viewSet)
router.register('users', views.User_viewSet)


urlpatterns = [
    path('',views.index, name = 'homepage' ),
    path('signup/', views.signup, name='signup'),
    path('', include('django.contrib.auth.urls')),
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('profile/<username>/', views.profile, name='profile'),
    path('project/<post>', views.project_rating, name='project'),
    path('profile/<username>/edit', views.edit_profile, name='edit_profile'),


]