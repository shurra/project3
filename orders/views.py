from django.http import HttpResponse
from django.shortcuts import render

from .models import Category, PizzaTopping, Pizza, Sub, Pasta, Salad, DinnerPlatter


# Create your views here.
def index(request):
    # return HttpResponse("Project 3: TODO")
    cat_pks = [1, 2, 8, 3, 4, 5, 6]
    categories_dict = Category.objects.in_bulk(cat_pks)
    categories = [categories_dict[pk] for pk in cat_pks]
    cat_products = []
    for c in categories:
        if c.name.find("Pizza"):
            products = Pizza.objects.filter(category__name=c.name)
            # cat_products.append({"name": c.name, "products": products})
        if c.name == "Toppings":
            products = PizzaTopping.objects.filter(category__name=c.name)
        if c.name == "Subs":
            products = Sub.objects.filter(category__name=c.name)
        if c.name == "Pasta":
            products = Pasta.objects.filter(category__name=c.name)
        if c.name == "Salads":
            products = Salad.objects.filter(category__name=c.name)
        if c.name == "Dinner Platters":
            products = DinnerPlatter.objects.filter(category__name=c.name)

        cat_products.append({"name": c.name, "products": products})
    context = {
        "categories": cat_products
    }
    return render(request, "orders/menu.html", context)
