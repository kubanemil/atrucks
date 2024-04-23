from django.test import TestCase
from rest_framework.test import APIClient

from .models import PhoneInfo


class PhoneInfoTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        PhoneInfo.objects.create(
            abc_code=917,
            min_code=3400000,
            max_code=3500000,
            operator="MTC Operator",
            region="Moscow, Russia",
        )

    def test_get_operator_info(self):
        response = self.client.get("/api/phone_info/?phone_number=79173453223")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["phone_number"], "79173453223")
        self.assertEqual(response.data["operator"], "MTC Operator")
        self.assertEqual(response.data["region"], "Moscow, Russia")

    def test_get_operator_info_invalid_phone(self):
        response = self.client.get("/api/phone_info/?phone_number=+79173453223")
        self.assertEqual(response.status_code, 400)

        response = self.client.get("/api/phone_info/?phone_number=+7 495 739-70-00")
        self.assertEqual(response.status_code, 400)

    def test_get_operator_info_no_phone(self):
        response = self.client.get("/api/phone_info/?phone_number=7917335322")
        self.assertEqual(response.status_code, 404)
