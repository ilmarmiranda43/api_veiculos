# api_veiculos
API que usa banco de dados para cadastrar e gerenciar os veículos da empresa.

## Guia de Uso da API

## Endpoints

## 1. Geração de Token
- **Endpoint:** `/generate_token`
- **Método:** `POST`
- **Descrição:** Gera um token JWT.

  > **Parâmetros de Entrada:**
  > - `MerchantId`: ID do Merchant (obrigatório)
  > - `MerchantKey`: Chave do Merchant (obrigatório)

  **Resposta de Sucesso:**
  ```json
  {
    "token": "<JWT Token>"
  }
 
 **Respostas de Erro:**
> - 400 Bad Request: Quando MerchantId ou MerchantKey não são fornecidos.
> - 401 Unauthorized: Quando MerchantId ou MerchantKey são inválidos.
> - 500 Internal Server Error: Em caso de falha na geração do token.

## 2. Obter Todos os Veículos
- **Endpoint:** `/veiculos`
- **Método:** `GET`
- **Descrição:** Obtém todos os veículos cadastrados.
- **Autenticação:** Necessário token JWT.

  **Resposta de Sucesso:**
     ```json
     [
     {
       "id": 1,
       "veiculo": "Carro Exemplo",
       "status": "CONNECTED"
     }
   ]
**Respostas de Erro:**
 > - 401 Unauthorized: Token não fornecido ou inválido.
 > - 400 Bad Request: Falha ao buscar os dados dos veículos.

## 3. Obter Veículo por ID
- **Endpoint:** `/veiculos/<int:veiculo_id>`
- **Método:** `GET`
- **Descrição:** Obtém o veículo cadastrado pelo ID
- **Autenticação:** Necessário token JWT.

   > **Parâmetros da URL:**
   > - `veiculo_id`: ID do veículo (obrigatório)

  **Resposta de Sucesso:**
   ```json
    [
      {
        "id": 1,
        "veículo": "Carro Exemplo",
        "status": "CONNECTED"
      }
  ]
**Respostas de Erro:**
 > - 401 Unauthorized: Token não fornecido ou inválido.
 > - 400 Bad Request: Falha ao buscar os dados dos veículos

## 4. Atualizar Status de Veículo
  - **Endpoint:** `/veiculos/UPDATE/<int:veiculo_id>/<int:novo_status>`
  - **Método:** `PUT`
  - **Descrição:** Atualiza o status do veículo cadastrado para 0 (DESCONECTADO) ou 1 (CONECTADO)
  - **Autenticação:** Necessário token JWT.
  
     > **Parâmetros da URL:**
     > - `veiculo_id`: ID do veículo (obrigatório)
     > - `novo_status`: NOvo status do veículo(0 ou 1)
  
    **Resposta de Sucesso:**
     ```json
       {
          "message": "Veículo atualizado com sucesso!"
        }
  **Respostas de Erro:**
   > - 401 Unauthorized: Token não fornecido ou inválido.
   > - 404 Not Found: Veículo não encontrado.
   > - 400 Bad Request: Status inválido

## 5. Deletar Veículo
  - **Endpoint:** `/veiculos/delete/<int:veiculo_id>`
  - **Método:** `DELETE`
  - **Descrição:** Apaga o veículo cadastrado pelo código informado.
  - **Autenticação:** Necessário token JWT.
  
     > **Parâmetros da URL:**
     > - `veiculo_id`: ID do veículo (obrigatório)
     
    **Resposta de Sucesso:**
     ```json
       {
          "message": "Veículo deletado com sucesso"
        }
  **Respostas de Erro:**
   > - 401 Unauthorized: Token não fornecido ou inválido.
   > - 404 Not Found: Veículo não encontrado.
   > - 400 Bad Request: Falha ao deletar o veículo.

## 6. Adicionar Veículos
  - **Endpoint:** `/add_veiculos`
  - **Método:** `POST`
  - **Descrição:** Adiciona um ou mais veículos.
  - **Autenticação:** Necessário token JWT.
  
     > **Parâmetros da URL:**
     > - `veiculo_id`: Lista de veículos a serem adicionados (obrigatório)

    **Exemplo de Requisição:**
     ```json
       {
          "message": "Veículo deletado com sucesso"
        }
     
  **Resposta de Sucesso:**
   ```json
       {
          "message": "Veículo deletado com sucesso"
        }
  **Respostas de Erro:**
   > - 401 Unauthorized: Token não fornecido ou inválido.
   > - 404 Not Found: Veículo não encontrado.
   > - 400 Bad Request: Falha ao deletar o veículo.


