from django.urls import path
from .views import getAllProducts, getSingleProduct,MyTokenObtainpairView,registerUser


urlpatterns =[
    path('products/', getAllProducts),
    path('product/<int:pk>/', getSingleProduct),

    # Client Authentication
    path('users/login/', MyTokenObtainpairView.as_view()),
    path('users/register/', registerUser),
]