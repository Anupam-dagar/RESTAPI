from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.home, name='home'),    
    url(r'^getroomdata/(?P<datebooking>[-\w]+)/$', views.BookingApi.as_view(), name='GetBooking'),
    url(r'^getroompricedata/(?P<datebooking>[-\w]+)/$', views.PriceApi.as_view(), name='GetPrice'),
    url(r'^updateroomdata/(?P<datebooking>[-\w]+)/$', views.BookingApi.as_view(), name='UpdateBooking'),
    url(r'^updateroompricedata/(?P<datebooking>[-\w]+)/$', views.PriceApi.as_view(), name='UpdatePrice'),
    url(r'^bulk/$', views.BulkOperationsApi.as_view(), name='BulkOperation')
]