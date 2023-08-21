from django.conf import settings
from rest_framework import serializers

from api.serializers import UserSerializer
from services.models import CustomServiceType, PredefinedServiceType, Service


class PredefinedServiceTypeSerializer(serializers.ModelSerializer):
    name = serializers.CharField(
        max_length=settings.MAX_LEN_NAME, required=True
    )

    class Meta:
        model = PredefinedServiceType
        fields = ('id', 'name')


class ServiceSerializer(serializers.ModelSerializer):
    title = serializers.CharField(required=True)
    service_image = serializers.ImageField(required=False)
    price = serializers.IntegerField(min_value=1, required=True)
    description = serializers.CharField(
        max_length=settings.MAX_LEN_ABOUT_ME, required=False
    )
    duration = serializers.IntegerField(min_value=1, required=True)
    service_type = PredefinedServiceTypeSerializer(read_only=True)

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user
        worker_service = Service.objects.create(
            title=validated_data.get('title'),
            service_image=validated_data.get('service_image'),
            price=validated_data.get('price'),
            description=validated_data.get('description'),
            duration=validated_data.get('duration'),
            service_type=PredefinedServiceType(
                name=validated_data.get('service_type').get('name')
            ),
            worker=user,
        )
        return worker_service

    def validate_service_type(self, field):
        service_name = field.get('name')
        if not PredefinedServiceType.objects.filter(
            name=service_name
        ).exists():
            raise serializers.ValidationError('Такого сервиса нет!', code=404)
        user = self.context.get('request').user
        custom_type = CustomServiceType.objects.filter(
            name=service_name
        ).first()
        if custom_type is not None and custom_type.worker != user:
            raise serializers.ValidationError(
                'У Вас нет доступа к этому виду услуги', code=400
            )
        return field

    class Meta:
        model = Service
        fields = (
            'id',
            'title',
            'service_image',
            'price',
            'description',
            'duration',
            'service_type',
        )


class CustomServiceTypeSerializer(PredefinedServiceTypeSerializer):
    worker = UserSerializer(read_only=True)

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user
        custom_service_type = CustomServiceType(
            name=validated_data.get('name'),
            worker=user,
        )
        custom_service_type.save()
        return custom_service_type

    class Meta:
        model = CustomServiceType
        fields = ('id', 'name', 'worker')
