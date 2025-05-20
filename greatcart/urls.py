from django.contrib import admin
from django.urls import path, include
from . import views 
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name = 'home'),
    path('store/',include('store.urls')),
    path('cart/',include('carts.urls')),
    path('accounts/',include('accounts.urls')),
<<<<<<< HEAD
    # path('cart/',include('carts.urls')),
=======

    # ORDERS
    path('orders/', include('orders.urls')),
>>>>>>> 88c44cc (Some Changes are done)
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
