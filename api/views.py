from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Booking, Price
from .serializers import BookingSerializer, PriceSerializer
from rest_framework import permissions, status
import datetime
from django.core.exceptions import ObjectDoesNotExist
import logging

logger = logging.getLogger('django')

class BookingApi(APIView):
    def get(self, request, datebooking, format=None):
        logger.info('Get request initiated.')
        try:
            booking = Booking.objects.get(date=datebooking)
            bserializer = BookingSerializer(booking)
            booking_data = bserializer.data
            logger.info("Request completed\nRequest status code: 200\nData: " + str(booking_data))
            return Response(booking_data, status=status.HTTP_200_OK)
        except:
            logger.error('No details found for given date')
            return Response({'success': False, 'message': 'No details found for given date'}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, datebooking, format=None):
        logger.info('Update request initiated.')
        request_data = request.data.copy()
        request_data['date'] = datebooking
        singleroomaval = request_data.get('singleroomaval',None)
        doubleroomaval = request_data.get('doubleroomaval',None)
        if singleroomaval is not None:
            if int(singleroomaval) > 5 or int(singleroomaval) < 0:
                return Response({"success": False,"message": "Availability must be between 0 and 5."}, status=status.HTTP_400_BAD_REQUEST)
        if doubleroomaval is not None:
            if int(doubleroomaval) > 5 or int(doubleroomaval) < 0:
                return Response({"success": False,"message": "Availability must be between 0 and 5."}, status=status.HTTP_400_BAD_REQUEST)                
        try:
            booking = Booking.objects.get(date=datebooking)
            bserializer = BookingSerializer(booking, data=request_data, partial=True)
        except:
            bserializer = BookingSerializer(data=request_data)
        if bserializer.is_valid():
            bserializer.save()
            logger.info('Request completed\nRequest status code: 200\nData: ' + str(bserializer.data))
            return Response(bserializer.data, status=status.HTTP_200_OK)
        logger.error(bserializer.errors)
        return Response(bserializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PriceApi(APIView):
    def get(self, request, datebooking, format=None):
        logger.info('GET request initiated.')
        try:
            pricebooking = Price.objects.get(booking__date=datebooking)
            pserializer = PriceSerializer(pricebooking)
            price_data = pserializer.data
            logger.info('Request completed\nRequest status code: 200\nData: ' + str(price_data))
            return Response(price_data, status=status.HTTP_200_OK)
        except:
            logger.error('No details found for given date')
            return Response({'success': False, 'message': 'No details found for given date'}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, datebooking, format=None):
        logger.info('UPDATE request initiated.')
        request_data = request.data.copy()
        request_data['booking'] = datebooking
        try:
            price = Price.objects.get(booking__date=datebooking)
            pserializer = PriceSerializer(price, data=request_data, partial=True)
        except:
            pserializer = PriceSerializer(data=request_data)            
        if pserializer.is_valid():
            pserializer.save()
            logger.info('Request completed\nRequest status code: 200\nData: ' + str(pserializer.data))
            return Response(pserializer.data, status=status.HTTP_200_OK)
        logger.error(pserializer.errors)
        return Response(pserializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BulkOperationsApi(APIView):
    def put(self, request, format=None):
        logger.info('BULK operation initiated.')
        from_date = request.data.get('from_date', None)
        to_date = request.data.get('to_date', None)
        days = request.data.get('days', None) 
        room_type = request.data.get('room_type', None)
        price = request.data.get('price', None)
        availability = request.data.get('availability', None)

        if not all([from_date, to_date, days, room_type, price, availability]):
            logger.error('Incomplete payload.')
            return Response({'success': False, 'message': 'Payload is not complete.'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            from_date = datetime.datetime.strptime(from_date, '%Y-%m-%d').date()
            to_date = datetime.datetime.strptime(to_date, '%Y-%m-%d').date()       
        except ValueError:
            logging.error('Wrong date format.')
            return Response({'success': False, 'message': 'Please enter date in YYYY-MM-DD format.'}, status=status.HTTP_400_BAD_REQUEST)
        if from_date > to_date:
            return Response({"success": False, "message": "'From date' must be before 'to date'."}, status=status.HTTP_400_BAD_REQUEST)
        delta = datetime.timedelta(days=1)
        try:
            if len(price.split('.')[1]) > 2:
                return Response({"success": False, "message": "Decimal digits in price should be less than or equals 2."}, status=status.HTTP_400_BAD_REQUEST)
        except IndexError:
            pass
        if int(availability) > 5 or int(availability) < 0:
            return Response({"success": False,"message": "Availability must be between 0 and 5."}, status=status.HTTP_400_BAD_REQUEST)
        post_booking = {}
        post_price = {}
        while from_date <= to_date:
            if str(from_date.isoweekday()) in days:
                post_booking['date'] = from_date
                post_price['booking'] = from_date
                if room_type == 'double':
                    post_booking['doubleroomaval'] = availability
                    post_price['pricedouble'] = price
                elif room_type == 'single':
                    post_booking['singleroomaval'] = availability
                    post_price['pricesingle'] = price
                try:
                    booking = Booking.objects.get(date=from_date)
                    bserializer = BookingSerializer(booking, data=post_booking, partial=True)
                except ObjectDoesNotExist:
                    bserializer = BookingSerializer(data=post_booking, partial=True)
                if bserializer.is_valid():
                    bserializer.save()
                else:
                    logger.error(bserializer.errors)
                    return Response(bserializer.errors, status=status.HTTP_400_BAD_REQUEST)
                try:
                    pricing = Price.objects.get(booking=from_date)
                    pserializer = PriceSerializer(pricing, data=post_price, partial=True)
                except ObjectDoesNotExist:
                    pserializer = PriceSerializer(data=post_price, partial=True)
                if pserializer.is_valid():
                    pserializer.save()
                else:
                    logger.error(bserializer.errors)
                    return Response(bserializer.errors, status=status.HTTP_400_BAD_REQUEST)
            from_date = from_date + delta
        logger.info('Bulk operation succeeded.')
        return Response({'success': True, 'Message': 'Operation Succeeded'}, status=status.HTTP_200_OK)

def home(request):
    return render(request, 'api/home.html',{})