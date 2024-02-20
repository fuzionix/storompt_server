from django.urls import path
from . import views

urlpatterns = [
    path('<uuid:id>', views.index, name='index'),
    path('get-item/<uuid:id>', views.getItem, name='getItem'),
    path('create-item', views.createItem, name='createItem'),
]
