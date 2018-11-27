from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.views.generic.detail import SingleObjectMixin

from .models import Category, PizzaTopping, Pizza, Sub, Pasta, Salad, DinnerPlatter, Order, OrderItem, SubsAddition

from .forms import RegisterForm, PizzaForm, SubForm, PastaForm, SaladForm, DinnerPlatterForm, OrderForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.shortcuts import get_object_or_404
from decimal import *

# Create your views here.


def index(request):
    # print(f"Request:{dir(request)}")
    # print(f"Request method = {request.method}")
    # print(f"{request.session.keys()}")
    # return HttpResponse("Project 3")
    cat_pks = [1, 2, 8, 3, 4, 5, 6]
    categories_dict = Category.objects.in_bulk(cat_pks)
    categories = [categories_dict[pk] for pk in cat_pks]
    cat_products = []
    products = []
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
    pizza_form = PizzaForm()
    sub_form = SubForm()
    pasta_form = PastaForm()
    salad_form = SaladForm()
    dinner_platter_form = DinnerPlatterForm()
    context = {
        # "categories": cat_products,
        "pizza_form": pizza_form,
        "sub_form": sub_form,
        "pasta_form": pasta_form,
        "salad_form": salad_form,
        "dinner_platter_form": dinner_platter_form,
        # "cart_items": request.session.get('cart_items')
        # "pizzas": Pizza.objects.all(),
        "cats": categories
    }
    if request.session.get('cart_items'):
        print(f"Session data for shopping cart = {request.session['cart_items']}, expire at {request.session.get_expiry_date()}")
    return render(request, "orders/menu.html", context)


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
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
            # TODO: Load shopping cart from db to session!
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "orders/login.html", {"message": "Invalid credentials."})
    else:
        return render(request, "orders/login.html", {"message": ""})


def logout_view(request):
    # TODO: Save shopping cart from session to db!
    logout(request)
    return redirect('index')


@login_required(login_url='/login/')
def collect_pizza(request):
    if request.method == "POST":
        form = PizzaForm(request.POST)
        if form.is_valid():
            toppings_num = form.cleaned_data.get('toppings').count()
            if toppings_num == 4:
                toppings_num = 5
            search_pizza = Pizza.objects.get(
                # category__name=Category.objects.get(name=form.cleaned_data.get('field_category')).name,
                category=form.cleaned_data.get('field_category'),
                toppings_num=toppings_num
            )
            price = search_pizza.small_price if int(form.cleaned_data.get('size')) == 1 else search_pizza.large_price
            # TODO: додавати id
            item_to_cart = {'product_id': search_pizza.id,
                            'name': search_pizza.category.name,
                            'category': search_pizza.category.id,
                            'size': dict(PizzaForm.SIZES)[form.cleaned_data["size"]],
                            'price': str(price),
                            'toppings': [t.name for t in form.cleaned_data.get('toppings')],
                            'quantity': form.cleaned_data.get('quantity'),
                            'total': str(price * int(form.cleaned_data.get('quantity')))}
            add_to_cart(request, item_to_cart)
    else:
        form = PizzaForm()
        return render(request, "orders/pizza-form.html", {'form': form})
    return HttpResponseRedirect(reverse("index"))


@login_required(login_url='/login/')
def collect_sub(request):
    if request.method == "POST":
        form = SubForm(request.POST)
        if form.is_valid():
            print(f"collect_sub POST = {form.cleaned_data}")
            print(f"collect_sub name = {form.cleaned_data.get('name')}")
            sub = form.cleaned_data.get('name')
            price = sub.small_price if int(form.cleaned_data.get('size')) == 1 else sub.large_price
            print(f"Price = {price}")
            if form.cleaned_data.get('extra_cheese'):
                price += Decimal(0.50)
            if form.cleaned_data.get('addition'):
                for addition in form.cleaned_data.get('addition'):
                    price += addition.price
            print(f"Price = {price}")
            item_to_cart = {'product_id': sub.id,
                            'category': sub.category.id,
                            'name': sub.name,
                            'size': dict(SubForm.SIZES)[form.cleaned_data["size"]],
                            'price': str(price),
                            'additions': [t.name for t in form.cleaned_data.get('addition')],
                            'extra_cheese': form.cleaned_data.get('extra_cheese'),
                            'quantity': form.cleaned_data.get('quantity'),
                            'total': str(price * int(form.cleaned_data.get('quantity')))}
            add_to_cart(request, item_to_cart)
            # print(f"Item to cart = {item_to_cart}")
    return HttpResponseRedirect(reverse("index"))


