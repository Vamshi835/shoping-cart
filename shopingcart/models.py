import datetime

from django.db import models
from django.utils import timezone
from datetime import datetime    

class Register(models.Model):
	Fullname=models.CharField(max_length=50)
	email=models.CharField(max_length=80,unique=True)
	password=models.CharField(max_length=15)
	phone = models.CharField(max_length=20)
	register_date = models.DateTimeField(default=datetime.now,blank=True)

class Cart(models.Model):
	id=models.AutoField(primary_key=True)
	email=models.CharField(max_length=80)
	BookId=models.CharField(max_length=100,unique=True)
	BookName=models.CharField(max_length=200,unique=True)
	Index=models.IntegerField()
	Price=models.FloatField()
	Quantity=models.IntegerField(default=1)

	def __str__(self):
		self.BookName