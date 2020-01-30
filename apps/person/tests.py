from django.test import TestCase
from rest_framework.test import APIClient
import os
from django.conf import settings


class PersonTest(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        response = self.client.post('/person/', {'name': 'admin', 'last_name': 'admin'})
        self.admin_id = response.data['id']
        response = self.client.post('/person/', {'name': 'user', 'last_name': 'user'})
        self.user_id = response.data['id']

    def test_create_list_retrieve(self):
        response1 = self.client.post('/person/', {'last_name': 'Person 1 lastname'})
        response2 = self.client.post('/person/', {'name': 'Person 1'})
        response3 = self.client.post('/person/')
        self.assertEquals(response1.status_code, response2.status_code, response3.status_code)
        self.assertTrue(response1.status_code == 400)

        response = self.client.get('/person/')
        self.assertTrue(response.status_code == 200)
        self.assertEqual(len(response.data), 2)

        response = self.client.post('/person/', {'name': 'Person 1', 'last_name': 'Person 1 lastname'})
        person_id = response.data['id']
        self.assertEqual(len(person_id), 36)
        self.assertEqual(response.status_code, 201)

        response = self.client.get('/person/')
        self.assertEqual(len(response.data), 3)

        response = self.client.get(f'/person/{self.admin_id}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], 'admin')
        self.assertEqual(response.data['last_name'], 'admin')
        self.assertEqual(response.data['has_vector'], False)

    def test_delete(self):
        response = self.client.delete(f'/person/{self.user_id}/')
        self.assertEqual(response.status_code, 204)
        response = self.client.get('/person/')
        self.assertEqual(len(response.data), 1)

    def test_update(self):
        image_path = os.path.join(settings.BASE_DIR, 'apps', 'person', 'data', 'first.jpg')
        with open(image_path, 'rb') as f:
            response = self.client.put(f'/person/{self.admin_id}/', {'vector': f})
        self.assertEqual(response.data['has_vector'], True)
        self.assertEqual(response.status_code, 200)

        response = self.client.put(f'/person/{self.admin_id}/')
        self.assertEqual(response.status_code, 400)

    def test_compare(self):
        image1_path = os.path.join(settings.BASE_DIR, 'apps', 'person', 'data', 'first.jpg')
        image2_path = os.path.join(settings.BASE_DIR, 'apps', 'person', 'data', 'second.jpg')

        response = self.client.post('/person/compare/')
        self.assertEqual(response.status_code, 400)

        response = self.client.post('/person/compare/', {'person1': self.admin_id, 'person2': self.user_id})
        self.assertEqual(response.status_code, 400)

        with open(image1_path, 'rb') as f:
            self.client.put(f'/person/{self.admin_id}/', {'vector': f})

        with open(image2_path, 'rb') as f:
            self.client.put(f'/person/{self.user_id}/', {'vector': f})

        response = self.client.post('/person/compare/', {'person1': self.admin_id, 'person2': self.user_id})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(type(response.data['result']), float)
