from django.contrib import admin

from .models import Category, Pizza, PizzaTopping, Sub, Pasta, Salad, DinnerPlatter

# Register your models here.
admin.site.register(Category)
admin.site.register(Pizza)
admin.site.register(PizzaTopping)
admin.site.register(Sub)
admin.site.register(Pasta)
admin.site.register(Salad)
admin.site.register(DinnerPlatter)
