from django.urls import path
from . import views
urlpatterns = [
    path('', views.index),
    path('home/', views.home, name = 'home'),
    path('login/', views.login_user, name ='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('change_password/', views.change_password, name='change_password'),
    path('customer/', views.customer_view, name='customer_view'),
    path('add_car/', views.add_car, name='add_car'),
    path('update/', views.update, name='update'),
]