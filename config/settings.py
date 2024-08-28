import logging
import flet as ft
import time
from datetime import datetime
import paho.mqtt.client as mqtt

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def connect_mqtt(page: ft.Page):
    logger.info("Conectando ao broker MQTT...")
    broker = page.client_storage.get("broker_config")
    port = page.client_storage.get("port_config")
    user = page.client_storage.get("usuario_config")
    password = page.client_storage.get("senha_config")
    
    if not broker or not port or not user or not password:
        logger.error("Informações de configuração MQTT não encontradas no local storage.")
        page.add(ft.Text("Informações de configuração MQTT não encontradas no local storage."))
        page.update()
        return

    client = mqtt.Client()
    client.username_pw_set(user, password)

    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            logger.info("Conectado ao broker MQTT com sucesso.")
            page.add(ft.Text("Conectado ao broker MQTT com sucesso."))
        else:
            logger.error(f"Falha na conexão com o broker MQTT. Código de retorno: {rc}")
            page.add(ft.Text(f"Falha na conexão com o broker MQTT. Código de retorno: {rc}"))
        page.update()
    
    def on_message(client, userdata, msg):
        payload = msg.payload.decode()
        logger.info(f"Mensagem recebida do tópico '{msg.topic}': {payload}")
        page.add(ft.Text(f"Mensagem recebida do tópico '{msg.topic}': {payload}"))
        save_message_to_storage(page, msg.topic, payload)
        update_dropdown(page)
        page.update()

    def save_message_to_storage(page: ft.Page, topic: str, message: str):
        logger.info(f"Salvando mensagem no tópico '{topic}': {message}")
        messages = page.client_storage.get("mqtt_messages")
        if messages is None:
            messages = {}
        if topic not in messages:
            messages[topic] = []
        messages[topic].append(message)
        page.client_storage.set("mqtt_messages", messages)

    def update_dropdown(page: ft.Page):
        logger.info("Atualizando dropdown com novos tópicos.")
        dropdown = page.controls[0]
        messages = page.client_storage.get("mqtt_messages")
        if messages is None:
            messages = {}
        dropdown.options.clear()
        for topic in messages.keys():
            dropdown.options.append(ft.DropdownOption(topic))
        dropdown.update()

    client.on_connect = on_connect
    client.on_message = on_message

    try:
        logger.info("Tentando conectar ao broker MQTT...")
        client.connect(broker, int(port), 60)
        client.loop_start()
    except Exception as e:
        logger.error(f"Erro ao conectar ao broker MQTT: {e}")
        page.add(ft.Text(f"Erro ao conectar ao broker MQTT: {e}"))
        page.update()

    return client

def background_task(client):
    while True:
        logger.info("Background task is running...")
        time.sleep(1)