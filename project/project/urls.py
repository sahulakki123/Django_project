"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.landing, name='landing'),
    path('signup/', views.signup, name='signup'),
    path('login/',views.login,name='login'),
    path('login/forget-password/', views.forget_password, name='forget_password'),
    path('login/forget-password/enteremail/', views.enteremail, name='enteremail'),
    path('login/forget-password/enteremail/reset/', views.reset, name='reset'),
    
    path('userdashboard/',views.userdashboard,name='userdashboard'),
    path('userdashboard/profile/', views.profile, name='profile'),
    path('userdashboard/serach/', views.search, name='search'),
    path('add-to-cart/<int:id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_page, name='cart_page'),
    path('remove-cart/<int:id>/', views.remove_cart, name='remove_cart'),
    path('paynow/<int:pk>', views.paynow, name='paynow'),
    path('payment_amount/<int:pk>', views.payment_amount, name='payment_amount'),
    path('pay_status/<int:pk>/', views.pay_status, name='pay_status'),
    
    path('logout/',views.logout,name='logout'),
    
    
    path('Adminpanel/',views.Adminpanel,name='Adminpanel'),
    path('Adminpanel/all_user/',views.all_user,name='all_user'),
    path('Adminpanel/add_rest/',views.add_rest,name='add_rest'), #
    path('Adminpanel/show_rest/',views.show_rest,name='show_rest'),#
    path('Adminpanel/save_rest/',views.save_rest,name='save_rest'),#
    path('Adminpanel/add_item/',views.add_item,name='add_item'), #
    path('Adminpanel/show_item/',views.show_item,name='show_item'),#
        
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

