from rest_framework import viewsets

from services.models import CustomServiceType, Service
from services.serializers import CustomServiceTypeSerializer, ServiceSerializer


class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            if self.action in ('list', 'retieve'):
                return Service.objects.filter(worker=user).all()
        return super().get_queryset()


class CustomServiceTypeViewSet(viewsets.ModelViewSet):
    serializer_class = CustomServiceTypeSerializer

    def get_queryset(self):
        return CustomServiceType.objects.filter(worker=self.request.user).all()
