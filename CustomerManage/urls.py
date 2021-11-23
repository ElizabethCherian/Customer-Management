from django.contrib import admin
from django.urls import path
from CustomerManage import views






app_name='CustomerManage'

urlpatterns = [
   
    path('home/',views.home,name="home"),
    path('products/',views.Products,name="products"),
    path('customer/<int:custid>/',views.customer,name="customer"),
    path('create-order/',views.CreateOrder,name="create-order"),
    path('update-order/<int:ordid>/',views.UpdateOrder,name="update-order"),
    path('delete-order/<int:ordid>/',views.DeleteOrder,name="delete-order"),
    path('create-customer/',views.CreateCustomer,name="create-customer"),
    path('update-customer/<int:custid>/',views.UpdateCustomer,name="update-customer"),
    path('place-order/<int:custid>/',views.PlaceOrder,name="place-order"),
    path('register/',views.Register,name="register"),
    path('login/',views.Login,name="login"),
    path('logout/',views.Logout,name="logout"),
    path('user/',views.Userpage,name="user"),
    path('useraccount/',views.Useraccount,name="user-account"),


]