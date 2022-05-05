from django.urls import path
from .views import ProductList

urlpatterns = [

    # Clienet Endpoints
    path('products/', ProductList ),
]