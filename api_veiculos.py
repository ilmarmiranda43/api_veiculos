from flask import Flask, request, jsonify
from flask_restx import Api, Resource, fields
import json
import pyodbc
from datetime import datetime, timedelta, timezone
import jwt
from functools import wraps

app = Flask(__name__)


authorizations = {
    'Bearer Auth': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization',
        'description': 'Adicione o token no formato: Bearer <token>'
    }
}

api = Api(app, version='1.0', title='API de Veículos',
          description='Uma API para gerenciamento de veículos',
          authorizations=authorizations,
          security='Bearer Auth'  # Define o Bearer Auth como padrão
         )

sql_str = "SELECT id, veiculo, Status FROM Veiculos"

# Secret key for JWT encoding
JWT_SECRET = 'YG_Ba5XChYTyVgDilkX7bTYphgOmFMdB5sDh1T15uJU='  # Change this to a strong secret key

conn_str = (
            "Driver={SQL Server};"
            "Server=LAPTOP-R3DK1NKD\\SQLEXPRESS;"
            "Database=GerenciarVeiculos;"
            "User Id=Teste_API;"
            "Password=V@i#u$o&;"
        )

ns = api.namespace('veiculos', description='Operações relacionadas ao gerenciamento de veículos')

veiculos_model = api.model('Veiculos', {
    'veiculos': fields.List(fields.String(required=True, description='Lista de veículos'))
})

token_model = api.model('Token', {
    'MerchantId': fields.String(required=True, description='ID do Merchant'),
    'MerchantKey': fields.String(required=True, description='Chave do Merchant')
})

def insert_veiculo(conn, veiculo_ins):
    sql = """
    INSERT INTO Veiculos (
        veiculo, created_at ) 
        VALUES (?, GETDATE())
    """
    cursor = conn.cursor()
    cursor.execute(sql, (
        veiculo_ins, 
    ))

    conn.commit()

# Função para validar o token JWT
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # Verifica se o token está no header da requisição
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1]
        
        if not token:
            return {'message': 'Token Faltando. Favor gerar e inserir o token!'}, 401

        try:
            # Decodifica o token (ajuste a chave secreta conforme o seu projeto)
            data = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])

        except:
            return {'message': 'Token is invalid!'}, 401
        
        return f(*args, **kwargs)
    
    return decorated

@ns.route('/veiculos', methods=['GET'])
class ObterVeiculosResource(Resource):
    @ns.doc('obter_veiculos')
    @token_required  # Adiciona o decorador para verificar a autorização
    def get(self):
        """Obtém todos os veículos cadastrados"""
        try:

            conn = pyodbc.connect(conn_str)
            cursor = conn.cursor()
            cursor.execute(sql_str)
            veiculos = cursor.fetchall()

            result = []
            for veiculo in veiculos:
                result.append({
                    "id": veiculo.id,
                    "veiculo": veiculo.veiculo,
                    "status": veiculo.Status
                })

            conn.close()
            return jsonify(result)
    
        except Exception as e:
            conn.close()
            return {"error": f"Falha ao buscar dados do(s) veículo(s): {str(e)}"}, 400

@ns.route('/veiculos/<int:veiculo_id>')
class ObterVeiculosResource(Resource):
    @ns.doc('obter_veiculos')
    @token_required  # Adiciona o decorador para verificar a autorização
    def get(self, veiculo_id):
        """Obtém o veículo cadastrado pelo ID"""

        try:

            sql_concatenado = sql_str + ' WHERE id = ?'
            
            conn = pyodbc.connect(conn_str)
            cursor = conn.cursor()
            cursor.execute(sql_concatenado, (veiculo_id,))
            veiculos = cursor.fetchall()

            result = []
            for veiculo in veiculos:
                result.append({
                    "id": veiculo.id,
                    "veiculo": veiculo.veiculo,
                    "status": veiculo.Status
                })

            conn.close()
            return jsonify(result)
        
        except Exception as e:
            conn.close()
            return {"error": f"Falha ao buscar dados do veículo: {str(e)}"}, 400

