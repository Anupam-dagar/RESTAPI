from django.test import TestCase, Client
from .models import Booking, Price
from rest_framework.test import APIRequestFactory
from rest_framework import status
from django.core.urlresolvers import reverse
import json
from concurrency.exceptions import RecordModifiedError
client = Client()


class BookingModelTestCase(TestCase):
    def setUp(self):
        self.booking = Booking(
            date='2018-05-20', singleroomaval=2, doubleroomaval=3)

    def test_model_can_create_a_booking(self):
        initial_count = Booking.objects.count()
        self.booking.save()
        final_count = Booking.objects.count()
        self.assertEqual(initial_count + 1, final_count)


class BookingApiTestCase(TestCase):
    def setUp(self):
        Booking.objects.create(
            date='2018-05-20', singleroomaval=2, doubleroomaval=3)
        Booking.objects.create(
            date='2018-05-19', singleroomaval=2, doubleroomaval=3)
        self.valid_payload = {
            'singleroomaval': 4,
            'doubleroomaval': 2
        }
        self.edit_payload = {
            'singleroomaval': 1,
            'doubleroomaval': 2
        }
        self.date_invalid_edit_payload = {
            'singleroomaval': 1,
            'doubleroomaval': 2
        }
        self.single_aval_invalid_edit_payload = {
            'date': '2018-05-20',
            'singleroomaval': 6,
            'doubleroomaval': 2
        }
        self.single_aval_neg_invalid_edit_payload = {
            'date': '2018-05-20',
            'singleroomaval': -1,
            'doubleroomaval': 2
        }
        self.double_aval_invalid_edit_payload = {
            'date': '2018-05-20',
            'singleroomaval': 1,
            'doubleroomaval': 6
        }
        self.double_aval_neg_invalid_edit_payload = {
            'date': '2018-05-20',
            'singleroomaval': 1,
            'doubleroomaval': -1
        }
        self.partialupdate_edit_payload = {
            'singleroomaval': 1,
        }

    def test_get_single_booking(self):
        response = client.get(reverse('Booking', kwargs={
            'datebooking': '2018-05-20'}))
        response_dict = {
            'date': '2018-05-20',
            'singleroomaval': 2,
            'doubleroomaval': 3
        }
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, response_dict)

    def test_valid_payload(self):
        response = client.put(reverse('Booking', kwargs={
            'datebooking': '2018-04-18'}), data=json.dumps(self.valid_payload), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_edit_payload(self):
        response = client.put(reverse('Booking', kwargs={
            'datebooking': '2018-05-20'}), data=json.dumps(self.edit_payload), content_type='application/json')
        response_dict = {
            "date": "2018-05-20",
            "singleroomaval": 1,
            "doubleroomaval": 2
        }
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, response_dict)

    def test_date_invalid_edit_payload(self):
        response = client.put(reverse('Booking', kwargs={
            'datebooking': '20-05-2018'}), data=json.dumps(self.date_invalid_edit_payload), content_type='application/json')
        response_dict = {
            "date": [
                "Date has wrong format. Use one of these formats instead: YYYY[-MM[-DD]]."
            ]
        }
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, response_dict)

    def test_single_aval_invalid_edit_payload(self):
        response = client.put(reverse('Booking', kwargs={
            'datebooking': '2018-05-20'}), data=json.dumps(self.single_aval_invalid_edit_payload), content_type='application/json')
        response_dict = {
            "non_field_errors": [
                "Room availability must be between 0 or 5"
            ]
        }
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, response_dict)

    def test_single_aval_neg_invalid_edit_payload(self):
        response = client.put(reverse('Booking', kwargs={
            'datebooking': '2018-05-20'}), data=json.dumps(self.single_aval_neg_invalid_edit_payload), content_type='application/json')
        response_dict = {
            "non_field_errors": [
                "Room availability must be between 0 or 5"
            ]
        }
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, response_dict)

    def test_double_aval_invalid_edit_payload(self):
        response = client.put(reverse('Booking', kwargs={
            'datebooking': '2018-05-20'}), data=json.dumps(self.double_aval_invalid_edit_payload), content_type='application/json')
        response_dict = {
            "non_field_errors": [
                "Room availability must be between 0 or 5"
            ]
        }
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, response_dict)

    def test_double_aval_neg_invalid_edit_payload(self):
        response = client.put(reverse('Booking', kwargs={
            'datebooking': '2018-05-20'}), data=json.dumps(self.double_aval_neg_invalid_edit_payload), content_type='application/json')
        response_dict = {
            "non_field_errors": [
                "Room availability must be between 0 or 5"
            ]
        }
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, response_dict)

    def test_partialupdate_edit_payload(self):
        response = client.put(reverse('Booking', kwargs={
            'datebooking': '2018-05-20'}), data=json.dumps(self.partialupdate_edit_payload), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class PriceApiTestCase(TestCase):
    def setUp(self):
        self.booking_get = Booking.objects.create(
            date='2018-05-20', singleroomaval=2, doubleroomaval=3)
        Price.objects.create(booking=self.booking_get,
                             pricesingle=800, pricedouble=900)
        self.booking_post = Booking.objects.create(
            date='2018-05-19', singleroomaval=1, doubleroomaval=2)
        self.valid_payload = {
            "pricesingle": 1000,
            "pricedouble": 1500
        }
        self.date_invalid_payload = {
            "pricesingle": 1000,
            "pricedouble": 1500
        }
        self.pricesingle_invalid_edit_payload = {
            "pricesingle": -1,
            "pricedouble": 1500
        }
        self.pricedouble_invalid_edit_payload = {
            "pricesingle": 1000,
            "pricedouble": -1
        }
        self.edit_payload = {
            "pricesingle": 1000
        }

    def test_get_single_price(self):
        response = client.get(
            reverse('Price', kwargs={'datebooking': '2018-05-20'}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_valid_payload(self):
        response = client.put(reverse('Price', kwargs={
            "datebooking": "2018-05-19"}), data=json.dumps(self.valid_payload), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_date_invalid_payload(self):
        response = client.put(reverse('Price', kwargs={
            "datebooking": "12-05-2018"}), data=json.dumps(self.date_invalid_payload), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_edit_payload(self):
        response = client.put(reverse('Price', kwargs={
            "datebooking": "2018-05-20"}), data=json.dumps(self.edit_payload), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_pricesingle_invalid_edit_payload(self):
        response = client.put(reverse('Price', kwargs={
            'datebooking': '2018-05-20'}), data=json.dumps(self.pricesingle_invalid_edit_payload), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_pricedouble_invalid_edit_payload(self):
        response = client.put(reverse('Price', kwargs={
            'datebooking': '2018-05-20'}), data=json.dumps(self.pricedouble_invalid_edit_payload), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class BulkOperationTest(TestCase):
    def setUp(self):
        self.double_valid_payload = {
            "from_date": "2015-10-10",
            "to_date": "2016-10-10",
            "days": ["1", "2", "3", "4", "5", "6", "7"],
            "room_type": "double",
            "price": "1199",
            "availability": 3
        }
        self.single_valid_payload = {
            "from_date": "2015-10-10",
            "to_date": "2016-10-10",
            "days": ["1", "2", "3", "4", "5", "6", "7"],
            "room_type": "single",
            "price": "1199",
            "availability": 3
        }
        self.from_date_invalid_payload = {
            "from_date": "10-10-2015",
            "to_date": "2016-10-10",
            "days": ["1", "2", "3", "4", "5", "6", "7"],
            "room_type": "single",
            "price": "1199",
            "availability": 3
        }
        self.to_date_invalid_payload = {
            "from_date": "2015-10-10",
            "to_date": "10-10-2016",
            "days": ["1", "2", "3", "4", "5", "6", "7"],
            "room_type": "single",
            "price": "1199",
            "availability": 3
        }
        self.price_invalid_payload = {
            "from_date": "2015-10-10",
            "to_date": "10-10-2016",
            "days": ["1", "2", "3", "4", "5", "6", "7"],
            "room_type": "single",
            "price": -1,
            "availability": 3
        }
        self.aval_invalid_payload = {
            "from_date": "2015-10-10",
            "to_date": "10-10-2016",
            "days": ["1", "2", "3", "4", "5", "6", "7"],
            "room_type": "single",
            "price": "1199",
            "availability": 6
        }
        self.aval_neg_invalid_payload = {
            "from_date": "2015-10-10",
            "to_date": "10-10-2016",
            "days": ["1", "2", "3", "4", "5", "6", "7"],
            "room_type": "single",
            "price": "1199",
            "availability": -1
        }
        self.invalid_date_range_payload = {
            "from_date": "2016-10-10",
            "to_date": "2015-10-10",
            "days": ["1", "2", "3", "4", "5", "6", "7"],
            "room_type": "single",
            "price": "1199",
            "availability": 3
        }

    def test_double_valid_payload(self):
        response = client.put(reverse('BulkOperation'), data=json.dumps(
            self.double_valid_payload), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_single_valid_payload(self):
        response = client.put(reverse('BulkOperation'), data=json.dumps(
            self.single_valid_payload), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_from_date_invalid_payload(self):
        response = client.put(reverse('BulkOperation'), data=json.dumps(
            self.from_date_invalid_payload), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_to_date_invalid_payload(self):
        response = client.put(reverse('BulkOperation'), data=json.dumps(
            self.to_date_invalid_payload), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_price_invalid_payload(self):
        response = client.put(reverse('BulkOperation'), data=json.dumps(
            self.price_invalid_payload), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_aval_invalid_payload(self):
        response = client.put(reverse('BulkOperation'), data=json.dumps(
            self.aval_invalid_payload), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_aval_neg_invalid_payload(self):
        response = client.put(reverse('BulkOperation'), data=json.dumps(
            self.aval_neg_invalid_payload), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_date_range_payload(self):
        response = client.put(reverse('BulkOperation'), data=json.dumps(
            self.invalid_date_range_payload), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class ConcurrencyTest(TestCase):
    def setUp(self):
        self.booking = Booking.objects.create(
            date='2018-05-20', singleroomaval=2, doubleroomaval=3)
        Price.objects.create(booking=self.booking,
                             pricesingle=800, pricedouble=900)

    def test_concurrency_booking(self):
        user_one = Booking.objects.get(date='2018-05-20')
        user_one.singleroomaval = 1
        user_two = Booking.objects.get(date='2018-05-20')
        user_two.singleroomaval = 4

        user_one.save()
        self.assertRaises(RecordModifiedError, user_two.save)

    def test_concurrency_price(self):
        user_one = Price.objects.get(booking=self.booking)
        user_one.pricesingle = 400
        user_two = Price.objects.get(booking=self.booking)
        user_two.pricesingle = 200

        user_one.save()
        self.assertRaises(RecordModifiedError, user_two.save)
