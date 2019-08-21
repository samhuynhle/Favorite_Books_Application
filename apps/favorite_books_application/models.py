from django.db import models
from apps.login_registration_app.models import *

class BookManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}

        if len(postData['title']) < 1:
            errors['title'] = "Book Title is required"
        if len(postData['description']) < 5:
            errors['description'] = "Book Description should be more than 5 characters"

        return errors

# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=45)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    favorites = models.ManyToManyField(User, related_name="favorites")
    user = models.ForeignKey(User, related_name="books")
    objects = BookManager()

    def __repr__(self):
        return f"<Book object: {self.id}>"