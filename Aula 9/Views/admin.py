from Auxiliar.controls import *
from Auxiliar.ClassRegex import REGEX
import string
from random import choice
from pathlib import Path
from Auxiliar.sqlmanager import criar_tabela, inserir_dados, ver_dados, encriptar_valor, editar_dados, apagar_dados

def adminPanel(page: ft.Page, username: str = 'Admin'):
    
    def clicked(e):
        page.snack_bar = SnackBar(value=f'{e.control}',icon=ft.icons.MENU_BOOK, color=ft.colors.BLUE)
        page.snack_bar.open = True
        
        page.update()
    
    def manage_users(e):
        
        def manage_user(e: ft.ControlEvent, id: int):
            
            def delete_user(e: ft.ControlEvent, id: int):
                
                admins = ver_dados(
                    nomeTabela='usuarios',
                    conditions=f'cargo = "Administrator"',
                    colunas='id'
                )
                
                if len(admins) == 1 and int(id) == int(admins[0][0]):
                    page.snack_bar = SnackBar(value='Não pode apagar este usuário', icon=ft.icons.CLOSE, color=ft.colors.RED)
                    page.snack_bar.open = True
                
                else:
                    apagar_dados(
                        nomeTabela='usuarios',
                        conditions=f'id = "{id}"'
                    )
                    
                    page.snack_bar = SnackBar(value='Usuário apagado com sucesso', icon=ft.icons.VERIFIED, color=ft.colors.BLUE)
                    page.snack_bar.open = True
                
                page.dialog.open = False
                load_users(e)
                
                page.update()
            
            def edit_user(e: ft.ControlEvent, id: int):
                dados = ver_dados(
                    nomeTabela='usuarios',
                    conditions=f'id = "{id}"'
                )[0]
                
                nome.value = dados[1]
                user.value = dados[2]
                email.value = dados[3]
                cargo.value = dados[5]
                status.value = dados[6]
                
                btn_addUser.on_click = lambda e, id = id: add_user(e, id= id)
                page.dialog.open = False
                load_users(e)
                page.update()
            
            if e.control.icon == 'delete':
                page.dialog = AlertDialog(
                    page=page,
                    title=f'Usuário nº {id}',
                    value=f'Deseja apagar  usuário nº {id}?',
                    text_button='Confirmar',
                    icon=ft.icons.DELETE,
                    color=ft.colors.RED,
                    on_click=lambda e, id = id: delete_user(e, id)
                )
                
                page.dialog.open = True
            
            elif e.control.icon == 'edit':
                page.dialog = AlertDialog(
                    page=page,
                    title=f'Usuário nº {id}',
                    value=f'Deseja editar  usuário nº {id}?',
                    text_button='Confirmar',
                    icon=ft.icons.EDIT,
                    color=ft.colors.BLUE,
                    on_click=lambda e, id = id: edit_user(e, id)
                )
                
                page.dialog.open = True
            
            page.update()
        
        def load_users(e):
            
            tabela_usuarios.rows.clear()
            
            try:
                dados = ver_dados(
                    nomeTabela='usuarios',
                    colunas='id,nome,username,email,cargo,status'
                )
                
                if len(dados) > 0:
                    for dado in dados:
                        tabela_usuarios.rows.append(
                            ft.DataRow(
                                cells=[
                                    ft.DataCell(ft.Text(value=dado[0], size=12, color=ft.colors.WHITE, weight='bold')),
                                    ft.DataCell(ft.Text(value=dado[1], size=12, color=ft.colors.WHITE, weight='bold')),
                                    ft.DataCell(ft.Text(value=dado[2], size=12, color=ft.colors.WHITE, weight='bold')),
                                    ft.DataCell(ft.Text(value=dado[3], size=12, color=ft.colors.WHITE, weight='bold')),
                                    ft.DataCell(ft.Text(value=dado[4], size=12, color=ft.colors.WHITE, weight='bold')),
                                    ft.DataCell(ft.Text(value=dado[5], size=12, color=ft.colors.WHITE, weight='bold')),
                                    ft.DataCell(
                                        ft.Row(
                                            controls=[
                                                IconButton(icon=ft.icons.EDIT, color=ft.colors.BLUE, size=20, on_click= lambda e, id = dado[0]: manage_user(e, id)),
                                                IconButton(icon=ft.icons.DELETE, color=ft.colors.RED, size=20, on_click= lambda e, id = dado[0]: manage_user(e, id)),
                                            ]
                                        )
                                    )
                                ]
                            )
                        )
            
            except Exception as e:
                page.snack_bar = SnackBar(value=f'Erro: {e}', icon=ft.icons.CLOSE, color=ft.colors.RED)
                page.snack_bar.open = True
                
            page.update()
        
        def add_user(e: ft.ControlEvent, id: int = ''):
            
            criar_tabela(
                nomeTabela='usuarios'
            )
            
            if nome.value != '' and user.value != '' and email.value != '' and cargo.value != None and status.value != None:
                if REGEX().verificar_email(email.value) == True:
                    if id == '':
                        dados = ver_dados(
                            nomeTabela='usuarios',
                            conditions=f'username = "{user.value}" OR email = "{email.value}"',
                            colunas='nome'
                        )
                        
                        if len(dados) == 0:
                            
                            strings = string.ascii_letters + "0123456789" + "!@$?"
                            password = ''
                            
                            for _ in range(5):
                                password += choice(strings)
                            
                            path = Path.cwd() / "Users"
                            path.mkdir(parents=True, exist_ok=True)
                            
                            with open(f'Users/{user.value}.txt', mode='w', encoding='UTF-8') as arquivo:
                                arquivo.writelines(f'Username: {user.value}\nPassword: {password}')
                                
                            inserir_dados(
                                nomeTabela='usuarios',
                                dados=[nome.value, user.value, email.value, encriptar_valor(password), cargo.value, status.value]
                            )
                            
                            nome.value = ''
                            user.value = ''
                            email.value = ''
                            cargo.value = None
                            status.value = None
                            nome.autofocus = True
                            
                            page.snack_bar = SnackBar(value='Usuário Criado com sucesso', icon=ft.icons.VERIFIED, color=ft.colors.BLUE)
                            page.snack_bar.open = True
                        
                        else:
                            page.snack_bar = SnackBar(value='Já existe um usuários com estes dados', icon=ft.icons.CLOSE, color=ft.colors.RED)
                            page.snack_bar.open = True
                    
                    else:
                        dados = ver_dados(
                            nomeTabela='usuarios',
                        )
                        
                        if len(dados) == 1 and (cargo.value != 'Administrator' or status.value != 'Activo'):
                            page.snack_bar = SnackBar(value='Não pode editar este usuário', icon=ft.icons.CLOSE, color=ft.colors.RED)
                            page.snack_bar.open = True
                        
                        else:
                            dicionario = {
                                'nome': nome.value,
                                'username': user.value,
                                'email': email.value,
                                'cargo': cargo.value,
                                'status': status.value
                            }
                            
                            for coluna in dicionario:
                                editar_dados(
                                    nomeTabela='usuarios',
                                    dados=[coluna, dicionario[coluna], f'id = "{id}"'],
                                )
                            
                            page.snack_bar = SnackBar(value=f'Usuário nº {id} actualizado com sucesso', icon=ft.icons.VERIFIED, color=ft.colors.BLUE)
                            page.snack_bar.open = True
                        
                        
                        btn_addUser.on_click = lambda e, id = id: add_user(e)
                        nome.value = ''
                        user.value = ''
                        email.value = ''
                        cargo.value = None
                        status.value = None
                        nome.autofocus = True
                
                else:
                    email.value = ''
                    email.autofocus = True
                    page.snack_bar = SnackBar(value='O email inserido é inválido', icon=ft.icons.CLOSE, color=ft.colors.RED)
                    page.snack_bar.open = True
                
            else:
                page.snack_bar = SnackBar(value='Preencha todos os campos', icon=ft.icons.CLOSE, color=ft.colors.RED)
                page.snack_bar.open = True
            
            load_users(e)
            page.update()
        
        tela_principal.content = ft.Column(
            controls=[
                ft.Text(
                    value='Gestão de Usuários'.upper(),
                    color=ft.colors.WHITE,
                    size=15,
                    weight='bold'
                ),
                
                ft.ResponsiveRow(
                    controls=[
                        nome := TextField(
                            hint_text='Nome do Usuário',
                            size=13,
                            color=ft.colors.BLACK,
                            prefix_icon=ft.icons.PERSON,
                            autofocus=True,
                            col={'sm': 12, 'md': 4, 'lg': 2.28}
                        ),
                        
                        user := TextField(
                            hint_text='Username',
                            size=13,
                            color=ft.colors.BLACK,
                            prefix_icon=ft.icons.PERSON,
                            col={'sm': 12, 'md': 4, 'lg': 2.28}
                        ),
                        
                        email := TextField(
                            hint_text='Email',
                            size=13,
                            color=ft.colors.BLACK,
                            prefix_icon=ft.icons.EMAIL,
                            col={'sm': 12, 'md': 4, 'lg': 2.28}
                        ),
                        
                        cargo := ft.Dropdown(
                            label='Cargo',
                            label_style=ft.TextStyle(
                                size=13,
                                color=ft.colors.with_opacity(0.2, ft.colors.BLACK),
                                weight='bold'
                            ),
                            
                            text_style=ft.TextStyle(
                                size=13,
                                color=ft.colors.BLACK,
                                weight='bold'
                            ),
                            
                            prefix_icon=ft.icons.CATEGORY,
                            bgcolor=ft.colors.WHITE,
                            options=[
                                ft.dropdown.Option(text='Administrator'),
                                ft.dropdown.Option(text='Gestor'),
                            ],
                            col={'sm': 12, 'md': 4, 'lg': 2.28}
                        ),
                        
                        status := ft.Dropdown(
                            label='Status',
                            label_style=ft.TextStyle(
                                size=13,
                                color=ft.colors.with_opacity(0.2, ft.colors.BLACK),
                                weight='bold'
                            ),
                            
                            text_style=ft.TextStyle(
                                size=13,
                                color=ft.colors.BLACK,
                                weight='bold'
                            ),
                            
                            prefix_icon=ft.icons.KEY,
                            bgcolor=ft.colors.WHITE,
                            options=[
                                ft.dropdown.Option(text='Activo'),
                                ft.dropdown.Option(text='Inactivo'),
                            ],
                            col={'sm': 12, 'md': 4, 'lg': 2.28}
                        ),
                        
                        btn_addUser := FloatingButton(
                            bgcolor=ft.colors.BLUE,
                            icon=ft.icons.ADD,
                            col={'sm': 12, 'md': 4, 'lg': 0.6},
                            on_click=add_user
                        )
                    ]
                ),
                
                ft.Divider(
                    height=2,
                    color=ft.colors.WHITE,
                    visible=True
                ),
                
                ft.Text(
                    value='Todos os usuários'.upper(),
                    color=ft.colors.WHITE,
                    size=15,
                    weight='bold'
                ),
                
                tabela_usuarios := ft.DataTable(
                    show_bottom_border=True,
                    width=page.width,
                    
                    columns=[
                        ft.DataColumn(label=ft.Text(value='ID', size=13, color=ft.colors.WHITE, weight='bold')),
                        ft.DataColumn(label=ft.Text(value='Nome', size=13, color=ft.colors.WHITE, weight='bold')),
                        ft.DataColumn(label=ft.Text(value='Username', size=13, color=ft.colors.WHITE, weight='bold')),
                        ft.DataColumn(label=ft.Text(value='Email', size=13, color=ft.colors.WHITE, weight='bold')),
                        ft.DataColumn(label=ft.Text(value='Cargo', size=13, color=ft.colors.WHITE, weight='bold')),
                        ft.DataColumn(label=ft.Text(value='Status', size=13, color=ft.colors.WHITE, weight='bold')),
                        ft.DataColumn(label=ft.Text(value='Gerir', size=13, color=ft.colors.WHITE, weight='bold')),
                    ],
                    
                    rows= [
                        
                    ]
                )
            ]
        )
        
        load_users(e)
        
        def on_resize(e):
            tabela_usuarios.width = page.width
            page.update()
    
        page.on_resized.subscribe(on_resize)
        
        page.update()
    
    adminpanel = ft.Container(
        width=page.width,
        height=page.height,
        
        content=ft.Column(
            controls=[
                menu := ft.Row(
                    controls=[
                        ft.Row(
                            controls = [
                                IconButton(
                                    icon=ft.icons.MENU,
                                    color=ft.colors.WHITE,
                                    size=25,
                                    on_click=clicked
                                ),
                                
                                ft.Text(
                                    value='Sistema de Gestão de Requisições'.upper(),
                                    color=ft.colors.WHITE,
                                    size=16,
                                    weight='bold'
                                )
                            ]
                        ),
                        
                        ft.Row(
                            controls=[
                                ft.Text(
                                    value=f'{username}'.upper(),
                                    color=ft.colors.WHITE,
                                    size=16,
                                    weight='bold'
                                ),
                                
                                IconButton(
                                    icon=ft.icons.NOTIFICATIONS,
                                    color=ft.colors.WHITE,
                                    size=25,
                                    on_click=clicked
                                ),
                                
                                IconButton(
                                    icon=ft.icons.PERSON,
                                    color=ft.colors.WHITE,
                                    size=25,
                                    on_click=clicked
                                ),
                            ]
                        )  
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                ),
                
                ft.Divider(
                    height=1,
                    color=ft.colors.WHITE,
                    visible=True
                ),
                
                ft.Row(
                    controls=[
                        lateral_menu := ft.Column(
                            controls=[
                                IconButton(
                                    icon=ft.icons.MANAGE_ACCOUNTS,
                                    color=ft.colors.WHITE,
                                    size=25,
                                    on_click=manage_users
                                ),
                                
                                IconButton(
                                    icon=ft.icons.EDIT_DOCUMENT,
                                    color=ft.colors.WHITE,
                                    size=25,
                                    on_click=clicked
                                ),
                                
                                IconButton(
                                    icon=ft.icons.ARCHIVE,
                                    color=ft.colors.WHITE,
                                    size=25,
                                    on_click=clicked
                                ),
                            ],
                            
                        ),
                        
                        tela_principal := ft.Container(
                            width=page.width - 89,
                            height=page.height,
                            
                        )
                    ],
                    vertical_alignment=ft.CrossAxisAlignment.START
                )
            ]
        )
    )
    
    def on_resize(e):
        adminpanel.width=page.width
        adminpanel.height=page.height
        
        tela_principal.width=page.width - 89
        tela_principal.height=page.height
        
        page.update()
    
    page.on_resized.subscribe(on_resize)
    
    return adminpanel