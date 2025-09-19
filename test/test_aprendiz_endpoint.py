from rest_framework.test import APITestCase
from django.urls import reverse

class AprendizCreateEndpointTest(APITestCase):
    def test_create_aprendiz_success(self):
        url = '/api/general/aprendices/Create-Aprendiz/create/'  # Ajusta si tienes un nombre en urls.py
        data = {
            "type_identification": "CC",
            "number_identification": 12123214332,
            "first_name": "string",
            "second_name": "string",
            "first_last_name": "string",
            "second_last_name": "string",
            "phone_number": 3102944906,
            "email": "user@soy.sena.edu.co",
            "program_id": 1,
            "ficha_id": 1
        }
        response = self.client.post(url, data, format='json')
        print(response.data)  # Para depuración
        self.assertIn(response.status_code, [200, 201])  # Ajusta según tu vista
        # Puedes agregar más asserts según la respuesta esperada

    def test_create_aprendiz_invalid_type_identification(self):
        url = '/api/general/aprendices/Create-Aprendiz/create/'
        data = {
            "type_identification": "NO_EXISTE",
            "number_identification": 12123214332,
            "first_name": "string",
            "second_name": "string",
            "first_last_name": "string",
            "second_last_name": "string",
            "phone_number": 3102983938,
            "email": "user@soy.sena.edu.co",
            "program_id": 1,
            "ficha_id": 1
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('type_identification', response.data)
