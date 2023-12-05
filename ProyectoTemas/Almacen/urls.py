from django.urls import path
from . import views
urlpatterns = [
    path('', views.productlist, name = 'index'),
    path('addproduct', views.addproduct, name='addproduct'),
    path('updateproduct/<int:id>', views.updateproduct, name = 'updateproduct'),
    path('deleteproduct/<int:id>', views.deleteproduct, name='deleteproduct')
]