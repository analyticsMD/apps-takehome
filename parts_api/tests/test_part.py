from django.test import Client, TestCase
from django.urls import reverse
from rest_framework import status

from parts_api.models import Part
from parts_api.tests.factories import TestParts


class PartViewTests(TestCase):
    def setUp(self):
        Part.objects.all().delete()

        self.parts = TestParts.create_batch(5)
        self.conn = Client()

    def test_update_part(self):
        test_part = self.parts[0]

        part_id = test_part.id
        previous_is_active = test_part.is_active

        endpoint = reverse("part-update", kwargs={"part_id": part_id})

        payload = "{\"is_active\": \"False\"}"
        response = self.conn.put(endpoint, payload)

        post_is_active = Part.objects.get(id=part_id).is_active

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(previous_is_active, post_is_active)
