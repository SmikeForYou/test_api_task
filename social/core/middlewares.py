from user.models import UserActivity
from django.http import HttpRequest


class UserActionsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if request.user.is_authenticated:
            UserActivity.objects.create(user=request.user, action=request.path)
        return response