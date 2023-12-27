import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User as DjangoUser
from Products.models import Product

class UserProfile(models.Model):
    user = models.OneToOneField(DjangoUser, on_delete=models.CASCADE)
    address = models.CharField(_('Address'), max_length=255, blank=True)
    is_admin = models.BooleanField(default=False)
    email = models.EmailField(default=None, null=True)
    phone_number = models.CharField(_('Phone Number'), max_length=15, blank=True)
    profile_image = models.ImageField(_('Profile Image'), upload_to='user_profile_images/', blank=True, null=True)
    date_of_birth = models.DateField(_('Date of Birth'), blank=True, null=True)


class Review(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')
