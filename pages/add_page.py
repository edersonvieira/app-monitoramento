import flet as ft
from pages.home_page import home_page

def add_page(page: ft.Page):
    page.title = "Adicionar"
    
    equipamento_id = ft.TextField(label="Identificação do Equipamento")
    pub = ft.TextField(label="Tópico de Publicação")
    
    def add_topico(e):
        equipamento = equipamento_id.value
        topico_pub = pub.value
        
        dispositivos = page.client_storage.get("dispositivos")
        if dispositivos is None:
            dispositivos = []
        if equipamento not in dispositivos:
            dispositivos.append(equipamento)
        page.client_storage.set("dispositivos", dispositivos)
        
        page.client_storage.set(f"{equipamento}_topico", topico_pub)
        
        equipamento_id.value = ""
        pub.value = ""
        
        page.controls.clear()
        page.add(ft.Text(f"Tópico adicionado:\Publicação: {topico_pub} para o equipamento {equipamento}"))
        home_page(page)
        page.update()

    adicionar_button = ft.ElevatedButton(text="Adicionar", on_click=add_topico, width=page.window_width - 20, height=50)
    
    page.add(equipamento_id)
    page.add(pub)
    page.add(adicionar_button)