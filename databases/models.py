from django import forms
from django.core.validators import validate_email
from django.db import models

# Create your models here.
class Invest(models.Model):
    quantity = models.IntegerField()
    PL = models.FloatField()
    Invested_Amt = models.FloatField()
    Purchased_Value = models.FloatField()
    id = models.IntegerField(primary_key=True)
    Stock_ISN = models.IntegerField()
class Stock(models.Model) :
    sector = models.CharField(max_length=100000)
    longBusinessSummary = models.CharField(max_length=100000)
    stock_name = models.CharField(max_length=1000)
    ISIN = models.IntegerField(primary_key=True)
    volume = models.IntegerField()
    Avg_traded_price = models.FloatField()
    lower_ckt =  models.FloatField()
    upper_ckt =  models.FloatField()
    value =  models.FloatField()
    growth =  models.FloatField()
    company_name = models.IntegerField()
class Investor(models.Model):
    UserName = models.CharField(max_length=1000,primary_key=True,unique=True)
    F_Name = models.CharField(max_length=1000,unique=True)
    L_Name = models.CharField(max_length=1000,unique=True)
    Email = models.CharField(max_length=1000,validators=[validate_email],unique=True)
    Contact_no = models.CharField(max_length=13,unique=True)
    Pan_card_no = models.CharField(max_length=1000,unique=True)
    Address_line1 = models.CharField(max_length=1000)
    Address_line2 =models.CharField(max_length=1000)
    State = models.CharField(max_length=1000)
    city = models.CharField(max_length=1000)
    District = models.CharField(max_length=1000)
    Pin_code = models.IntegerField()
class Bank(models.Model):
    Account_no = models.CharField(primary_key=True,max_length=1000)
    Username = models.ForeignKey(Investor,on_delete=models.CASCADE)
    IFSC_code = models.CharField(max_length=1000)
    Branch = models.CharField(max_length=1000)
    Name = models.CharField(max_length=1000)
    Current_amount = models.IntegerField()
class Company(models.Model):
    Name = models.CharField(primary_key=True,max_length=1000)
    Website_link = models.CharField(max_length=1000)
    CEO = models.CharField(max_length=1000)
    Revenue = models.IntegerField()
    Parent_org = models.CharField(max_length=1000)
class Company_category(models.Model):
    category = models.CharField(max_length=1000)
    Compnay_name = models.CharField(primary_key=True,max_length=1000)
