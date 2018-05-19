from rest_framework import serializers
from .models import Booking, Price

class BookingSerializer(serializers.ModelSerializer):
    def validate(self, data):
        singleroomaval = data.get('singleroomaval')
        doubleroomaval = data.get('doubleroomaval')
        if singleroomaval > 5 or singleroomaval < 0 or doubleroomaval > 5 or doubleroomaval < 0:
            raise serializers.ValidationError('Room availability must be between 0 or 5')
        return data
        
    class Meta:
        model = Booking
        fields = ('date', 'singleroomaval', 'doubleroomaval')

class PriceSerializer(serializers.ModelSerializer):
    def validate(self, data):
        pricesingle = data.get('pricesingle')
        pricedouble = data.get('pricedouble')
        if pricesingle < 0 or pricedouble < 0:
            raise serializers.ValidationError('Invalid price entered.')
        return data
        
    class Meta:
        model = Price
        fields = ('booking', 'pricesingle', 'pricedouble')