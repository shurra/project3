from django.contrib import admin

from .models import Category, Pizza

# Register your models here.
admin.site.register(Category)
admin.site.register(Pizza)
