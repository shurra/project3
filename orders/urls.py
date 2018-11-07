from django.urls import path, re_path, include

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    # path('accounts/', include('django.contrib.auth.urls')),
]
