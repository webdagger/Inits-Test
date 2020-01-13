"""inits_test URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.urls import path
from django.conf import settings
from listing import views as listing_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/', listing_views.view_all_listings, name="view_all_listings"),
    path('create/', listing_views.create, name="create"),
    url(r'create_listing/', listing_views.create_listings, name="create_listings"),
    url(r'create_category/', listing_views.create_or_view_category, name="create_or_view_category"),
    url(r'view_listing/(?P<id>\d+)$', listing_views.view_all_listings, name="view_all_listings"),
    url(r'view_category/(?P<id>\d+)$', listing_views.create_or_view_category, name="create_or_view_category"),
    url(r'modify_listing/(?P<id>\d+)$', listing_views.modify_listings, name="modify_listings"),
    url(r'modify_listing/', listing_views.modify_listings, name="modify_listings"),
    url(r'modify_category/(?P<id>\d+)$', listing_views.modify_category, name="modify_category"),
    url(r'delete_listing/(?P<id>\d+)$', listing_views.delete_listings, name="delete_listing"),
    url(r'search/(?P<query>)$', listing_views.search, name="search"),



    path('searchapi/', listing_views.ListingsAPIView.as_view()),

]

if settings.DEBUG:
    from django.views.static import serve
    urlpatterns += url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
