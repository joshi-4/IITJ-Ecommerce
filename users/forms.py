from django import forms
from users import models

class ItemForm(forms.ModelForm):
	class Meta:
		model = models.item
		fields = ('title', 'price', 'description', 'category', 'image')