import json
import time
import flet as ft
import paho.mqtt.client as mqtt
import logging

from pages.home_page import update_table

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
            
            topicos_sub = page.client_storage.get("topicos_sub")
            if topicos_sub:
                for equipamento, topico in topicos_sub.items():
                    client.subscribe(topico)
                    logger.info(f"Inscrito no tópico: {topico} para o equipamento: {equipamento}")
        else:
            logger.error(f"Falha na conexão com o broker MQTT. Código de retorno: {rc}")
            page.add(ft.Text(f"Falha na conexão com o broker MQTT. Código de retorno: {rc}"))
        page.update()
    
    def on_message(client, userdata, msg):
        topic = msg.topic
        message = msg.payload.decode()
        logger.info(f"Mensagem recebida no tópico '{topic}': {message}")
        save_message_to_storage(page, topic, message)
        update_table(page, topic)

    def save_message_to_storage(page: ft.Page, topic: str, message: str):
        logger.info(f"Salvando mensagem no tópico '{topic}': {message}")
        
        topicos_sub = page.client_storage.get("topicos_sub")
        if not topicos_sub:
            logger.warning("Nenhum tópico de subscrição encontrado no local storage.")
            return
        
        equipamento = None
        for eq, topico in topicos_sub.items():
            if topico == topic:
                equipamento = eq
                break
        
        if not equipamento:
            logger.warning(f"Nenhum equipamento encontrado para o tópico '{topic}'.")
            return
        
        pacotes = page.client_storage.get("pacotes")
        if pacotes is None:
            pacotes = []
        
        equipamento_pacotes = None
        for pacote in pacotes:
            if equipamento in pacote:
                equipamento_pacotes = pacote[equipamento]
                break
        
        if equipamento_pacotes is None:
            equipamento_pacotes = []
            pacotes.append({equipamento: equipamento_pacotes})
        
        try:
            data = json.loads(message)
            x = data["x"]
            y = data["y"]
            z = data["z"]
            timestamp = data["timestamp"]
        except (json.JSONDecodeError, KeyError) as e:
            logger.error(f"Erro ao decodificar a mensagem JSON: {e}")
            return
        
        equipamento_pacotes.append({
            "x": float(x),
            "y": float(y),
            "z": float(z),
            "timestamp": int(timestamp)
        })
        
        page.client_storage.set("pacotes", pacotes)
        logger.info(f"Pacote salvo para o equipamento '{equipamento}': {equipamento_pacotes[-1]}")

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