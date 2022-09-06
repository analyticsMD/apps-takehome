from django.test import TestCase, Client
import sqlite3
import json
from parts_api import views
from parts_api.tests.utils import HttpRequest, HttpResponse

connection = sqlite3.connect("db.sqlite3")
from ..models import Part

class PartViewTests(TestCase):
    def test_update_part(self):
        
        # part_id to test number 18
        part_id = 18
        cursor = connection.cursor()
        cursor.execute(f"SELECT * FROM part WHERE id = {part_id}") 
        rows = cursor.fetchall()

        data = {
            "name": "Heavy coil",
            "sku": "SDJDDH8223DHJF",
            "description": "Tightly wound nickel-gravy alloy spring test",
            "weight_ounces": "28",
            "is_active": "0"
        }

        c = Client()
        response = c.put(f"/part/update/{part_id}/", json.dumps(data))
        response_object = json.loads(response.content)

        cursor = connection.cursor()
        cursor.execute(f"SELECT * FROM part WHERE id = {part_id}") 
        rows = cursor.fetchall()
        if rows:
            self.assertEqual(rows[0][0], part_id)
            self.assertEqual(rows[0][2], "SDJDDH8223DHJF")
            self.assertEqual(response_object['message'], 'Part was upated successfully')


    def test_update_part_not_found(self):
        part_id = 444
        data = {
            "name": "Heavy coil",
            "sku": "SDJDDH8223DHJF",
            "description": "Tightly wound nickel-gravy alloy spring",
            "weight_ounces": "22",
            "is_active": "0"
        }

        c = Client()
        response = c.put(f"/part/update/{part_id}/", json.dumps(data))
        response_object = json.loads(response.content)

        cursor = connection.cursor()
        cursor.execute(f"SELECT * FROM part WHERE id = {part_id}") 
        rows = cursor.fetchall()
        if not rows:
            self.assertEqual(response_object['message'], 'Part id 444 not found')
            self.assertEqual(response.status_code, 404)
