from rest_framework.test import APITestCase
from rest_framework import status
from ..models import Part
from ..serializers import PartSerializer


class TestPartCrud(APITestCase):

    def test_get_all(self):
        response = self.client.get('/parts/get-all')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)


    def test_create(self):
        data = {
            "name": "Heavy coil",
            "sku": "SDJDDH8223DHJ",
            "description": "Tightly wound nickel-gravy alloy spring",
            "weight_ounces": 22,
            "is_active": "1"
        }
        response = self.client.post('/parts/create', data)

        created_part = response.data
        part = Part.objects.get(pk=created_part['id'])

        self.assertEqual(part.name, 'Heavy coil')
        self.assertEqual(created_part['sku'], 'SDJDDH8223DHJ')
        self.assertEqual(created_part['weight_ounces'], 22)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


    def test_get(self):
        data = {
            "name": "Heavy coil",
            "sku": "SDJDDH8223DHJ",
            "description": "Tightly wound nickel-gravy alloy spring",
            "weight_ounces": 22,
            "is_active": "1"
        }
        created_response = self.client.post('/parts/create', data)
        created_part = created_response.data
        self.assertEqual(created_response.status_code, status.HTTP_201_CREATED)

        get_response = self.client.get(f"/parts/get/{created_part['id']}/")
        
        self.assertEqual(get_response.data['sku'], 'SDJDDH8223DHJ')
        self.assertEqual(get_response.data['description'], 'Tightly wound nickel-gravy alloy spring')


    def test_bad_create(self):
        data = {}
        created_response = self.client.post('/parts/create', data)
        self.assertEqual(created_response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_update(self):
        data = {
            "name": "Heavy coil",
            "sku": "SDJDDH8223DHJ",
            "description": "Tightly wound nickel-gravy alloy spring",
            "weight_ounces": 22,
            "is_active": "1"
        }
        created_response = self.client.post('/parts/create', data)
        created_part = created_response.data

        new_data = {
            "name": "new Heavy coil",
            "sku": "SDJDDH8223DHJ",
            "description": "new Tightly wound nickel-gravy alloy spring",
            "weight_ounces": 22,
            "is_active": "0"
        }
        put_response = self.client.put(f"/parts/update/{created_part['id']}/", new_data)
        
        self.assertEqual(put_response.data['name'], 'new Heavy coil')
        self.assertEqual(put_response.data['description'], 'new Tightly wound nickel-gravy alloy spring')
        self.assertEqual(put_response.data['is_active'], '0')


    def test_delete(self):
        data = {
            "name": "Heavy coil",
            "sku": "SDJDDH8223DHJ",
            "description": "Tightly wound nickel-gravy alloy spring",
            "weight_ounces": 22,
            "is_active": "1"
        }
        created_response = self.client.post('/parts/create', data)
        created_part = created_response.data

        delete_response = self.client.delete(f"/parts/delete/{created_part['id']}/")
        
        self.assertEqual(delete_response.status_code, status.HTTP_204_NO_CONTENT)

    def test_get_common_words(self):
        parts = Part.objects.all()
        parts.delete()

        data = {
            "name": "Heavy coil",
            "sku": "SDJDDH8223DHJ",
            "description": "Tightly wound nickel-gravy alloy spring",
            "weight_ounces": 22,
            "is_active": "1"
        }
        created_response = self.client.post('/parts/create', data)

        data = {
            "name": "Heavy coil",
            "sku": "SDJDDH8223DHJ",
            "description": "Tightly wound nickel-gravy alloy spring spring spring summer hi hi",
            "weight_ounces": 22,
            "is_active": "1"
        }
        created_response = self.client.post('/parts/create', data)

        created_response = self.client.get('/parts/common-words/5/')
        expected_response = [{'spring': 4}, {'tightly': 2}, {'wound': 2}, {'nickel-gravy': 2}, {'alloy': 2}] 
        self.assertEqual(created_response.data, expected_response)