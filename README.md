# api_veiculos
API que usa banco de dados para cadastrar e gerenciar os veículos da empresa.

## Guia de Uso da API

### Endpoints

#### 1. Geração de Token
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

---
