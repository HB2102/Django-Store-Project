from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('payment_success', views.payment_success, name='payment_success'),
    path('checkout', views.checkout, name='checkout'),
    path('billing_info', views.billing_info, name='billing_info'),

]

# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


