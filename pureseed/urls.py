
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from api.views import GoogleLogin
from django.views.generic import TemplateView





urlpatterns = [
    path('admin/', admin.site.urls),
   # path('', TemplateView.as_view(template_name='index.html')),

    path('accounts/', include('django.contrib.auth.urls')),
    path('auth/google_login/',GoogleLogin.as_view()),
    # Client Routes
    path('api/', include(('api.urls'))),
    path('', include(('shop.urls'))),

    # Admin Routes
]
urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)