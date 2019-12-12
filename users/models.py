from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class account(models.Model):

	address = models.CharField(max_length = 256)
	phone_num = models.CharField(max_length = 13)
	name = models.CharField(max_length = 100)
	user = models.OneToOneField(User, on_delete = models.CASCADE)

	def __str__(self):
		return self.name


CATEGORY_CHOICES = (
		('CY', 'cycle'),
		('BO', 'books'),
		('WS', 'workshop'),
		('ED', 'eng. design'),
		('CL', 'clothes'),
		('OT', 'others')
	)


class item(models.Model):

	title = models.CharField(max_length = 100, unique = True)
	createdAt = models.DateTimeField(auto_now_add = True)
	price = models.FloatField()
	description = models.TextField()
	image = models.ImageField(upload_to= 'images/')
	category = models.CharField(choices = CATEGORY_CHOICES, max_length = 40)
	owner =  models.ForeignKey('account', on_delete = models.CASCADE)

	def __str__(self):
		return self.title
