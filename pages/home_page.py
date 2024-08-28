import logging
import flet as ft

logger = logging.getLogger(__name__)

def home_page(page: ft.Page):
    logger.info("Carregando página inicial.")
    page.title = "Inicial"

    dropdown = ft.Dropdown(
        label="Selecione seu equipamento",
        on_change=lambda e: update_table(page, e.control.value)  # Atualiza a tabela quando o dropdown muda
    )
    
    table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("X")),
            ft.DataColumn(ft.Text("Y")),
            ft.DataColumn(ft.Text("Z")),
            ft.DataColumn(ft.Text("Data e Hora")),
        ],
        rows=[],
        width=page.window_width - 20
    )
    
    page.add(dropdown)
    page.add(table)

    # Populate dropdown with dispositivos
    dispositivos = page.client_storage.get("dispositivos")
    if dispositivos is None:
        dispositivos = []
    for dispositivo in dispositivos:
        dropdown.options.append(ft.dropdown.Option(dispositivo))
    dropdown.update()
    logger.info("Página inicial carregada com sucesso.")

def update_table(page: ft.Page, selected_topic: str):
    logger.info(f"Atualizando tabela para o tópico selecionado: {selected_topic}")
    messages = page.client_storage.get("mqtt_messages")
    if messages is None:
        messages = {}
    if selected_topic not in messages:
        logger.warning(f"Tópico selecionado '{selected_topic}' não encontrado nas mensagens.")
        return

    # Limpar as linhas existentes na tabela
    table = page.controls[1]  # Assuming the table is the second control added to the page
    table.rows.clear()

    # Adicionar novas linhas à tabela com base nas mensagens recuperadas
    for message in messages[selected_topic]:
        # Supondo que a mensagem seja uma string no formato "X,Y,Z,Data e Hora"
        x, y, z, timestamp = message.split(',')
        table.rows.append(
            ft.DataRow(cells=[
                ft.DataCell(ft.Text(x)),
                ft.DataCell(ft.Text(y)),
                ft.DataCell(ft.Text(z)),
                ft.DataCell(ft.Text(timestamp)),
            ])
        )
    table.update()
    logger.info(f"Tabela atualizada para o tópico: {selected_topic}")