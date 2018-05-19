from django.contrib import admin
from .models import Booking, Price
# Register your models here.
class PriceAdmin(admin.ModelAdmin):
    readonly_fields = ('booking',)
class BookingAdmin(admin.ModelAdmin):
    readonly_fields = ('date',)
admin.site.register(Booking, BookingAdmin)
admin.site.register(Price, PriceAdmin)