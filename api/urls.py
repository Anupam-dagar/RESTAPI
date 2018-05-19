from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^getroomdata/(?P<datebooking>[-\w]+)/$', views.BookingApi.as_view(), name='GetBooking'),
    url(r'^getroompricedata/(?P<datebooking>[-\w]+)/$', views.PriceApi.as_view(), name='GetPrice'),
    url(r'^postroomdata/$', views.BookingApi.as_view(), name='CreateBooking'),
    url(r'^postroompricedata/$', views.PriceApi.as_view(), name='CreatePricing'),
    url(r'^updateroomdata/(?P<datebooking>[-\w]+)/$', views.EditBookingApi.as_view(), name='UpdateBooking'),
    url(r'^updateroompricedata/(?P<datebooking>[-\w]+)/$', views.EditPriceApi.as_view(), name='UpdatePrice'),    
]