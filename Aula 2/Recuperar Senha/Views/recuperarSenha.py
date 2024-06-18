import sys

sys.path.append('Auxiliar')
from Auxiliar.controls import *

def recuperarSenha(page: ft.Page, login: ft.Container):
    
    def close_msgbox(e):
        
        alertdialog.open = False
        login.visible = True
        
        page.update()
    
    def verificar_user(e):
        
        email.visible = False
        alertdialog.content.height = 85
        username.prefix_icon = ft.icons.KEY
        username.hint_text = 'Código de confirmação'
        username.autofocus = True
        btn_verificar.text = 'Verificar Código'
        
        page.update()
    
    alertdialog = ft.AlertDialog(
        modal= True,
        
        title=ft.Row(
            controls=[
                ft.Text(
                    value='Recuperar Senha',
                    size=20,
                    weight='bold',
                    color=ft.colors.WHITE
                ),
                
                ft.IconButton(
                    icon=ft.icons.CLOSE,
                    icon_color=ft.colors.RED,
                    icon_size=25,
                    on_click=close_msgbox
                )
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        ),
        
        content=ft.Column(
            width=300,
            height=140,
            
            controls=[
                username := TextField(
                    hint_text='Username',
                    prefix_icon=ft.icons.PERSON,
                    color=ft.colors.WHITE,
                    size=14,
                    border=ft.InputBorder.UNDERLINE,
                    autofocus=True
                ),
                
                email := TextField(
                    hint_text='Email',
                    prefix_icon=ft.icons.EMAIL,
                    color=ft.colors.WHITE,
                    size=14,
                    border=ft.InputBorder.UNDERLINE
                ),
                
                btn_verificar := FloatingButton(
                    bgcolor=ft.colors.BLUE,
                    text='Recuperar senha',
                    width=320,
                    height=40,
                    on_click=verificar_user
                ),
            ]
        )
    )
    
    return alertdialog