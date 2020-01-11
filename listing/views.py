from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.db.models import Q
from django.contrib.auth.decorators import login_required

from rest_framework import generics
from rest_framework import filters
from datetime import datetime

from listing.models import Category
from listing.models import Listing
from listing.models import Image
from listing.serializers import ListingSerializer

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


def view_and_create_listings(request, id =""):
    if request.method == "POST":
        name = str(request.POST['name'])
        description = str(request.POST['description'])
        url = str(request.POST['url'])
        email = str(request.POST['email'])
        phone_number = str(request.POST['phone'])
        address = str(request.POST['address'])
        default_image = request.FILES['image']
        #categories = request.POST['categories']
        # TODO loop the categories as a select 

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
            #categories = categories,
            activated = True
            )
            listing.save()
            # Object saved successfully ? Notify admin
            tmpl_vars = {'message': "Listings sucessfully created"}
            return render(request, 'view.html', tmpl_vars)
        except Exception as e:
            tmpl_vars = {"error": f"There was an error attempting to create the listing \\n {e}"}
            return render (request, 'view.html', tmpl_vars)
    elif request.method == "GET":
        id = int(id)
        listing_object = get_object_or_404(Listing, id=id)
        # update the views counts
        # TODO crude and does not track for id
        listing_object.view_count + 1
        tmpl_vars = {'listing':listing_object}
        return render(request, 'view.html', tmpl_vars)


@login_required
def delete_listings(request):
    if request.method == "GET":
        id = request.GET['id']
        try:
            listing_object = Listing.objects.get(id=id)
            listing_object.delete()
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
    print('hi')
    print(request.method)
    if request.method == "POST":
        # Create category
        name = str(request.POST['name'])
        description = str(request.POST['description'])
        print(name)
        print(description)
        print(name)

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
def delete_category(request):

    if request.method == "GET":
        id = request.GET['id']
        try:
            category_object = Category.objects.get(id=id)
            category_object.delete()
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
    


def search(request):
    if request.method == "GET":
        query = str(request.GET['query'])
        query_object = Listing.objects.select_related().filter(Q(name__icontains=query) | Q(description__icontains=query))
        tmpl_vars = { 'query': query_object}
        return render(request,'search.html', tmpl_vars)

def view_all_listings(request):
    query = Listing.objects.all()
    tmpl_vars = {'query': query}
    return render(request, 'index.html', tmpl_vars)


class ListingsAPIView(generics.ListCreateAPIView):
    # API endpoint responsible for the search
    search_fields = ['name', 'description']
    filter_backends = (filters.SearchFilter,)
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer


def views_increase():

