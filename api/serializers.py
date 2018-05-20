from rest_framework import serializers
from .models import Booking, Price
import logging

logger = logging.getLogger('django')

class BookingSerializer(serializers.ModelSerializer):
    def validate(self, data):
        singleroomaval = data.get('singleroomaval', True)
        doubleroomaval = data.get('doubleroomaval', True)
        if singleroomaval > 5 or singleroomaval < 0 or doubleroomaval > 5 or doubleroomaval < 0:
            logger.error('Wrong room availability entered.')
            raise serializers.ValidationError('Room availability must be between 0 or 5')
        return data
    
    class Meta:
        model = Booking
        fields = ('date', 'singleroomaval', 'doubleroomaval')

class PriceSerializer(serializers.ModelSerializer):
    def validate(self, data):
        pricesingle = data.get('pricesingle', True)
        pricedouble = data.get('pricedouble', True)
        if pricesingle < 0 or pricedouble < 0:
            logger.error('Invalid price entered.')
            raise serializers.ValidationError('Invalid price entered.')
        return data
        
    class Meta:
        model = Price
        fields = ('booking', 'pricesingle', 'pricedouble')