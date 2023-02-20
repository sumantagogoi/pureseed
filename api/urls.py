from django.urls import path
from .views import getAllProducts, getSingleProduct,getAllCategories,MyTokenObtainpairView,registerUser,createOrder, \
    ForgotPasswordView, ChangeForgotPassword,ValidateCoupon, getAllOrdersByUser, getSingleOrderByUser, \
        updatePassword, updateUserDetails, getProfile,editOrder, upiOrder, CheckPincode, editOrderStatus


urlpatterns =[
    path('products/', getAllProducts),
    path('product/<int:pk>/', getSingleProduct),
    path('categories/', getAllCategories),
    path('create_order/',createOrder),
    path('edit_order/',editOrder),
    path('edit_order_status/', editOrderStatus),
    path('upi_order/', upiOrder),
    path('validate_coupon/', ValidateCoupon.as_view()),   
    path('check_pincode/<str:pincode>/', CheckPincode.as_view(), name='check_pincode'),

    # Client Authentication
    path('users/login/', MyTokenObtainpairView.as_view()),
    path('users/register/', registerUser),
    path('users/forgot_password/',ForgotPasswordView.as_view()),
    path('users/change_password/', ChangeForgotPassword.as_view()),
    path('users/update_password/', updatePassword),
    path('users/update_details/', updateUserDetails),
    path('users/get_all_orders/',getAllOrdersByUser),
    path('users/order/<int:pk>/', getSingleOrderByUser),
    path('users/profile/', getProfile),
]