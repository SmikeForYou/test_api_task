from drf_yasg import utils
from post import models as post_models
from post import serializers as post_serializers
from rest_framework import viewsets, permissions, mixins, response, views


@utils.swagger_auto_schema()
class PostsViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin,
                   mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = post_serializers.PostSerializer
    queryset = post_models.Post.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class PostsPatrialUpdateView(views.APIView):
    serializer_class = post_serializers.PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, pk):
        post = post_models.Post.objects.get(pk=pk)
        self.check_object_permissions(self.request, post)
        return post


    @utils.swagger_auto_schema(request_body=post_serializers.PostSerializer, responses={200: post_serializers.PostSerializer})
    def patch(self, request, pk):
        instance = self.get_object(pk)
        context = {"request": self.request}
        serializer = self.serializer_class(instance, data=request.data, partial=True, context=context)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return response.Response(data=serializer.data)
