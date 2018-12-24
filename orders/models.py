from django.db import models
from django.contrib.auth.models import User
# from rest_framework import serializers

# Create your models here.

User._meta.get_field('email')._unique = True


class Category(models.Model):
    name = models.CharField(max_length=64)
    is_dish = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return f"{ self.name }"


class PizzaTopping(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=64)

    def __str__(self):
        return f"{ self.name }"


class DualPriceProduct(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=64)
    small_price = models.DecimalField(max_digits=6, decimal_places=2)
    large_price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        abstract = True


class Pizza(models.Model):
    PIZZA_TOPPINGS_NUM = (
        (0, 'Cheese'),
        (1, '1 topping'),
        (2, '2 toppings'),
        (3, '3 toppings'),
        (5, 'Special'),
    )
    name = models.CharField(max_length=64)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='pizzas')
    toppings_num = models.IntegerField(choices=PIZZA_TOPPINGS_NUM, default=0)
    small_price = models.DecimalField(max_digits=6, decimal_places=2)
    large_price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f"{self.category} with {self.get_toppings_num_display()}"


class Sub(DualPriceProduct):
    pass


class DinnerPlatter(DualPriceProduct):
    pass


class SinglePriceProduct(models.Model):
    name = models.CharField(max_length=64)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f"{self.category} {self.name} costs {self.price}"

    class Meta:
        abstract = True


class Pasta(SinglePriceProduct):
    pass


class Salad(SinglePriceProduct):
    pass


class SubsAddition(models.Model):
    name = models.CharField(max_length=64)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f"{self.name} costs {self.price}"


class Order(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    done = models.BooleanField(default=False)
    total = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f"{self.created_by.username} on {self.created_on}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=500)
    # size = models.IntegerField(blank=True, null=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f"{self.name}"


class UserSession(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    session_cart_data = models.TextField()

