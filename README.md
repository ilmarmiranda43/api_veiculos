# api_veiculos
API que usa banco de dados para cadastrar e gerenciar os veículos da empresa.

# Documentação da API de Veículos
## Descrição
## Esta é uma API para gerenciamento de veículos, construída com Flask e Flask-RESTx. Ela permite a realização de operações CRUD (Criar, Ler, Atualizar e Deletar) em registros de veículos, além de suportar autenticação via JWT para proteger os endpoints.

## Autenticação
A API utiliza autenticação via JWT (JSON Web Token). O token deve ser incluído no header da requisição no formato:

Authorization: Bearer <token>
Geração de Token
Endpoint: /generate_token
Método: POST
Descrição: Gera um token JWT com base no MerchantId e MerchantKey fornecidos.
Parâmetros de Entrada:
MerchantId: ID do Merchant (obrigatório)
MerchantKey: Chave do Merchant (obrigatório)
Resposta de Sucesso:
Código: 200 OK
Conteúdo: { "token": "<JWT Token>" }
Resposta de Erro:
400 Bad Request: Quando MerchantId ou MerchantKey não são fornecidos.
401 Unauthorized: Quando MerchantId ou MerchantKey são inválidos.
500 Internal Server Error: Em caso de falha na geração do token.
