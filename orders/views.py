from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.views.generic.detail import SingleObjectMixin

from .models import Category, PizzaTopping, Pizza, Sub, Pasta, Salad, DinnerPlatter, Order, OrderItem, SubsAddition, UserSession

from .forms import RegisterForm, PizzaForm, SubForm, PastaForm, SaladForm, DinnerPlatterForm, OrderForm
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from django.shortcuts import get_object_or_404
from decimal import *
import json

# Create your views here.


def index(request):
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
        "pizza_form": pizza_form,
        "sub_form": sub_form,
        "pasta_form": pasta_form,
        "salad_form": salad_form,
        "dinner_platter_form": dinner_platter_form,
        "cats": categories
    }
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
            login(request, user)
            if UserSession.objects.filter(user=request.user).exists():
                user_session = json.loads(UserSession.objects.get(user=request.user).session_cart_data)
                if user_session:
                    # print(f"Login: user_session = {user_session['cart']['cart_items']}")
                    request.session['cart_items'] = user_session['cart']['cart_items']
                    request.session['cart_total'] = user_session['cart']['cart_total']
                    # request.session['cart_items'] = user_session
                    # cart_total = sum([Decimal(item['total']) for item in request.session['cart_items']])
                    # request.session['cart_total'] = str(cart_total)
                    request.session.modified = True
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "orders/login.html", {"message": "Invalid credentials."})
    else:
        return render(request, "orders/login.html", {"message": ""})


def logout_view(request):
    if 'cart_items' in request.session.keys():
        user_session_data, created = UserSession.objects.update_or_create(
            user=request.user,
            defaults={
                'session_cart_data': json.dumps({
                    'cart': {
                        'cart_items': request.session['cart_items'],
                        'cart_total': request.session['cart_total']
                    }
                })
            }
        )
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
                category=form.cleaned_data.get('field_category'),
                toppings_num=toppings_num
            )
            price = search_pizza.small_price if int(form.cleaned_data.get('size')) == 1 else search_pizza.large_price
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
            sub = form.cleaned_data.get('name')
            price = sub.small_price if int(form.cleaned_data.get('size')) == 1 else sub.large_price
            if form.cleaned_data.get('extra_cheese'):
                price += Decimal(0.50)
            if form.cleaned_data.get('addition'):
                for addition in form.cleaned_data.get('addition'):
                    price += addition.price
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
        if "cart_items" in request.session.keys() and len(request.session['cart_items']) > 0:
            # ------------------   Create order   ------------------
            order = Order(created_by=request.user, total=0)
            order.save()
            # ------------------   create order items   ----------------------
            order_total = 0
            for item in request.session['cart_items']:
                for i in range(item['quantity']):
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
    return redirect("orders")


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('change_password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'orders/change-password.html', {
        'form': form
    })
