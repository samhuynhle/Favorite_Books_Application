from django.shortcuts import render, redirect
from .models import *
from apps.login_registration_app.models import *
from django.contrib import messages

from datetime import date, datetime, timezone

# Create your views here.
def books_home(request, user_id):
    if 'user_id' not in request.session:
        request.session['user_id'] = 'logged out'
        return redirect('/')

    if request.session['user_id'] == 'logged out':
        return redirect('/')

    context = {
        'user': User.objects.get(id=request.session['user_id']),
        'all_books': Book.objects.all(),
    }
    return render(request,'favorite_books_application/books_home.html', context)

def display_book(request, book_id):
    if request.session['user_id'] == 'logged out':
        return redirect('/')

    current_book = Book.objects.get(id=book_id)
    
    context = {
        'current_user': User.objects.get(id=request.session['user_id']),
        'current_book': current_book,
        'books_favorites': current_book.favorites.all(),
    }

    return render(request, 'favorite_books_application/books_display.html', context)

def add_book(request):
    if request.session['user_id'] == 'logged out':
        return redirect('/')

    errors = Book.objects.basic_validator(request.POST)

    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request,value)
        return redirect(f"/books/{request.POST['user_id']}")
    else:
        current_user = User.objects.get(id=request.POST['user_id'])
        new_book = Book.objects.create(title= request.POST['title'], description=request.POST['description'], user=current_user)
        new_book.favorites.add(current_user)
        new_book.save()

        return redirect(f"/display_book/{new_book.id}")

def update_book(request):

    errors = Book.objects.basic_validator(request.POST)

    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request,value)
        return redirect(f"/books/{request.POST['user_id']}")
    else:
        current_book = Book.objects.get(id=request.POST['book_id'])
        current_book.title = request.POST['title']
        current_book.description = request.POST['description']
        current_book.save()    

        return redirect(f"/books/{request.POST['user_id']}")

def favorite_book(request):
    if request.session['user_id'] == 'logged out':
        return redirect('/')

    current_user = User.objects.get(id=request.POST['user_id'])
    current_book = Book.objects.get(id=request.POST['book_id'])

    current_book.favorites.add(current_user)
    current_book.save()

    return redirect(f"/books/{request.POST['user_id']}")


def unfavorite_book(request):
    if request.session['user_id'] == 'logged out':
        return redirect('/')

    current_user = User.objects.get(id=request.POST['user_id'])
    current_book = Book.objects.get(id=request.POST['book_id'])

    current_book.favorites.remove(current_user)
    current_book.save()

    return redirect(f"/books/{request.POST['user_id']}")

def delete_book(request):
    if request.session['user_id'] == 'logged out':
        return redirect('/')

    current_book = Book.objects.get(id=request.POST['book_id'])
    current_book.delete()

    return redirect(f"/books/{request.POST['user_id']}")
