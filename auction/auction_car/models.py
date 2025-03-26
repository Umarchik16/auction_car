from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from rest_framework.exceptions import ValidationError


class UserProfile(AbstractUser):
    phone_number = PhoneNumberField(null=True, blank=True)
    ROLE_CHOICES = (
        ('Администратор', 'Администратор'),
        ('Продавец', 'Продавец'),
        ('Покупатель', 'Покупатель'),
    )
    user_role = models.CharField(max_length=32, choices=ROLE_CHOICES, default='Администратор')

    def __str__(self):
        return f'{self.first_name} - {self.last_name}'


class Brand(models.Model):
    brand_name = models.CharField(max_length=32)

    def __str__(self):
        return f'{self.brand_name}'


class Model(models.Model):
    model_name = models.CharField(max_length=32, null=True, blank=True)
    brand_model = models.ForeignKey(Brand, on_delete=models.CASCADE)

    def __str__(self):
        return self.model_name


class Car(models.Model):
    task = models.CharField(max_length=32, null=True, blank=True)
    year = models.PositiveSmallIntegerField()
    FUEL_CHOICES = [
        ('petrol', 'Бензин'),
        ('diesel', 'Дизель'),
        ('electric', 'Электро'),
        ('hybrid', 'Гибрид'),
    ]
    fuel_type = models.CharField(max_length=32, choices=FUEL_CHOICES)
    AUTO_CHOICES = (
        ('автомат', 'автомат'),
        ('механика', 'механика')
    )
    transmission = models.CharField(max_length=32, choices=AUTO_CHOICES)
    mileage = models.IntegerField(verbose_name='пробег')
    price = models.PositiveSmallIntegerField()
    description = models.TextField()
    seller = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='seller_user')
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='brand')
    model = models.ForeignKey(Model, on_delete=models.CASCADE, related_name='model')

    def __str__(self):
        return f'{self.model}'


class Image(models.Model):
    car_image = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='car_images')
    image = models.ImageField(upload_to='image')

    def __str__(self):
        return str(self.image)


class Auction(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE,  related_name='car')
    start_price = models.DecimalField(max_digits=10, decimal_places=2)
    min_price = models.DecimalField(max_digits=10, decimal_places=2)
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    STATUS_CHOICES = (
        ('активен', 'активен'),
        ('завершен', 'завершен'),
        ('отменен', 'отменен'),
    )
    status = models.CharField(max_length=32, choices=STATUS_CHOICES)

    def __str__(self):
        return self.status


class Bid(models.Model):
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE,  related_name='bids')
    buyer = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='buyer_bid')
    amount = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='размер ставки')
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'Bid by {self.buyer} - {self.amount} on {self.created_at}'


class FeedBack(models.Model):
    seller = models.ForeignKey(UserProfile, on_delete=models.CASCADE,  related_name='Покупатель')
    buyer = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='Продавец')
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    comment = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'Feedback from {self.buyer} to {self.seller} - Rating: {self.rating}'
