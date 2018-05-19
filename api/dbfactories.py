import factory
import factory.django
from factory.fuzzy import FuzzyInteger, FuzzyDate
import datetime
from .models import Booking, Price
from django.contrib.auth.models import User
import random

class BookingFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Booking
    
    date = FuzzyDate(datetime.date(2000, 1, 1))
    singleroomaval = FuzzyInteger(0, 5)
    doubleroomaval = FuzzyInteger(0, 5)

class PriceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Price
        django_get_or_create = ('booking',)
        
    booking = factory.SubFactory(BookingFactory)
    pricesingle = FuzzyInteger(0, 5000)
    pricedouble = FuzzyInteger(0, 5000)