from django.db import models

# Create your models here.

class Usersign(models.Model):
    Name=models.CharField(max_length=40)
    Email=models.EmailField()
    Contact=models.BigIntegerField()
    Password=models.CharField(max_length=20)
    CPassword=models.CharField(max_length=20,null=True)
    
    
class Restaurant(models.Model):
    restaurantname = models.CharField(max_length=100)
    restaurantcontact = models.BigIntegerField()
    restaurantaddress = models.TextField()
    images=models.ImageField(upload_to='images/')
    
class Item(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    itemname = models.CharField(max_length=100)
    itemprice = models.IntegerField()
    itemdesc = models.TextField()
    itemimage = models.ImageField(upload_to='items/')
    itemcategory = models.CharField(max_length=50)
    rating = models.FloatField(default=0)
    is_available = models.BooleanField(default=True)
    

class Cart(models.Model):
    user = models.ForeignKey(Usersign, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    
class Order(models.Model):
    order_id = models.CharField(max_length=100)
    amount = models.IntegerField()
    rezorpay = models.CharField(max_length=100, blank=True)
    patment_status =models.BooleanField(default=False)
    