@ns.route('/veiculos/update/<int:veiculo_id>/<int:novo_status>', methods=['PUT'])
class AtualizarVeiculosResource(Resource):
    @ns.doc('atualizar_veiculo')
    @token_required  # Adiciona o decorador para verificar a autorização
    def put(self, veiculo_id, novo_status):
        """Atualiza o veículo cadastrado pelo código informado e o status para 0 ou 1"""
        try:
            if novo_status not in [0, 1]:
                return {"error": "Status inválido. Utilize 0 ou 1."}, 400
            
            conn = pyodbc.connect(conn_str)
            cursor = conn.cursor()

            # Verifica se o veículo existe
            cursor.execute("SELECT * FROM Veiculos WHERE id = ?", veiculo_id)
            veiculo = cursor.fetchone()

            if not veiculo:
                conn.close()
                return {"error": "Veículo não encontrado."}, 404
            
            if novo_status == 0:
                status_str = "DESCONECTADO"
            else:
                status_str = "CONNECTADO"

            # Atualiza o status do veículo
            cursor.execute("UPDATE Veiculos SET updated_at = GETDATE(), status = ? WHERE id = ?", status_str, veiculo_id)
            conn.commit()

            conn.close()
            return {"error": "Veículo atualizado com sucesso!!"}, 200
        
        except Exception as e:
            conn.close()
            return {"error": f"Falha ao atualizar o veículo: {str(e)}"}, 400


@ns.route('/veiculos/delete/<int:veiculo_id>', methods=['DELETE'])
class DeleteVeiculosResource(Resource):
    @ns.doc('deletar_veiculo')
    @token_required  # Adiciona o decorador para verificar a autorização
    def delete(self, veiculo_id):
        """Apaga o veículo cadastrado pelo código informado"""
        try:
            conn = pyodbc.connect(conn_str)
            cursor = conn.cursor()
            cursor.execute("DELETE FROM Veiculos WHERE id = ?", veiculo_id)
            conn.commit()
            
            conn.close()
            return {"message": "Veículo deletado com sucesso"}, 200
        
        except Exception as e:
            conn.close()
            return {"error": f"Falha ao deletar o veículo informado: {str(e)}"}, 400

@ns.route('/add_veiculos', methods=['POST'])
class AddVeiculoResource(Resource):
    @ns.doc('add_veiculos')
    @ns.expect(veiculos_model, validate=True)
    def post(self):
        """Adiciona um ou mais veículos"""
        data = request.get_json()

        if not data or 'veiculos' not in data:
            return {"error": "Entrada inválida, deve conter a chave 'veiculos' com uma lista de veículos"}, 400

        veiculos = data['veiculos']  # Extrai a lista de veículos

        if not isinstance(veiculos, list) or not all(isinstance(veiculo, str) for veiculo in veiculos):
            return {"error": "A chave 'veiculos' deve conter uma lista de strings"}, 400

        conn = pyodbc.connect(conn_str)

        for veiculo in veiculos:
            try:
                insert_veiculo(conn, veiculo)
            except Exception as e:
                conn.close()
                return {"error": f"Falha ao adicionar o veículo: {str(e)}"}, 400

        conn.close()

        return {"message": "Veículo(s) adicionado(s) com sucesso"}, 200



def validate_merchant(conn, merchant_id, merchant_key):
    sql = """
    SELECT COUNT(*) 
    FROM Merchants
    WHERE MerchantId = ? AND MerchantKey = ?
    """
    cursor = conn.cursor()
    cursor.execute(sql, (merchant_id, merchant_key))
    result = cursor.fetchone()
    return result[0] > 0

@ns.route('/generate_token')
class GenerateTokenResource(Resource):
    @ns.doc('generate_token')
    @ns.expect(token_model)
    def post(self):
        """Gera um token JWT"""
        try:
            data = request.get_json()
            merchant_id = data.get("MerchantId")
            merchant_key = data.get("MerchantKey")

            if not merchant_id or not merchant_key:
                return {"error": "MerchantId and MerchantKey are required"}, 400

            conn = pyodbc.connect(conn_str)
            
            # Validar MerchantId e MerchantKey na base de dados
            if not validate_merchant(conn, merchant_id, merchant_key):
                conn.close()
                return {"error": "Invalid MerchantId or MerchantKey"}, 401

            # Create a payload with an expiration time
            payload = {
                "merchant_id": merchant_id,
                "exp": datetime.now(timezone.utc) + timedelta(hours=1)  # Token expires in 1 hour
            }

            # Encode the token
            token = jwt.encode(payload, JWT_SECRET, algorithm="HS256")
            conn.close()
            return jsonify({"token": token})

        except pyodbc.Error as e:
            # Captura erros relacionados ao banco de dados
            return {"error": "Database error", "details": str(e)}, 500

        except jwt.PyJWTError as e:
            # Captura erros relacionados à geração do token JWT
            return {"error": "Token generation error", "details": str(e)}, 500

        except Exception as e:
            # Captura todos os outros tipos de erro
            return {"error": "An unexpected error occurred", "details": str(e)}, 500


if __name__ == '__main__':
    app.run(debug=True)
