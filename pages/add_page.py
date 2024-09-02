import flet as ft
from pages.home_page import home_page

def add_page(page: ft.Page):
    page.title = "Adicionar"
    
    equipamento_id = ft.TextField(label="Identificação do Equipamento")
    sub = ft.TextField(label="Tópico de Subscrição")
    
    def add_topico(e):
        equipamento = equipamento_id.value
        topico_sub = sub.value
        
        topicos_sub = page.client_storage.get("topicos_sub")
        if topicos_sub is None:
            topicos_sub = {}
        
        topicos_sub[equipamento] = topico_sub
        
        page.client_storage.set("topicos_sub", topicos_sub)
        
        equipamento_id.value = ""
        sub.value = ""
        
        page.controls.clear()
        page.add(ft.Text(f"Tópico adicionado:\nPublicação: {topico_sub} para o equipamento {equipamento}"))
        home_page(page)
        page.update()

    adicionar_button = ft.CupertinoFilledButton(text="Adicionar", on_click=add_topico, width=page.window_width - 20, height=50)
    
    content = ft.Column(
        [
            equipamento_id,
            sub,
            adicionar_button
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