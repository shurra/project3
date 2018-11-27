from django.urls import path, re_path, include
from django.views.generic import TemplateView

from . import views
from orders.views import OrdersList, OrderDetail

urlpatterns = [
    path("", views.index, name="index"),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', TemplateView.as_view(template_name="orders/profile.html"), name='profile'),
    path('collect_pizza/', views.collect_pizza, name="collect_pizza"),
    path('collect_sub/', views.collect_sub, name="collect_sub"),
    path('collect_pasta/', views.collect_pasta, name="collect_pasta"),
    path('collect_salad/', views.collect_salad, name="collect_salad"),
    path('collect_dinner_platter/', views.collect_dinner_platter, name="collect_dinner_platter"),
    path('remove_from_card/', views.remove_from_card, name="remove_from_card"),
    path('submit_order/', views.submit_order, name="submit_order"),
    path('orders/', OrdersList.as_view(), name="orders"),
    path('order/<int:pk>/', OrderDetail.as_view(), name="order-detail"),
    path('order-done/', views.order_done, name="order-done")
    # path('order/(?P<pk>\d+)$', OrderDetail.as_view(), name="order-detail")
    # path('accounts/', include('django.contrib.auth.urls')),
]
