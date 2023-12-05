from django import forms

class ProductForm(forms.Form):
    id = forms.IntegerField()
    product_name = forms.CharField(max_length=100)
    price = forms.FloatField()