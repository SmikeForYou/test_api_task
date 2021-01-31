from django.shortcuts import render

# Create your views here.
class SwaggerFakeViewMixin:
    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return self.queryset.model.objects.none()
        return super().get_queryset(self)