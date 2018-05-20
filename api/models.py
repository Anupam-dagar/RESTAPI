from django.db import models
from concurrency.fields import IntegerVersionField
class Booking(models.Model):
    version = IntegerVersionField()
    date = models.DateField(primary_key=True)
    singleroomaval = models.IntegerField(default=5)
    doubleroomaval = models.IntegerField(default=5)    

    def __str__(self):
        return str(self.date)

    def __unicode__(self):
        return str(self.date)

class Price(models.Model):
    version = IntegerVersionField()
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, primary_key=True)
    pricesingle = models.IntegerField(default=0)
    pricedouble = models.IntegerField(default=0)

    def __str__(self):
        return str(self.booking.date)

    def __unicode__(self):
        return str(self.booking.date)        
