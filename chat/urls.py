from django.urls import path
from . import views

urlpatterns = [
    path('<uuid:id>', views.index, name='index')
]
