import flet as ft
from pages.home_page import home_page

def config_page(page: ft.Page):
    page.title = "Configuração"
    
    broker_config = page.client_storage.get("broker_config") or ""
    port_config = page.client_storage.get("port_config") or ""
    usuario_config = page.client_storage.get("usuario_config") or ""
    senha_config = page.client_storage.get("senha_config") or ""
    
    broker_input = ft.TextField(label="Broker", value=broker_config)
    port_input = ft.TextField(label="Porta", value=port_config)
    usuario_input = ft.TextField(label="Usuário MQTT", value=usuario_config)
    senha_input = ft.TextField(label="Senha MQTT", password=True, value=senha_config)
    
    def save_mqtt_config(e):
        broker_config = broker_input.value
        port_config = port_input.value
        usuario_config = usuario_input.value
        senha_config = senha_input.value
        
        page.client_storage.set("broker_config", broker_config)
        page.client_storage.set("port_config", port_config)
        page.client_storage.set("usuario_config", usuario_config)
        page.client_storage.set("senha_config", senha_config)
        
        alert = ft.CupertinoAlertDialog(
            title=ft.Text("Configuração Salva"),
            content=ft.Text(f"Comunicação MQTT salva:\nBroker: {broker_config}:{port_config}\nUsuário: {usuario_config}\nSenha: {senha_config}"),
            actions=[
                ft.CupertinoDialogAction("OK", on_click=lambda e: close_dialog(alert))
            ],
        )
        page.dialog = alert
        alert.open = True
        page.update()
    
    def close_dialog(dialog):
        dialog.open = False
        page.update()
    
    save_button = ft.CupertinoFilledButton(text="Salvar", on_click=save_mqtt_config, width=page.window_width - 20, height=50)
    
    def clear_storage(e):
        confirm_clear = ft.CupertinoAlertDialog(
            title=ft.Text("Confirmar Limpeza"),
            content=ft.Text("Tem certeza de que deseja limpar o LocalStorage?"),
            actions=[
                ft.CupertinoDialogAction("Cancelar", on_click=lambda e: close_dialog(confirm_clear)),
                ft.CupertinoDialogAction("Limpar", on_click=lambda e: execute_clear_storage(confirm_clear))
            ],
        )
        page.dialog = confirm_clear
        confirm_clear.open = True
        page.update()
    
    def execute_clear_storage(dialog):
        page.client_storage.clear()
        page.controls.clear()
        close_dialog(dialog)
        page.update()
        page.navigation_bar.selected_index = 0
        home_page(page)

    
    clear_button = ft.CupertinoFilledButton(text="Limpar LocalStorage", on_click=clear_storage, width=page.window_width - 20, height=50)
    
    content = ft.Column(
        [
            broker_input,
            port_input,
            usuario_input,
            senha_input,
            save_button,
            clear_button
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )
    
    container = ft.Container(
        content=content,
        alignment=ft.alignment.center,
        expand=True
    )
    
    page.add(container)