from rest_framework import serializers
from post import models as post_models


class PostSerializer(serializers.ModelSerializer):
    liked = serializers.BooleanField(required=False, default=False)

    def to_representation(self, instance: post_models.Post):
        data = super().to_representation(instance=instance)
        data["liked"] = instance.liked_by_user(self.context["request"].user)
        return data

    def create(self, validated_data):
        validated_data["author"] = self.context["request"].user
        liked_status = validated_data.pop("liked", None)
        instance: post_models.Post = super().create(validated_data)
        if liked_status is not None:
            instance.set_liked_status(self.context["request"].user, liked_status)
        return instance

    def update(self, instance: post_models.Post, validated_data):
        liked_status = validated_data.get("liked")
        if liked_status is not None:
            instance.set_liked_status(self.context["request"].user, liked_status)
        return super().update(instance, validated_data)


    class Meta:
        model = post_models.Post
        fields = ("id", "title", "body", "liked")