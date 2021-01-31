from django.contrib.auth import get_user_model
from rest_framework import permissions, response
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from drf_yasg import utils
from user import serializers as user_serializers
from rest_framework import viewsets, permissions, mixins, response, views


class CreateUserView(CreateAPIView):
    model = get_user_model()
    permission_classes = [permissions.AllowAny]
    serializer_class = user_serializers.UserSerializer



class LastActivityView(views.APIView):
    serializer_class = user_serializers.LastActivitySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

    @utils.swagger_auto_schema(responses={200: user_serializers.LastActivitySerializer})
    def get(self, request):
        instance = self.get_object()
        serializer = self.serializer_class(instance)
        return response.Response(data=serializer.data)