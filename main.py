from flask import Flask, jsonify, request
import requests
import json
from datetime import datetime
from pymongo import MongoClient
import os
import logging

# Definindo a aplicação Flask
app = Flask(__name__)

# Configuração de log para debug. Descomente a linha abaixo apenas se erros persistirem, como pode ser o caso da API_KEY.
#logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s')


# OpenWeatherMap API Key
API_KEY = os.getenv('API_KEY')

if not API_KEY:
    logging.error("API_KEY não configurada. Certifique-se de definir a variável de ambiente API_KEY.")
else:
    logging.debug(f"API_KEY: {API_KEY}")

# MongoDB
client = MongoClient('mongodb://mongo:27017/')
db = client.weather_raizen
collection = db.history

# Roteirização da aplicação Flask

# Rota padrão
@app.route('/', methods=['GET'])
def index():
    message = "Esta é uma aplicação de backend em Python que realiza consultas de previsão do tempo utilizando a API do OpenWeatherMap, com gravação do histórico de chamadas em banco de dados MongoDB. Leia o Readme para realizar as consultas."
    return message

# Rota de consulta e processo de requisições na API
@app.route('/weather', methods=['GET'])
def get_weather():
    # Nome da cidade através da query string 'city'
    city = request.args.get('city')

    if not city:
        return jsonify({'error': 'Informe a cidade para realizar a consulta.'}), 400
  
    url = 'http://api.openweathermap.org/data/2.5/forecast'
    params = {'q': city, 'appid': API_KEY, 'units': 'metric'}  # 'cnt' para quantidade de dias da consulta e 'units' para temperatura em Celsius

    response = requests.get(url, params=params)
    
    # Tratamento de erros caso haja algum problema em se comunicar com o servidor da API
    if response.status_code != 200:
        logging.debug(f"Resposta da API: {response.status_code} - {json.dumps(json.loads(response.text), indent=2)}")
        return jsonify({'error': 'Erro ao realizar consulta no servidor, tente novamente.'})
    
    try:
        data = response.json()
    except json.JSONDecodeError as e:
        logging.error(f"Erro ao decodificar a resposta JSON: {e}")
        return jsonify({'error': 'Erro ao decodificar a resposta do servidor.', 'details': str(e)})

    # Cálculo de temperatura média nos próximos 5 dias
    total_sum_temp = 0

    for i in data["list"]:
        temp_un = i["main"]["temp"]
        total_sum_temp = total_sum_temp + temp_un


    # Gravação do histórico das consultas no MongoDB
    temp = data["list"][0]["main"]["temp"]
    temp_media = total_sum_temp / len(data["list"])
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    history = {'timestamp': timestamp, 'city': city, 'temp': temp, 'temp_media_5dias': "{:.2f}".format(temp_media)}
    collection.insert_one(history)

    # Retorno da previsão
    return jsonify(data)

# Rota de histórico de consultas
@app.route('/history', methods=['GET'])
def get_history():
    # Get do histórico no MongoDB
    history_entries = list(collection.find({}, {'_id': 0}))

    return jsonify(history_entries)  # Retorno do histórico (json)

# Execução da aplicação
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
