from django.db import models
from django.contrib.auth.models import User

# Create your models here.
#if you want to save blank field you need to allow it on Django and Database level. blank=True -
# will allow empty field in admin panel null=True - will allow saving NULL to the database column.

class Customer(models.Model):
    user = models.OneToOneField(User,null=True,blank=True,on_delete=models.CASCADE)
    name = models.CharField(max_length=200,null=True)
    phone = models.CharField(max_length=200,null=True)
    email = models.EmailField(max_length=200,null=True)
    profile_pic = models.ImageField(default='profile.png',null=True,blank=True)
    date_created = models.DateTimeField(auto_now_add=True,null=True)

    def __str__(self):
        return str(self.name)

class Tag(models.Model):
    name = models.CharField(max_length=200,null=True)

    def __str__(self):
        return str(self.name)

class Product(models.Model):
    CATEGORY = (
        ('Indoor','Indoor'),
        ('Out Door','Out Door')
    )

    name = models.CharField(max_length=200, null=True)
    price = models.FloatField(null=True)
    category = models.CharField(max_length=200,null=True,choices=CATEGORY)
    description = models.CharField(max_length=300,null=True,blank=True)
    tag = models.ManyToManyField(Tag)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return str(self.name)

class Order(models.Model):
    STATUS = (
        ('Pending','Pending'),
        ('Out for delivery','Out for delivery'),
        ('Delivered','Delivered')
    )
    customer = models.ForeignKey(Customer,null=True,on_delete=models.SET_NULL,  related_name='orders')
    '''on_delete=models.SET_NULL means if we delete customer his order will remain in the 
    database with no value to customer
    '''
    product = models.ForeignKey(Product,null=True,on_delete=models.SET_NULL)
    status = models.CharField(max_length=200,choices=STATUS,null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    note = models.CharField(max_length=100,null = True)

    def __str__(self):
        return str(self.status)



