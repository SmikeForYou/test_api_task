from django.contrib.auth import get_user_model
from rest_framework import serializers
from user.models import User

user_model = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = user_model.objects.create(
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    class Meta:
        model = user_model
        fields = ("id", "email", "password")


class LastActivitySerializer(serializers.ModelSerializer):
    last_activity = serializers.SerializerMethodField()

    def get_last_activity(self, obj: User):
        return obj.last_activity

    class Meta:
        model = user_model
        fields = ("id", "last_login", "last_activity")