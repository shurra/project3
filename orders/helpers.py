from decimal import *
from django.shortcuts import redirect


def search_in_list_of_dicts(search_list, key, value):
    for item in search_list:
        if item[key] == value:
            return item


def add_to_cart(request, item_to_cart):
    """
    Add to cart function - save item data to shopping cart in session
    """
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


def remove_from_card(request):
    """
    Remove item from cart in session.
    """
    request.session['cart_items'].remove(search_in_list_of_dicts(request.session['cart_items'],
                                                                 "cart_item_id",
                                                                 int(request.GET.get('cart_item_id'))))
    cart_total = sum([Decimal(item['total']) for item in request.session['cart_items']])
    request.session['cart_total'] = str(cart_total)
    request.session.modified = True
    return redirect('index')

