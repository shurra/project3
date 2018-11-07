from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect

from .models import Category, PizzaTopping, Pizza, Sub, Pasta, Salad, DinnerPlatter

from .forms import RegisterForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse

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


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            print(f"User = {user}")
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=form.cleaned_data.get('username'), password=raw_password)
            login(request, user)
            return redirect('index')
    else:
        form = RegisterForm()
    return render(request, 'orders/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "orders/login.html", {"message": "Invalid credentials."})
    else:
        return render(request, "orders/login.html", {"message": ""})


def logout_view(request):
    logout(request)
    return redirect('index')
