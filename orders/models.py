from django.db import models

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=64)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Pizza(models.Model):
    PIZZA_SIZES = (
        ('S', 'Small'),
        ('L', 'Large'),
    )
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    pizza_size = models.CharField(max_length=10, choices=PIZZA_SIZES)