@login_required(login_url='/login/')
def collect_pasta(request):
    if request.method == "POST":
        form = PastaForm(request.POST)
        if form.is_valid():
            pasta = form.cleaned_data.get('name')
            price = pasta.price
            item_to_cart = {'product_id': pasta.id,
                            'name': pasta.name,
                            'category': pasta.category.id,
                            'price': str(price),
                            'quantity': form.cleaned_data.get('quantity'),
                            'total': str(price * int(form.cleaned_data.get('quantity')))}
            add_to_cart(request, item_to_cart)
    return HttpResponseRedirect(reverse("index"))


@login_required(login_url='/login/')
def collect_salad(request):
    if request.method == "POST":
        form = SaladForm(request.POST)
        if form.is_valid():
            salad = form.cleaned_data.get('name')
            price = salad.price
            item_to_cart = {'product_id': salad.id,
                            'name': salad.name,
                            'category': salad.category.id,
                            'price': str(price),
                            'quantity': form.cleaned_data.get('quantity'),
                            'total': str(price * int(form.cleaned_data.get('quantity')))}
            add_to_cart(request, item_to_cart)
    return HttpResponseRedirect(reverse("index"))


@login_required(login_url='/login/')
def collect_dinner_platter(request):
    if request.method == "POST":
        form = DinnerPlatterForm(request.POST)
        if form.is_valid():
            dinner_platter = form.cleaned_data.get('name')
            price = dinner_platter.small_price if int(form.cleaned_data.get('size')) == 1 else dinner_platter.large_price
            item_to_cart = {'product_id': dinner_platter.id,
                            'category': dinner_platter.category.id,
                            'name': dinner_platter.name,
                            'size': dict(DinnerPlatterForm.SIZES)[form.cleaned_data["size"]],
                            'price': str(price),
                            'quantity': form.cleaned_data.get('quantity'),
                            'total': str(price * int(form.cleaned_data.get('quantity')))}
            add_to_cart(request, item_to_cart)
            # print(f"Item to cart = {item_to_cart}")
    return HttpResponseRedirect(reverse("index"))


@login_required(login_url='/login/')
def add_to_cart(request, item_to_cart):
    if not request.session.get('cart_items'):
        cart_items = []
        item_id = 1
    else:
        cart_items = request.session.get('cart_items')
        item_id = max([item['cart_item_id'] for item in request.session.get('cart_items')]) + 1
    item_to_cart['cart_item_id'] = item_id
    cart_items.append(item_to_cart)
    request.session['cart_items'] = cart_items
    cart_total = sum([Decimal(item['total']) for item in cart_items])
    request.session['cart_total'] = str(cart_total)
    request.session.modified = True
    print(f"item added = {item_to_cart}")


@login_required(login_url='/login/')
def remove_from_card(request):
    request.session['cart_items'].remove(search_in_list_of_dicts(request.session['cart_items'],
                                                                 "cart_item_id",
                                                                 int(request.GET.get('cart_item_id'))))
    cart_total = sum([Decimal(item['total']) for item in request.session['cart_items']])
    request.session['cart_total'] = str(cart_total)
    request.session.modified = True
    return redirect('index')


def search_in_list_of_dicts(search_list, key, value):
    for item in search_list:
        if item[key] == value:
            return item


