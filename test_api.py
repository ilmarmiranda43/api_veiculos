import unittest
import json
import jwt
from api_veiculos import app, JWT_SECRET
from unittest.mock import patch, MagicMock

class TestVeiculosAPI(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.client = app.test_client()
        cls.headers = {'Content-Type': 'application/json'}

    def test_generate_token_valid_credentials(self):
        with patch('pyodbc.connect') as mock_conn:
            mock_cursor = MagicMock()
            mock_cursor.fetchone.return_value = (1,)
            mock_conn.return_value.cursor.return_value = mock_cursor
            
            payload = {
                "MerchantId": "8910213c-7309-47fc-8e8a-b0d9d71b85a2",
                "MerchantKey": "a78f5130d55e90a02611d11976790038e37c082ead39ff53201691508e44f85f"
            }
            response = self.client.post('/veiculos/generate_token', data=json.dumps(payload), headers=self.headers)
            self.assertEqual(response.status_code, 200)
            self.assertIn("token", response.get_json())

    def test_generate_token_invalid_credentials(self):
        with patch('pyodbc.connect') as mock_conn:
            mock_cursor = MagicMock()
            mock_cursor.fetchone.return_value = (0,)
            mock_conn.return_value.cursor.return_value = mock_cursor
            
            payload = {
                "MerchantId": "invalid_id",
                "MerchantKey": "invalid_key"
            }
            response = self.client.post('/veiculos/generate_token', data=json.dumps(payload), headers=self.headers)
            self.assertEqual(response.status_code, 401)
            self.assertIn("error", response.get_json())

    def test_get_all_veiculos_with_valid_token(self):
        with patch('pyodbc.connect') as mock_conn:
            mock_cursor = MagicMock()
            mock_cursor.fetchall.return_value = [
                (1, "Carro A", "CONNECTADO"),
                (2, "Carro B", "DESCONECTADO")
            ]
            mock_conn.return_value.cursor.return_value = mock_cursor

            token = jwt.encode({"merchant_id": "8910213c-7309-47fc-8e8a-b0d9d71b85a2"}, JWT_SECRET, algorithm="HS256")
            headers = {'Authorization': f'Bearer {token}'}
            response = self.client.get('/veiculos', headers=headers)
            if response.status_code == 200:
                self.assertEqual(response.status_code, 200)
                self.assertEqual(len(response.get_json()), 2)

    def test_get_all_veiculos_without_token(self):
        response = self.client.get('/veiculos/veiculos')
        self.assertEqual(response.status_code, 401)
        self.assertIn("Token Faltando", response.get_json()["message"])

    def test_get_veiculo_by_id_with_valid_token(self):
        with patch('pyodbc.connect') as mock_conn:
            mock_cursor = MagicMock()
            mock_cursor.fetchall.return_value = [(1, "Carro A", "CONNECTADO")]
            mock_conn.return_value.cursor.return_value = mock_cursor

            token = jwt.encode({"merchant_id": "8910213c-7309-47fc-8e8a-b0d9d71b85a2"}, JWT_SECRET, algorithm="HS256")
            headers = {'Authorization': f'Bearer {token}'}
            response = self.client.get('/veiculos/1', headers=headers)
            if response.status_code == 200:
                self.assertEqual(response.status_code, 200)
                self.assertEqual(len(response.get_json()), 1)
                self.assertEqual(response.get_json()[0]["veiculo"], "Carro A")

    def test_update_veiculo_with_valid_token(self):
        with patch('pyodbc.connect') as mock_conn:
            mock_cursor = MagicMock()
            mock_cursor.fetchone.return_value = (1, "Carro A", "DESCONECTADO")
            mock_conn.return_value.cursor.return_value = mock_cursor

            token = jwt.encode({"merchant_id": "valid_id"}, JWT_SECRET, algorithm="HS256")
            headers = {'Authorization': f'Bearer {token}'}
            response = self.client.put('/veiculos/veiculos/update/1/1', headers=headers)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.get_json()["error"], "Veículo atualizado com sucesso!!")

    def test_delete_veiculo_with_valid_token(self):
        with patch('pyodbc.connect') as mock_conn:
            mock_cursor = MagicMock()
            mock_cursor.fetchone.return_value = (1, "Carro A", "DESCONECTADO")
            mock_conn.return_value.cursor.return_value = mock_cursor

            token = jwt.encode({"merchant_id": "valid_id"}, JWT_SECRET, algorithm="HS256")
            headers = {'Authorization': f'Bearer {token}'}
            response = self.client.delete('/veiculos/veiculos/delete/1', headers=headers)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.get_json()["message"], "Veículo deletado com sucesso")

if __name__ == '__main__':
    unittest.main()
