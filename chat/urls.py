from django.urls import path
from . import views

urlpatterns = [
    path('<uuid:id>', views.index, name='index'),
    path('get-item/<uuid:id>', views.get_item, name='get_item'),
    path('create-item', views.create_item, name='create_item'),
]
