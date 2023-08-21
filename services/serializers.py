from django.conf import settings
from rest_framework import serializers

from services.models import CustomServiceType, PredefinedServiceType, Service


class PredefinedServiceTypeSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=settings.MAX_LEN_NAME)

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
    service_type = PredefinedServiceTypeSerializer()

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user
        service = Service.objects.create(
            title=validated_data.get('title'),
            service_image=validated_data.get('service_image'),
            price=validated_data.get('price'),
            description=validated_data.get('description'),
            duration=validated_data.get('duration'),
            service_type=PredefinedServiceType.objects.get(
                **validated_data.get('service-type')
            ),
            worker=user,
        )
        return service

    def validate_service_type(self, service_type: PredefinedServiceType):
        if not PredefinedServiceType.objects.filter(**service_type).exists():
            raise serializers.ValidationError(
                'Такого вида сервиса нет!', code=404
            )
        user = self.context.get('request').user
        custom_type = CustomServiceType.objects.filter(**service_type).first()
        if custom_type is not None and custom_type.worker != user:
            raise serializers.ValidationError(
                'У Вас нет доступа к этому виду услуги', code=400
            )
        return service_type

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
    worker = serializers.HiddenField(default=serializers.CurrentUserDefault())

    def create(self, validated_data):
        custom_service_type, created = CustomServiceType.objects.get_or_create(
            **validated_data,
        )
        return custom_service_type

    class Meta:
        model = CustomServiceType
        fields = ('id', 'name', 'worker')
