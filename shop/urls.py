from django.urls import path
from .import views

urlpatterns = [
#path('', TemplateView.as_view(template_name='index.html')),
path('', views.index),
path('customers/', views.customers),
path('cash-register/', views.cashReg),
path('manage-items/', views.items),
path('confirm-upi/', views.confirmUPI),
]