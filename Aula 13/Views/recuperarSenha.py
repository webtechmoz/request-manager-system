import sys
import string
from pathlib import Path

sys.path.append('Auxiliar')
from Auxiliar.controls import *
from Auxiliar.ClassRegex import REGEX
from Auxiliar.Email import send_mail, choice
from Auxiliar.sqlmanager import ver_dados, encriptar_valor, editar_dados

def recuperarSenha(page: ft.Page, login: ft.Container):
    
    def close_msgbox(e):
        
        alertdialog.open = False
        login.visible = True
        
        page.update()
    
    def verificar_user(e):
        
        def confirmar_codigo(e, Username, gen_KEY: str):
            
            if username.value != '':
                if username.value == gen_KEY:
                    strings = string.ascii_letters + "0123456789" + "!@$?"
                    senha = ''
                    
                    for _ in range(5):
                        senha += choice(strings)
                    
                    editar_dados(
                        nomeTabela='usuarios',
                        dados=['senha', encriptar_valor(senha), f'username = "{Username}"']
                    )
                    
                    path = Path.cwd() / "Users"
                    path.mkdir(parents=True, exist_ok=True)
                    
                    with open(f'Users/{Username}.txt', mode='w', encoding='UTF-8') as arquivo:
                        arquivo.writelines(f'Username: {Username}\nPassword: {senha}')
                    
                    close_msgbox
                    
                    page.snack_bar = SnackBar(value='A palavra-passe foi redefinida com sucesso', icon=ft.icons.CHECK, color=ft.colors.BLUE)
                    page.snack_bar.open = True
                
                else:
                    page.snack_bar = SnackBar(value='Chave de confirmação inválida', icon=ft.icons.CLOSE, color=ft.colors.RED)
                    page.snack_bar.open = True
            
            else:
                page.snack_bar = SnackBar(value='Preencha com o código de confirmação', icon=ft.icons.CLOSE, color=ft.colors.RED)
                page.snack_bar.open = True

            page.update()
        
        if username.value != '' and email.value != '':
            if REGEX().verificar_email(email.value) == True:
                dados = ver_dados(
                    nomeTabela='usuarios',
                    conditions=f'username = "{username.value}" AND email = "{email.value}"',
                    colunas='username'
                )
                
                if len(dados) > 0:
                    gen_KEY = send_mail(email.value)
                    
                    if 'Err' in str(gen_KEY):
                        page.snack_bar = SnackBar(value=f'{gen_KEY}', icon=ft.icons.CLOSE, color=ft.colors.RED)
                        page.snack_bar.open = True
                    
                    else:
                        username.value = ''
                        email.value = ''
                        email.visible = False
                        alertdialog.content.height = 85
                        username.prefix_icon = ft.icons.KEY
                        username.hint_text = 'Código de confirmação'
                        username.autofocus = True
                        btn_verificar.text = 'Verificar Código'
                        btn_verificar.on_click = lambda e, Username = dados[0][0], gen_KEY = gen_KEY: confirmar_codigo(e, Username, gen_KEY)

                        page.snack_bar = SnackBar(value='Código de confirmação enviado', icon=ft.icons.VERIFIED, color=ft.colors.BLUE)
                        page.snack_bar.open = True
                else:
                    page.snack_bar = SnackBar(value='Username ou Email incorrectos', icon=ft.icons.CLOSE, color=ft.colors.RED)
                    page.snack_bar.open = True
            
            else:
                page.snack_bar = SnackBar(value='Email inválido', icon=ft.icons.CLOSE, color=ft.colors.RED)
                page.snack_bar.open = True
        
        else:
            page.snack_bar = SnackBar(value='Preencha todos os campos', icon=ft.icons.CLOSE, color=ft.colors.RED)
            page.snack_bar.open = True
        
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