from django.urls import path
from .views import getAllProducts, getSingleProduct,getAllCategories,MyTokenObtainpairView,registerUser


urlpatterns =[
    path('products/', getAllProducts),
    path('product/<int:pk>/', getSingleProduct),
    path('categories/', getAllCategories),

    # Client Authentication
    path('users/login/', MyTokenObtainpairView.as_view()),
    path('users/register/', registerUser),
]