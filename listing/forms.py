from django import forms
from listing.models import Category
from listing.models import Listing

class ListingForm(forms.Form):
    name = forms.CharField(max_length=1000, required=True, label='name')
    description = forms.Textarea()
    url = forms.URLInput()
    phone_number = forms.CharField(max_length=15, required=True)
    address = forms.Textarea()
    default_image = forms.ImageField(required=False)

    # We need to pass the available categories as a list to the multiple choices field.
    try:
        categories_object = Category.objects.all()
        category_choices = []
        for category in categories_object:
            category_choices.append((category.id, category.name))
        

    except Category.DoesNotExist:
        # This means tthere are no categories in the DB. we should create the from without an option for categories
        pass
    if category_choices:
        categories = forms.MultipleChoiceField(required=False, choices=tuple(category_choices))


class CategoryForm(forms.ModelForm):
    name = forms.CharField(max_length=1000, required=True)
    description = forms.Textarea()

