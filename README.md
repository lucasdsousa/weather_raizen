# Aplicação de Previsão do Tempo
Este repositório contém uma aplicação de backend em Python que realiza consultas de previsão do tempo utilizando a API do OpenWeatherMap, com gravação do histórico de chamadas em banco de dados MongoDB.

## Pré-requisitos
- Git
- Docker
- Docker Compose

### 1. Clone este repositório, em seguida abra-o:
```
git clone https://github.com/lucasdsousa/weather_raizen.git
cd seu_repositorio
```
### 2. Configure a Chave de API do OpenWeatherMap:
- Crie uma conta em https://openweathermap.org/ e obtenha sua chave de API gratuita.

### 3. Defina a API Key
- Certifique-se de definir a variável de ambiente API_KEY com a sua chave de API do OpenWeatherMap no arquivo docker-compose.yml e no Dockerfile.

### 4. Construa e Execute os Contêineres
Execute os seguintes comandos para construir e iniciar os contêineres:
```
docker-compose up --build
```

### 5. Acesse a Aplicação
- A aplicação estará acessível em http://localhost:5000.

### Endpoints
- GET /weather?city=<nome_da_cidade>: Consulta a previsão do tempo para a cidade especificada.
- GET /history: Retorna o histórico de consultas armazenado no MongoDB.

### Estrutura do Projeto
- main.py: Código principal da aplicação Flask.
- requirements.txt: Lista de dependências Python.
- Dockerfile: Definição do ambiente Docker para a aplicação.
- docker-compose.yml: Configuração do Docker Compose para a aplicação e MongoDB.

## Uso da API
### Obter Previsão do Tempo
Endpoint: /weather

Parâmetros:

- 'city' (obrigatório): Nome da cidade para a qual você deseja obter a previsão do tempo.
Exemplos de requisição:

```
http://127.0.0.1:5000/weather?city=Cachoeira
http://127.0.0.1:5000/weather?city=New%20York
http://localhost:5000/weather?city=Feira%20de%20Santana
http://localhost:5000/weather?city=Salvador,br
```
### Consultar Histórico de Chamadas
Endpoint: /history

Exemplo de requisição:

```
http://127.0.0.1:5000/history
```
### Contribuição
Sinta-se à vontade para contribuir com qualquer tipo de feedback.
