from django.contrib import admin

# Register your models here.
from listing.models import Listing
from listing.models import Image
from listing.models import Category

admin.site.register(Listing)
admin.site.register(Image)
admin.site.register(Category)