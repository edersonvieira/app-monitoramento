import logging
import flet as ft
from datetime import datetime

logger = logging.getLogger(__name__)

def home_page(page: ft.Page):
    logger.info("Carregando página inicial.")
    page.title = "Inicial"

    dropdown = ft.Dropdown(
        label="Selecione seu equipamento",
        on_change=lambda e: update_table(page, e.control.value)
    )
    
    table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("X")),
            ft.DataColumn(ft.Text("Y")),
            ft.DataColumn(ft.Text("Z")),
            ft.DataColumn(ft.Text("Data e Hora")),
        ],
        rows=[],
        width=page.window_width - 20,
    )
    
    scrollable_table = ft.Container(
        content=ft.Column([table], scroll=ft.ScrollMode.AUTO),
        height=400,  # Adjust the height as needed
        width=page.window_width - 20,
    )
    
    page.controls.append(dropdown)
    page.controls.append(scrollable_table)
    page.table = table

    topicos_sub = page.client_storage.get("topicos_sub")
    if topicos_sub is None:
        topicos_sub = {}
    dispositivos = topicos_sub.keys()
    for dispositivo in dispositivos:
        dropdown.options.append(ft.dropdown.Option(dispositivo))
    
    page.update()
    dropdown.update()
    logger.info("Página inicial carregada com sucesso.")

def update_table(page: ft.Page, topic: str):
    table = page.table

    if not isinstance(table, ft.DataTable):
        logger.error("The control is not a DataTable.")
        return

    table.rows.clear()

    pacotes = page.client_storage.get("pacotes")
    if not pacotes:
        logger.warning("No packets found in local storage.")
        return

    for pacote in pacotes:
        if topic in pacote:
            equipamento_pacotes = pacote[topic]
            break
    else:
        logger.warning(f"No packets found for topic '{topic}'.")
        return

    for pacote in equipamento_pacotes:
        timestamp = datetime.fromtimestamp(pacote["timestamp"]).strftime("%d/%m/%Y %H:%M:%S")
        table.rows.append(ft.DataRow(cells=[
            ft.DataCell(ft.Text(str(pacote["x"]))),
            ft.DataCell(ft.Text(str(pacote["y"]))),
            ft.DataCell(ft.Text(str(pacote["z"]))),
            ft.DataCell(ft.Text(timestamp))
        ]))

    page.update()