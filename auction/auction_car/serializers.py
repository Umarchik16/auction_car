from .models import *
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('username', 'email', 'password', 'first_name', 'last_name',
                  'phone_number')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = UserProfile.objects.create_user(**validated_data)
        return user


class CustomLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError('Неверные учетные данные')

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'username': instance.username,
                'email': instance.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name', 'username', 'user_role', 'phone_number']


class UserProfileSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name', 'user_role']


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['brand_name']


class ModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Model
        fields = ['model_name']


class CarListSerializer(serializers.ModelSerializer):
    model = ModelSerializer(read_only=True)

    class Meta:
        model = Car
        fields = ['task', 'id', 'model', 'year',
                  'fuel_type', 'mileage', 'price', 'transmission']


class CarDetailSerializer(serializers.ModelSerializer):
    model = ModelSerializer(read_only=True)
    brand = BrandSerializer(read_only=True)
    seller = UserProfileSerializer(read_only=True)

    class Meta:
        model = Car
        fields = ['task', 'model', 'year', 'fuel_type', 'mileage', 'price',
                  'transmission', 'description', 'seller',
                  'brand', 'model']


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'


class AuctionSerializer(serializers.ModelSerializer):
    car = CarListSerializer(read_only=True)

    class Meta:
        model = Auction
        fields = '__all__'


class BidSerializer(serializers.ModelSerializer):
    auction = AuctionSerializer(read_only=True)
    buyer = UserProfileSimpleSerializer(read_only=True)

    class Meta:
        model = Bid
        fields = '__all__'


class FeedBackSerializer(serializers.ModelSerializer):
    seller = UserProfileSimpleSerializer(read_only=True)
    buyer = UserProfileSimpleSerializer(read_only=True)

    class Meta:
        model = FeedBack
        fields = '__all__'
