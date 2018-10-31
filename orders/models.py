from djmoney.models.fields import MoneyField
from django.db import models

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=64)

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


class Pizza(models.Model):
    PIZZA_TOPPINGS_NUM = (
        (0, 'Cheese'),
        (1, '1 topping'),
        (2, '2 toppings'),
        (3, '3 toppings'),
        (5, 'Special'),
    )
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    toppings_num = models.IntegerField(choices=PIZZA_TOPPINGS_NUM, default=0)
    small_price = MoneyField(
        decimal_places=2,
        default=0,
        default_currency='USD',
        max_digits=11,
    )
    large_price = MoneyField(
        decimal_places=2,
        default=0,
        default_currency='USD',
        max_digits=11,
    )

    def __str__(self):
        return f"{self.category} with {self.get_toppings_num_display()} costs small: {self.small_price}, large: {self.large_price}."


class DualPriceProduct(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=64)
    # size = models.CharField(max_length=10, choices=SUB_SIZES)
    small_price = MoneyField(
        decimal_places=2,
        default=0,
        default_currency='USD',
        max_digits=11,
    )
    large_price = MoneyField(
        decimal_places=2,
        default=0,
        default_currency='USD',
        max_digits=11,
    )

    def __str__(self):
        return f"{self.name} costs small: {self.small_price}, large: {self.large_price}"

    class Meta:
        abstract = True


class Sub(DualPriceProduct):
    pass


class DinnerPlatter(DualPriceProduct):
    pass


class SinglePriceProduct(models.Model):
    name = models.CharField(max_length=64)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = MoneyField(
        decimal_places=2,
        default=0,
        default_currency='USD',
        max_digits=11,
    )

    def __str__(self):
        return f"{self.category} {self.name} costs {self.price}"

    class Meta:
        abstract = True


class Pasta(SinglePriceProduct):
    pass


class Salad(SinglePriceProduct):
    pass
