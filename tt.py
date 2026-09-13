"""
registrador.py - MÓDULO REGISTRADOR (roda no PC, não no Wokwi)
=================================================================
Este script fica ligado no computador (não é um ESP32). Ele:
  1) Se conecta ao mesmo broker MQTT (broker.hivemq.com)
  2) Assina o tópico de telemetria de TODOS os containers
  3) Cada vez que chega uma mensagem, grava os dados em um arquivo
     CSV (um arquivo por container) e também loga os alertas.

Como rodar:
    pip install paho-mqtt
    python registrador.py

Ele cria uma pasta "dados/" com um arquivo .csv por container e um
arquivo "alertas.log" com o histórico de alertas.
"""

import json
import os
import csv
from datetime import datetime
import paho.mqtt.client as mqtt

BROKER = "broker.hivemq.com"
PORTA = 1883
TOPICO_TELEMETRIA = "trabalho/containers/+/telemetria"
TOPICO_ALERTA = "trabalho/containers/+/alerta"

PASTA_DADOS = "dados"
os.makedirs(PASTA_DADOS, exist_ok=True)

CAMPOS_CSV = ["timestamp", "container_id", "codigo_container",
              "temperatura", "umidade", "luminosidade_lux", "porta_aberta"]


def caminho_csv(container_id):
    return os.path.join(PASTA_DADOS, f"{container_id}.csv")


def garante_cabecalho(container_id):
    caminho = caminho_csv(container_id)
    if not os.path.exists(caminho):
        with open(caminho, "w", newline="", encoding="utf-8") as f:
            csv.writer(f).writerow(CAMPOS_CSV)


def grava_telemetria(dados):
    container_id = dados["container_id"]
    codigo = dados["codigo_container"]
    garante_cabecalho(container_id)

    with open(caminho_csv(container_id), "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        for leitura in dados["leituras"]:
            writer.writerow([
                leitura["timestamp"],
                container_id,
                codigo,
                leitura["temperatura"],
                leitura["umidade"],
                leitura["luminosidade_lux"],
                leitura["porta_aberta"],
            ])
    print(f"[{datetime.now()}] Gravadas {len(dados['leituras'])} leituras de {container_id}")


def grava_alerta(dados):
    linha = f"[{datetime.now()}] ALERTA {dados['container_id']} " \
            f"tipo={dados['tipo_alerta']} valor={dados['valor']}\n"
    with open(os.path.join(PASTA_DADOS, "alertas.log"), "a", encoding="utf-8") as f:
        f.write(linha)
    print(linha.strip())


def ao_conectar(client, userdata, flags, rc, properties=None):
    print("Conectado ao broker MQTT com código:", rc)
    client.subscribe(TOPICO_TELEMETRIA)
    client.subscribe(TOPICO_ALERTA)


def ao_receber(client, userdata, msg):
    try:
        dados = json.loads(msg.payload.decode())
    except ValueError:
        print("Mensagem inválida recebida em", msg.topic)
        return

    if msg.topic.endswith("/telemetria"):
        grava_telemetria(dados)
    elif msg.topic.endswith("/alerta"):
        grava_alerta(dados)


cliente = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, "registrador-pc")
cliente.on_connect = ao_conectar
cliente.on_message = ao_receber

cliente.connect(BROKER, PORTA, keepalive=60)
print("Registrador rodando. Aguardando mensagens... (Ctrl+C para sair)")
cliente.loop_forever()