from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Booking, Price
from .serializers import BookingSerializer, PriceSerializer
from rest_framework import permissions, status
class BookingApi(APIView):
    def post(self, request, format=None):
        serializer = BookingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, datebooking, format=None):
        try:
            booking = Booking.objects.get(date=datebooking)
            bserializer = BookingSerializer(booking)
            booking_data = bserializer.data

            return Response(booking_data, status=status.HTTP_200_OK)
        except:
            return Response({'success': False, 'message': 'No details found for given date'}, status=status.HTTP_400_BAD_REQUEST)

class EditBookingApi(APIView):
    def post(self, request, datebooking, format=None):
        booking = Booking.objects.get(date=datebooking)
        bserializer = BookingSerializer(booking, data=request.data, partial=True)
        if bserializer.is_valid():
            bserializer.save()
            return Response(bserializer.data, status=status.HTTP_200_OK)
        return Response(bserializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PriceApi(APIView):
    def post(self, request, format=None):
        serializer = PriceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def get(self, request, datebooking, format=None):
        try:
            pricebooking = Price.objects.get(booking__date=datebooking)
            pserializer = PriceSerializer(pricebooking)
            price_data = pserializer.data

            return Response(price_data, status=status.HTTP_200_OK)
        except:
            return Response({'success': False, 'message': 'No details found for given date'}, status=status.HTTP_400_BAD_REQUEST)

class EditPriceApi(APIView):
    def post(self, request, datebooking, format=None):
        price = Price.objects.get(booking__date=datebooking)
        pserializer = PriceSerializer(price, data=request.data, partial=True)
        if pserializer.is_valid():
            pserializer.save()
            return Response(pserializer.data, status=status.HTTP_200_OK)
        return Response(pserializer.errors, status=status.HTTP_400_BAD_REQUEST)