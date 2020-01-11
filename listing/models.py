from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

class Listing(models.Model):
    name = models.CharField(max_length=1000, blank=False)
    date_created = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True, null=True)
    url = models.CharField(max_length=1000, blank=True, null=True)
    email = models.CharField(max_length=250, blank=False)
    phone_number = models.CharField(max_length=15, blank=False)
    address = models.TextField(blank=False)
    last_modified_date = models.DateTimeField(blank = True, null = True)
    default_image = models.ForeignKey('Image', on_delete=models.CASCADE, blank=True, null=True)
    other_images = models.ManyToManyField('Image', blank=True, related_name="other_images")
    view_count = models.IntegerField(default=0)
    categories = models.ManyToManyField('Category', blank = True,)
    activated = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=300, blank=False)
    date_created = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=False)
    last_modified = models.DateTimeField(blank = True, null=True)
    activated = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Image(models.Model):
    # Putting the Images in a separate table allows for easy linking with the relevant business.
    image = models.ImageField(upload_to='images/')
    date_created = models.DateTimeField(auto_now_add=True)
    # TODO for the __str__ return the name of the business that owns the image
