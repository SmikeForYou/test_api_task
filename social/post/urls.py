from django.urls import path, include
from post import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"posts", views.PostsViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("posts/<int:pk>", views.PostsPatrialUpdateView.as_view())
]