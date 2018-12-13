from django.contrib import admin

from .models import Category, Pizza, PizzaTopping, Sub, Pasta, Salad, DinnerPlatter, SubsAddition, OrderItem, Order

# TODO: admin view


class PizzaAdmin(admin.ModelAdmin):
    # filter_horizontal = ("small_price", )
    list_display = ["name", "category", "toppings_num", "small_price", "large_price"]
    list_editable = ["small_price", "large_price"]
    list_filter = ["category"]


class SubAdmin(admin.ModelAdmin):
    list_display = ["name", "small_price", "large_price"]
    list_editable = ["small_price", "large_price"]


class PastaAdmin(admin.ModelAdmin):
    list_display = ["name", "price", "category"]
    list_editable = ["price", "category"]


class SubsAdditionAdmin(admin.ModelAdmin):
    list_display = ["name", "price"]
    list_editable = ["price"]


class PizzaInline(admin.TabularInline):
    model = Pizza
    extra = 0


class PastaInline(admin.TabularInline):
    model = Pasta
    extra = 0


class ToppingsInline(admin.TabularInline):
    model = PizzaTopping
    extra = 0


class SubsInline(admin.TabularInline):
    model = Sub
    extra = 0


class SaladsInline(admin.TabularInline):
    model = Salad
    extra = 0


class DinnerPlattersInline(admin.TabularInline):
    model = DinnerPlatter
    extra = 0


class CategoryAdmin(admin.ModelAdmin):
    inlines = [PizzaInline, ToppingsInline, SubsInline, PastaInline, SaladsInline, DinnerPlattersInline]


class OrderInline(admin.TabularInline):
    model = OrderItem
    readonly_fields = ["category", "name", "price"]
    extra = 0


class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderInline]
    list_display = ["created_on", "created_by", "done", "total"]
    list_filter = ["created_on", "created_by", "done"]
    actions_on_bottom = True


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ["name", "category", "price", "order"]
    # list_editable = ["category"]
    readonly_fields = ["category", "name", "price", "order"]
    list_filter = ["category", "order__created_on"]
    date_hierarchy = 'order__created_on'
    search_fields = ['name', 'order__created_on']


# Register your models here.
admin.site.register(Category, CategoryAdmin)
admin.site.register(Pizza, PizzaAdmin)
admin.site.register(PizzaTopping)
admin.site.register(Sub, SubAdmin)
admin.site.register(Pasta, PastaAdmin)
admin.site.register(Salad, PastaAdmin)
admin.site.register(DinnerPlatter, SubAdmin)
admin.site.register(SubsAddition, SubsAdditionAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(Order, OrderAdmin)
