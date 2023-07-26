"""
URL configuration for darinatoys project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from store.views import *
from .settings import MEDIA_ROOT, DEBUG, MEDIA_URL
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
import os

urlpatterns = [
    path('admin/', admin.site.urls),
    path('toylist/', ToyAPIList.as_view()),
    path('toy/<str:slug>/', RetrieveToyAPI.as_view()),
    path('category/<str:slug>/', ListToysByCategory.as_view()),
    path('cart/', CartAPIView.as_view()),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path("all-profiles",UserProfileListCreateView.as_view(),name="all-profiles"),
    path("profile/<int:pk>",userProfileDetailView.as_view(),name="profile"),
    path('cart/purchase/', TransactionAPIView.as_view()),
    path('feedback/', FeedbackAPI.as_view()),
]

urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT, name='media')
