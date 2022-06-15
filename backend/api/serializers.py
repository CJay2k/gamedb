from rest_framework import serializers

from .models import (AvailablePlatforms, GameDetails, Games, Images, Platforms,
                     Reviews, Stores, Videos, Visits)
from django.utils.text import slugify


class ImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Images
        fields = ['url']


class VideosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Videos
        fields = ['url', 'type', 'is_master']


class GameDetailsSerializer(serializers.ModelSerializer):
    store_name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = GameDetails
        fields = ['store_name',
                  'game_url',
                  'price']

    def get_store_name(self, obj):
        return obj.store.name


class ReviewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reviews
        fields = '__all__'


class VisitsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Visits
        fields = '__all__'


# class GameDetailsAPISerializer(serializers.ModelSerializer):
#     store_name = serializers.CharField(source='store.name')
#     platforms = serializers.SerializerMethodField(read_only=True)

#     class Meta:
#         model = GameDetails
#         fields = ['store_name',
#                   'game_url',
#                   'price',
#                   'platforms']

#     def get_platforms(self, obj):
#         return [platform.platform.name for platform in obj.availableplatforms_set.all()]


class GamesListAPISerializer(serializers.ModelSerializer):
    thumbnail = serializers.SerializerMethodField(read_only=True)
    platforms = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Games
        fields = ['slug',
                  'title',
                  'thumbnail',
                  'platforms']

    def get_thumbnail(self, obj):
        thumbnail = ''
        for details in obj.gamedetails_set.all():
            if thumbnail := details.thumbnail_url:
                return thumbnail
            thumbnail = details.images_set.filter(is_master=True).first()

        return thumbnail or self.get_images(obj)[0]

    def get_platforms(self, obj):
        platforms = []
        for details in obj.gamedetails_set.all():
            platforms.extend(
                platform.platform.name for platform in details.availableplatforms_set.all())

        return set(platforms)


class GameDetailsAPISerializer(serializers.ModelSerializer):
    description = serializers.SerializerMethodField(read_only=True)
    thumbnail = serializers.SerializerMethodField(read_only=True)
    main_media = serializers.SerializerMethodField(read_only=True)
    images = serializers.SerializerMethodField(read_only=True)
    stores = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Games
        fields = ['title',
                  'description',
                  'thumbnail',
                  'main_media',
                  'images',
                  'stores'
                  ]

    def get_description(self, obj):
        best_desc = ''
        polish_accent_characters = [
            'ą', 'ć', 'ę', 'ł', 'ń', 'ó', 'ś', 'ź', 'ż']

        for details in obj.gamedetails_set.all():
            description = details.description
            if not best_desc:
                best_desc = description
            elif any(letter in best_desc for letter in polish_accent_characters):
                if any(letter in description for letter in polish_accent_characters) and len(
                        description) > len(best_desc):
                    best_desc = description
            elif len(description) > len(best_desc) or any(
                    letter in description for letter in polish_accent_characters):
                best_desc = description

        return best_desc

    def get_images(self, obj):
        best_images = []
        for details in obj.gamedetails_set.all():
            images = details.images_set.filter(is_master=False)
            if not best_images or len(images) > len(best_images):
                best_images = images

        return [img['url'] for img in ImagesSerializer(best_images, many=True).data]

    def get_main_media(self, obj):
        best_main_media = {}

        priority = {
            'video': 3,
            'youtube': 2,
            'image': 1,
            'none': 0
        }
        for details in obj.gamedetails_set.all():
            main_media = {}
            if video := details.videos_set.filter(type='video', is_master=True).first() or details.videos_set.filter(type='youtube', is_master=True).first():
                main_media = {
                    'src': video.url,
                    'type': video.type
                }
            elif image := details.images_set.filter(is_master=True).first() or details.images_set.filter().first():
                main_media = {
                    'src': image.url,
                    'type': 'image'
                }

            if priority[main_media.get('type', 'none')] > priority[best_main_media.get('type', 'none')]:
                best_main_media = main_media

        return best_main_media

    def get_thumbnail(self, obj):
        thumbnail = ''
        for details in obj.gamedetails_set.all():
            if thumbnail := details.thumbnail_url:
                return thumbnail
            thumbnail = details.images_set.filter(is_master=True).first()

        return thumbnail or self.get_images(obj)[0]

    def get_stores(self, obj):
        return [GameDetailsSerializer(details).data for details in obj.gamedetails_set.all()]


class GameAllDetailsSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=100)
    store_name = serializers.CharField(max_length=50)
    main_media = serializers.DictField()
    description = serializers.CharField(allow_blank=True)
    thumbnail_url = serializers.URLField(allow_blank=True)
    game_url = serializers.URLField()
    price = serializers.DecimalField(max_digits=7, decimal_places=2)

    images = serializers.ListField(
        child=serializers.URLField(),
        allow_empty=True
    )

    platforms = serializers.ListField(
        child=serializers.CharField(max_length=50)
    )

    def create(self, validated_data):
        game_data = validated_data.pop('title')
        store_data = validated_data.pop('store_name')
        main_media_data = validated_data.pop('main_media')
        images_data = validated_data.pop('images') or []
        platforms_data = validated_data.pop('platforms')

        game, _ = Games.objects.get_or_create(
            slug=slugify(game_data), defaults={'title': game_data})

        store, _ = Stores.objects.get_or_create(name=store_data)

        game_details, _ = GameDetails.objects.get_or_create(
            game=game, store=store, defaults=validated_data)

        for platform in platforms_data:
            p, _ = Platforms.objects.get_or_create(name=platform)
            AvailablePlatforms.objects.get_or_create(
                platform=p, game_details=game_details)

        for image_url in images_data:
            Images.objects.get_or_create(
                game_details=game_details, url=image_url, is_master=False)

        if main_media_data['type'] == 'image':
            Images.objects.get_or_create(
                game_details=game_details, url=main_media_data['src'], defaults={'is_master': True})
        if main_media_data['type'] in ['youtube', 'video']:
            Videos.objects.get_or_create(
                game_details=game_details, url=main_media_data['src'], type=main_media_data['type'], defaults={'is_master': True})

        return game_details
