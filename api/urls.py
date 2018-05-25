from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.home, name='home'),    
    url(r'^room/(?P<datebooking>[-\w]+)/$', views.BookingApi.as_view(), name='Booking'),
    url(r'^price/(?P<datebooking>[-\w]+)/$', views.PriceApi.as_view(), name='Price'),
    url(r'^bulk/$', views.BulkOperationsApi.as_view(), name='BulkOperation')
]