from django.urls import path
from . import views

urlpatterns = [
    path('<uuid:id>', views.index, name='index'),
    path('create-item', views.createItem, name='createItem')
]
