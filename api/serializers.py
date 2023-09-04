from rest_framework import serializers, status

from orders.models import Chat, Message, Order, Raiting
from properties.models import FeedbackProperty, Property, Room
from services.models import MediaFile, Service
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'first_name',
            'last_name',
            'profile_photo',
            'email',
            'contact_email',
            'phone',
            'work_experience',
            'city',
            'raiting',
            'about_me',
            'is_client',
            'is_photographer',
            'is_video_operator',
            'birthday',
            'social_telegram',
            'social_vkontakte',
        )


class PropertySerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Property
        fields = (
            'user',
            'name',
            'adress',
            'worktime',
            'area',
            'price',
        )


class RoomSerializer(serializers.ModelSerializer):
    property = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Room
        fields = (
            'property',
            'name',
            'area',
            'price',
        )


class FBpropertySerializer(serializers.ModelSerializer):
    property = serializers.StringRelatedField(read_only=True)
    user_client = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = FeedbackProperty
        fields = (
            'property',
            'raiting',
            'descriptions',
            'user_client',
        )


class MediafileSerializer(serializers.ModelSerializer):
    class Meta:
        model = MediaFile
        fields = (
            'title',
            'image',
            'video_link',
            'media_type',
            'is_main_photo',
        )
        read_only_fields = ('media_type',)

    def create(self, validated_data):
        title = validated_data.get('title')
        image = validated_data.get('image')
        video_link = validated_data.get('video_link')
        is_main_photo = validated_data.get('is_main_photo')
        media_type = (
            MediaFile.MediaTypeEnum.PHOTO.value
            if image
            else MediaFile.MediaTypeEnum.VIDEO.value
        )
        media_file = MediaFile.objects.create(
            title=title,
            image=image,
            video_link=video_link,
            media_type=media_type,
            is_main_photo=is_main_photo,
        )
        return media_file

    def validate(self, attrs):
        image = attrs.get('image')
        video_link = attrs.get('video_link')
        if (image and video_link) or (not image and not video_link):
            raise serializers.ValidationError(
                detail='Укажите либо файл фотографии либо ссылку на видео',
                code=status.HTTP_400_BAD_REQUEST,
            )
        return super().validate(attrs)


class ServiceLimitedMediaSerializer(serializers.ModelSerializer):
    media_files = serializers.SerializerMethodField(
        method_name='get_media_files'
    )

    class Meta:
        model = Service
        fields = (
            'name_service',
            'image_service',
            'cost_service',
            'description_service',
            'due_date',
            'media_files',
        )

    def get_media_files(self, service: Service):
        all_media_files = service.media_files.order_by('media_type').all()
        photos = all_media_files.filter(
            media_type=MediaFile.MediaTypeEnum.PHOTO.value
        )
        video = all_media_files.filter(
            media_type=MediaFile.MediaTypeEnum.VIDEO.value
        )
        if len(video) == 1:
            video = video[:1]
            photos = photos[:5]
        elif len(video) >= 2:
            video = video[:2]
            photos = photos[:4]
        else:
            return MediafileSerializer(photos[:6], many=True).data
        video_ids = [vid.id for vid in video]
        photos_id = [photo.id for photo in photos]
        return MediafileSerializer(
            all_media_files.filter(id__in=video_ids + photos_id), many=True
        ).data


class ServiceSerializer(serializers.ModelSerializer):
    media_files = MediafileSerializer(many=True)

    class Meta:
        model = Service
        fields = (
            'name_service',
            'image_service',
            'cost_service',
            'description_service',
            'due_date',
            'media_files',
        )


class GeneralCatalogExecutorCardSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()
    portfolio = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'id',
            'full_name',
            'is_client',
            'is_photographer',
            'is_video_operator',
            'about_me',
            'price',
            'portfolio',
        )

    def get_full_name(self, obj):
        return f'{obj.first_name} {obj.last_name}'

    def get_price(self, obj):
        services = obj.services.all()
        if services:
            lower_price = services.order_by('cost_service')[0].cost_service
            return lower_price

    def get_portfolio(self, obj):
        all_media = obj.portfolio.all().order_by('media_file__media_type')
        selection = []
        if all_media:
            last_media = all_media[-1]
            if last_media.media_file.media_type == 'Video':
                selection.append(last_media.media_file.link)
            for i in range(4):
                media = all_media[i]
                selection.append(media.media_file.link)
                if len(selection) == 4:
                    break

        return selection


class ChatSerializer(serializers.ModelSerializer):
    users = serializers.StringRelatedField(read_only=True, many=True)

    class Meta:
        model = Chat
        fields = (
            'name',
            'users',
        )


class OrderSerializer(serializers.ModelSerializer):
    service = serializers.StringRelatedField(read_only=True)
    chat = serializers.StringRelatedField(read_only=True)
    users = serializers.StringRelatedField(read_only=True, many=True)

    class Meta:
        model = Order
        fields = (
            'name',
            'cost',
            'date',
            'completion_date',
            'status',
            'users',
            'service',
            'chat',
        )


class MessageSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Message
        fields = (
            'chat',
            'author',
            'text',
            'created_at',
        )


class RaitingSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True, many=True)

    class Meta:
        model = Raiting
        fields = (
            'order',
            'user',
            'raiting',
        )


class CatalogDetailSerializer(serializers.ModelSerializer):
    # services = ServiceSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'profile_photo',
            'equipment',
            'about_me',
            'is_photographer',
            'is_video_operator',
            'contact_email',
            'phone',
            'social_telegram',
            'social_vkontakte',
            # 'services',
        )
