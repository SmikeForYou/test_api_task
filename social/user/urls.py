from django.urls import path

from user.views import CreateUserView, LastActivityView

urlpatterns = [
    path('sign-up/', CreateUserView.as_view(), name='sign_up'),
    path("last-activity/", LastActivityView.as_view(), name='last_activity')
]