@login_required(login_url='/login/')
def submit_order(request):
    if request.user.is_authenticated:
        print(f"User = {request.user.username}")
        if "cart_items" in request.session.keys() and len(request.session['cart_items']) > 0:
            # ------------------   Create order   ------------------
            order = Order(created_by=request.user, total=0)
            order.save()
            print(f"Order created by {order.created_by}, created on {order.created_on}, done status = {order.done}")
            # ------------------   create order items   ----------------------
            print(f"Items number = {len(request.session['cart_items'])}")
            order_total = 0
            for item in request.session['cart_items']:
                for i in range(item['quantity']):
                    print(f"order request cart item = {item}")
                    product_cat = Category.objects.get(id__exact=item['category'])
                    # print(f"item category = {product_cat}")
                    if "Pizza" in product_cat.name:
                        cat_product_class = Pizza
                        product = cat_product_class.objects.get(pk=item['product_id'])
                        size = 1 if item['size'] == "Small" else 2
                        order_item_name = item['size'] + " " + product.name
                        if item['toppings']:
                            order_item_name += " with " + ", ".join(item['toppings'])
                        price = product.small_price if size == 1 else product.large_price
                        order_item = OrderItem(order=order, category=product_cat, name=order_item_name, price=price)
                    elif "Sub" in product_cat.name:
                        cat_product_class = Sub
                        product = cat_product_class.objects.get(pk=item['product_id'])
                        size = 1 if item['size'] == "Small" else 2
                        order_item_name = item['size'] + " " + product.name
                        price = product.small_price if size == 1 else product.large_price
                        if item['additions']:
                            order_item_name += " with " + ", ".join(item['additions'])
                            for add in item['additions']:
                                item_addition = SubsAddition.objects.get(name=add)
                                price += item_addition.price
                        if item['extra_cheese']:
                            order_item_name += ", Extra cheese"
                            price += Decimal(0.50)
                        order_item = OrderItem(order=order, category=product_cat, name=order_item_name, price=price)
                    elif "Pasta" in product_cat.name:
                        cat_product_class = Pasta
                        product = cat_product_class.objects.get(pk=item['product_id'])
                        order_item_name = product.name
                        price = product.price
                        order_item = OrderItem(order=order, category=product_cat, name=order_item_name, price=price)
                    elif "Salad" in product_cat.name:
                        cat_product_class = Salad
                        product = cat_product_class.objects.get(pk=item['product_id'])
                        order_item_name = product.name
                        price = product.price
                        order_item = OrderItem(order=order, category=product_cat, name=order_item_name, price=price)
                    elif "Dinner Platters" in product_cat.name:
                        cat_product_class = DinnerPlatter
                        product = cat_product_class.objects.get(pk=item['product_id'])
                        size = 1 if item['size'] == "Small" else 2
                        order_item_name = item['size'] + product.name
                        price = product.small_price if size == 1 else product.large_price
                        order_item = OrderItem(order=order, category=product_cat, name=order_item_name, price=price)

                    print(f"Order item name = {order_item_name}, price = {price}")
                    print(f"Order item object = {order_item}")
                    order_item.save()
                    order_total += price
            order.total = order_total
            order.save()
            del request.session['cart_items']
            del request.session['cart_total']
    return redirect('orders')


class OrdersList(LoginRequiredMixin, ListView):
    login_url = '/login/'

    context_object_name = "user_orders"

    def get_queryset(self):
        if self.request.user.is_staff:
            return Order.objects.all().order_by('-created_on')
        else:
            return Order.objects.filter(created_by=self.request.user).order_by('-created_on')


class OrderDetail(LoginRequiredMixin, DetailView):
    login_url = '/login/'
    context_object_name = 'order'

    queryset = Order.objects.all()
    get_allow_empty = True

    def get_context_data(self, **kwargs):
        context = super(OrderDetail, self).get_context_data(**kwargs)
        context['form'] = OrderForm
        return context


@login_required(login_url='/login/')
def order_done(request):
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            # order = Order.objects.get(pk=id)
            order = get_object_or_404(Order, pk=int(form.data['order_id']))
            order.done = True
            order.save()
            # order = None
            print(f"Order Done order = {order}, order id = {int(form.data['order_id'])}, done = {form.cleaned_data.get('done')}")
    return redirect("orders")
