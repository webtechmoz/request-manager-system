from Views.recuperarSenha import *
from Views.admin import *
from Auxiliar.sqlmanager import ver_dados, encriptar_valor

def main(page: ft.Page):
    page.title = 'Request Manager System'
    page.window_maximized = True
    page.theme_mode = ft.ThemeMode.DARK
    
    def esquecisenha(e):
        
        page.dialog = recuperarSenha(page, login)
        page.dialog.open = True
        login.visible = False
        
        page.update()
    
    def account_login(e):
        
        if username.value != '' and password.value != '':
            dados = ver_dados(
                nomeTabela='usuarios',
                conditions=f'username = "{username.value}" AND senha = "{encriptar_valor(password.value)}"',
                colunas='nome'
            )
            
            if len(dados) > 0: 
                page.snack_bar = SnackBar(value=dados[0][0], icon=ft.icons.CHECK, color=ft.colors.BLUE)
                page.snack_bar.open = True
            
            else:
                page.snack_bar = SnackBar(value='Usuário ou senha incorrectos', icon=ft.icons.CLOSE, color=ft.colors.RED)
                page.snack_bar.open = True
        
        else:
            page.snack_bar = SnackBar(value='Preencha todos os campos', icon=ft.icons.CLOSE, color=ft.colors.RED)
            page.snack_bar.open = True
        
        username.value = ''
        password.value = ''
        page.update()
    
    container = ft.Container(
        width= page.window_width,
        height= page.window_height,
        alignment=ft.alignment.center,
        
        content=ft.Column(
            controls=[
                administrator := adminPanel(page),
                
                login := ft.Container(
                    width=320,
                    height=260,
                    bgcolor=ft.colors.WHITE,
                    border_radius=10,
                    padding=ft.padding.only(
                        top=10,
                        left=8,
                        right=8
                    ),
                    visible=False,
                    
                    content=ft.Column(
                        controls=[
                            ft.Text(
                                value='Login',
                                color=ft.colors.with_opacity(0.5, ft.colors.BLACK),
                                size=20,
                                weight='bold'
                            ),
                            
                            username := TextField(
                                hint_text='Username',
                                prefix_icon=ft.icons.PERSON,
                                color=ft.colors.BLACK,
                                size=14,
                                border=ft.InputBorder.UNDERLINE,
                                autofocus=True
                            ),
                            
                            password := TextField(
                                hint_text='Password',
                                prefix_icon=ft.icons.KEY,
                                color=ft.colors.BLACK,
                                size=14,
                                password=True,
                                border=ft.InputBorder.UNDERLINE
                            ),
                            
                            FloatingButton(
                                bgcolor=ft.colors.BLUE,
                                text='Login',
                                width=320,
                                height=40,
                                on_click=account_login
                            ),
                            
                            ft.TextButton(
                                text='Esqueci minha senha',
                                width=320,
                                
                                style=ft.ButtonStyle(
                                    color=ft.colors.BLUE,
                                ),
                                on_click=esquecisenha
                            )
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    )
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER
        )
    )
    
    def on_resize(e):
        container.width= page.window_width
        container.height= page.window_height
        
        page.update()
    
    page.on_resize.subscribe(on_resize)
    page.add(container)

if __name__ == '__main__':
    ft.app(target=main, assets_dir='assets')