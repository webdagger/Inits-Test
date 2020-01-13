from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist

from rest_framework import generics
from rest_framework import filters
from datetime import datetime

import bleach

from listing.models import Category
from listing.models import Listing
from listing.models import Image
from listing.serializers import ListingSerializer
from listing.forms import ListingForm
from listing.forms import CategoryForm

# Create your views here.

def login_admin(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        redirect('admin_page/')
    else:
        tmpl_vars = {"error": "The login attempt failed. Check that you are entering valid details"}
        redirect('login/', tmpl_vars)    



def create_listings(request):
    if request.method == "POST":
        form = ListingForm(request.Post)
        # basic form validation
        if form.is_valid():
            print(request.POST)
            name = bleach.clean(str(request.POST['name']))
            description = bleach.clean(str(request.POST['description']))
            url = bleach.clean(str(request.POST['url']))
            email = bleach.clean(str(request.POST['email']))
            phone_number = bleach.clean(str(request.POST['phone']))
            address = bleach.clean(str(request.POST['address']))
            default_image = request.FILES['image']
            # TODO Brute you should consider making this better. To ensure the program does not break you have to make sure 
            # the category is not strictly enforced.  Businesses can be saved without category
            chosen_categories = []
            # The categories object allows to save the object of the retrived categories as a list so it can be  passed and saved
            categories_object = []
            for key, value in request.POST.items():
                # the radio returns a list in the post request with the key as the category 
                try:
                    i = int(key)
                    chosen_categories.append(int(key))
                except ValueError:
                    # it means the key cannot be changed to a int
                    pass
            print(chosen_categories)
            for id in chosen_categories:
                try:
                    i = Category.objects.get(id=id)
                    categories_object.append(i)
                except ObjectDoesNotExist:
                    pass
        
        try:
            image_object = Image(image=default_image)
            image_object.save()
            listing = Listing(
            name = name,
            description = description,
            url = url,
            email = email,
            phone_number = phone_number,
            address = address,
            default_image = image_object,   
            activated = True,
            )
            listing.save()
            
            listing.categories.add(*categories_object)
            # Object saved successfully ? Notify admin
            tmpl_vars = {'message': "Listings sucessfully created"}
            return render(request, 'view.html', tmpl_vars)
        except Exception as e:
            tmpl_vars = {"error": f"There was an error attempting to create the listing \\n {e}"}
            return render (request, 'view.html', tmpl_vars)
    elif request.method == "GET":
        # I get all the categories and save the name in a dict of {id:'value'} and pass it as choices in the tmpl_vars 
        # Note the id's are passed so we can find out from the html which of the POST request a choice if POST['value'] can be an int
        choices = {}
        
        
        categories_object = Category.objects.all()
        for category in categories_object:
            choices.update({category.id:category.name})

        
        # TODO update the views counts
        tmpl_vars = {'choices':choices, 'form':ListingForm}
        return render(request, 'create listing.html', tmpl_vars)


@login_required
def delete_listings(request, id):
    if request.method == "GET":
        id = int(id)
        try:
            listing_object = Listing.objects.get(id=id)
            listing_object.delete()
            tmpl_vars = {'message':'sucessfully deleted listing'}
            return render("index.html", tmpl_vars)
        except Listing.DoesNotExist:
            tmpl_vars = {'error':'The listing you are trying to delete does not exist'}
            return render("index.html", tmpl_vars)
        except Exception as e:
            tmpl_vars = {'error':f'Error trying to remove that Listing check stack for more details \\n {e}'}
            return render("index.html", tmpl_vars)

@login_required
def modify_listings(request, id=""):
    if request.method == "POST":
        id = request.POST['id']
        listing_object = get_object_or_404(Listing, id=id)
        # Get the remaining data that is sent and change the last modified date
        name = str(request.POST['name'])
        description = str(request.POST['description'])
        url = str(request.POST['url'])
        email = str(request.POST['email'])
        phone_number = str(request.POST['phone'])
        address = str(request.POST['address'])
        default_image = request.FILES['image']

        #categories = request.POST['categories']
        last_modified_date = datetime.now()
        listing_object.name = name
        listing_object.description = description
        listing_object.url = url
        listing_object.email = email
        listing_object.phone_number = phone_number
        listing_object.address = address
        listing_object.default_image.image = default_image
        #listing_object.categories = categories
        listing_object.last_modified_date = last_modified_date
        listing_object.save()
        return render(request, "create.html")
                
    else:
        # Method == GET Populate the form
        id = id
        listing_object = get_object_or_404(Listing, id=id)
        tmpl_vars = {'listing':listing_object}
        return render(request, 'modify.html', tmpl_vars)

def create(request):
    return render(request, "create.html")

def create_or_view_category(request, id=""):
    if request.method == "POST":
        # Create category
        form = CategoryForm
        if form.is_valid():

            name = bleach.clean(str(request.POST['name']))
            description = bleach.clean(str(request.POST['description']))
            category_object = Category(
                name = name,
                description = description,
                activated = True,
            )
        category_object.save()
        tmpl_vars = {'message': "Category created"}
        return render(request, 'view.html',tmpl_vars )
    else:
        # GET Request to view the category
        id = int(id)
        category_object = get_object_or_404(Category, id=id)
        tmpl_vars = {'category_object': category_object}
        return render(request, 'view.html', tmpl_vars)

@login_required
def delete_category(request, id):

    if request.method == "GET":
        id = int(id)
        try:
            category_object = Category.objects.get(id=id)
            category_object.delete()
            tmpl_vars = {'message':'sucessfully deleted category'}
            return render("index.html", tmpl_vars)
        except Category.DoesNotExist:
            tmpl_vars = {'error':'The category you are trying to delete does not exist'}
            return render("index.html", tmpl_vars)
        except Exception as e:
            tmpl_vars = {'error':f'Error trying to remove that Category check stack for more details \\n {e}'}
            return render("index.html", tmpl_vars)

@login_required
def modify_category(request):
    if request.method == "POST":
        id = request.POST['id']
        category_object = get_object_or_404(Category, id=id)
        # Get the remaining data that is sent and change the last modified date
        name = str(request.POST['username'])
        description = str(request.POST['password'])
        last_modified_date = datetime.now()
        # Check to avoid trying to update srtict fields
        if name or description == "":
            tmpl_vars = {'error':"Error trying to update category"}
            return redirect("modify_categories/", tmpl_vars)
        else: 
            category_object.name = name
            category_object.description = description
            category_object.last_modified_date = last_modified_date
            category_object.save()
            return redirect(f"modify_categories/{id}")
    


def search(request, query):
    if request.method == "GET":
        query = query
        query_object = Listing.objects.select_related().filter(Q(name__icontains=query) | Q(description__icontains=query))
        tmpl_vars = { 'query': query_object}
        return render(request,'search.html', tmpl_vars)

def view_all_listings(request, id=""):
    if id:
        try:
        
            query = get_object_or_404(Listing, id=id)
            return render(request, query)
        except ValueError:
            # The id was not convertable to int
            return render(request, "index.html", {'error':f'{ValueError}, The value you are passing is not an int'})
    query = Listing.objects.all()
    tmpl_vars = {'query': query}
    return render(request, 'index.html', tmpl_vars)


class ListingsAPIView(generics.ListCreateAPIView):
    # API endpoint responsible for the search
    search_fields = ['name', 'description']
    filter_backends = (filters.SearchFilter,)
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer

