import flet as ft
from pages.config_page import config_page
import threading
from pages.home_page import home_page
from pages.add_page import add_page
from config.settings import connect_mqtt, background_task
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main(page: ft.Page):
    page.window_width = 375
    page.window_height = 667 
    logger.info("Iniciando a aplicação...")
    page.title = "APP Monitoramento"
    client = connect_mqtt(page)
    
    def on_navigation_change(e):
        logger.info(f"Alterando navegação para o índice: {e.control.selected_index}")
        page.controls.clear()
        if e.control.selected_index == 0:
            home_page(page)
        elif e.control.selected_index == 1:
            add_page(page)
        elif e.control.selected_index == 2:
            config_page(page)
        page.update()

    page.navigation_bar = ft.NavigationBar(
        destinations=[
            ft.NavigationDestination(icon=ft.icons.HOME, label="Inicial"),
            ft.NavigationDestination(icon=ft.icons.ADD, label="Adicionar"),
            ft.NavigationDestination(icon=ft.icons.ENGINEERING_OUTLINED, label="Configuração"),
        ],
        on_change=on_navigation_change
    )
    
    page.add(page.navigation_bar)
    home_page(page)

    threading.Thread(target=background_task, args=(client,), daemon=True).start()
    logger.info("Aplicação iniciada com sucesso.")

ft.app(target=main)