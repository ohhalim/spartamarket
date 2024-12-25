from django.db import models
from django.core.exceptions import ValidationError
from django.conf import settings
import re
from accounts.models import User

def product_image_path(instance, filename):
    return f'product_images/{instance.user.username}/{filename}'

def validation_hashtag(value):
    if not re.match(r'^[0-9a-zA-Z]+$', value):
        raise ValidationError('해시태그는 알파벳, 숫자, 언더스코어만 가능합니다!')

class HashTag(models.Model):
    name = models.CharField(max_length=50, unique=True, validators=[validation_hashtag])
    
    def __str__(self):
        return f'#{self.name}'

class Product(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='products')
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to=product_image_path, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked_products', blank=True)
    hashtags = models.ManyToManyField(HashTag, related_name='products', blank=True)
    views = models.PositiveIntegerField(default=0)  

    def like_count(self):
        return self.likes.count()
    
    def __str__(self):
        return self.title 