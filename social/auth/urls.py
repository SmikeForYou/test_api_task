from django.urls import path
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    path('token/', jwt_views.TokenObtainSlidingView.as_view(), name='token_obtain_sliding'),
]