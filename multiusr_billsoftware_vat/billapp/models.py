from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    is_company = models.BooleanField(default=0)

class Company(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,null=True,blank=True)
    company_code = models.CharField(max_length=100,null=True,blank=True)
    company_name = models.CharField(max_length=100,null=True,blank=True)
    address = models.CharField(max_length=100,null=True,blank=True)
    city = models.CharField(max_length=100,null=True,blank=True)
    state = models.CharField(max_length=100,null=True,blank=True)
    country = models.CharField(max_length=100,null=True,blank=True)
    contact = models.CharField(max_length=100,null=True,blank=True)
    pincode = models.IntegerField(null=True,blank=True)
    pan_number = models.CharField(max_length=255,null=True,blank=True)
    gst_type = models.CharField(max_length=255,null=True,blank=True)
    gst_no = models.CharField(max_length=255,null=True,blank=True)
    profile_pic = models.ImageField(null=True,blank = True,upload_to = 'image/company')

class Employee(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,null=True,blank=True)
    contact = models.CharField(max_length=100,null=True,blank=True)
    company_code = models.CharField(max_length=100,null=True,blank=True)
    is_approved = models.BooleanField(default=0)
    profile_pic = models.ImageField(null=True,blank = True,upload_to = 'image/employee')

class Item(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=True,blank=True)
    CHOICES = [
        ('Goods', 'Goods'),
        ('Service', 'Service'),
    ]
    itm_type = models.CharField(max_length=20, choices=CHOICES)
    itm_name = models.CharField(max_length=255)
    itm_hsn = models.PositiveIntegerField(null=True)
    itm_unit = models.CharField(max_length=255)
    itm_taxable = models.CharField(max_length=255)
    itm_vat = models.CharField(max_length=255,null=True)
    itm_sale_price = models.PositiveIntegerField()
    itm_purchase_price = models.PositiveBigIntegerField()
    itm_stock_in_hand = models.PositiveBigIntegerField(default=0)
    itm_at_price = models.PositiveBigIntegerField(default=0)
    itm_date = models.DateField()

class UnitModel(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=True,blank=True)
    unit_name = models.CharField(max_length=255)