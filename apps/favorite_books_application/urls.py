from django.conf.urls import url, include
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^books/(?P<user_id>[0-9]+)$', views.books_home),
    url(r'^display_book/(?P<book_id>[0-9]+)$', views.display_book),
    url(r'^add_book$', views.add_book),
    url(r'^update_book$', views.update_book),
    url(r'^favorite_book$', views.favorite_book),
    url(r'^unfavorite_book$', views.unfavorite_book),
    url(r'^delete_book$', views.delete_book),
]