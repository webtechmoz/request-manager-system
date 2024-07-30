from Auxiliar.controls import *
from Auxiliar.ClassRegex import REGEX
import string
from random import choice
from pathlib import Path
from Auxiliar.sqlmanager import criar_tabela, inserir_dados, ver_dados, encriptar_valor, editar_dados, apagar_dados
from Auxiliar.getDate import _getdate

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
                    width=page.window.width,
                    
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
            tabela_usuarios.width = page.window.width
            page.update()
    
        page.on_resized.subscribe(on_resize)
        
        page.update()
    
    def manage_requests(e: ft.ControlEvent):
        
        def load_requests():
            try:
                dados = ver_dados(
                    nomeTabela='pendentes',
                    conditions='status = "Pendente"'
                )
                
                tabela_requisicoes.rows.clear()                
                for dado in dados:
                    tabela_requisicoes.rows.append(
                        ft.DataRow(
                            cells=[
                                ft.DataCell(ft.Checkbox(value=False)),
                                ft.DataCell(ft.Text(value=dado[0], color=ft.colors.WHITE, size=12, weight='bold')),
                                ft.DataCell(ft.Text(value=dado[1], color=ft.colors.WHITE, size=12, weight='bold')),
                                ft.DataCell(ft.Text(value=dado[2], color=ft.colors.WHITE, size=12, weight='bold')),
                                ft.DataCell(ft.Text(value=dado[3], color=ft.colors.WHITE, size=12, weight='bold')),
                                ft.DataCell(ft.Text(value=dado[4], color=ft.colors.WHITE, size=12, weight='bold')),
                                ft.DataCell(ft.Text(value=dado[5], color=ft.colors.WHITE, size=12, weight='bold')),
                                ft.DataCell(ft.Text(value=dado[8], color=ft.colors.WHITE, size=12, weight='bold')),
                                ft.DataCell(ft.Text(value=dado[6], color=ft.colors.WHITE, size=12, weight='bold')),
                            ]
                        )
                    )
            
            except Exception as erro:
                page.snack_bar = SnackBar(value=f'Erro: {erro}',icon=ft.icons.CLOSE, color=ft.colors.RED)
                page.snack_bar.open = True
            
            page.update()
        
        def supplier_details(e: ft.ControlEvent):
            if e.control.value == 'Aprovado':
                detalhes_fornecedor.visible = True
            
            else:
                detalhes_fornecedor.visible = False
            
            page.update()
        
        def manage_request(e):
            if len(tabela_requisicoes.rows) > 0:
                selected_request = False
                for row in tabela_requisicoes.rows:
                    if row.cells[0].content.value == True:
                        selected_request = True
                        break
                
                if selected_request == True:
                    if decisao.value != None:
                        if decisao.value == 'Aprovado':
                            if notas.value != '' and precoUnitario.value != '' and fornecedor.value != '' and cidade.value != '' and morada.value != '' and nuit.value != '' and iva.value != '':
                                for row in tabela_requisicoes.rows:
                                    if row.cells[0].content.value == True:
                                        id = int(row.cells[1].content.value)
                                        
                                        editar_dados(
                                            nomeTabela='pendentes',
                                            dados=['status','Aprovado',f'id ="{id}"']
                                        )
                                        
                                        dados = ver_dados(
                                            nomeTabela='pendentes',
                                            conditions=f'id = "{id}"'
                                        )[0]
                                        
                                        criar_tabela('arquivadas')
                                        
                                        colunas = {
                                            'indice': id,
                                            'departamento': dados[1],
                                            'categoria': dados[2],
                                            'produto': dados[3],
                                            'descricao': dados[4],
                                            'quantidades': dados[5],
                                            'precoUnitario': precoUnitario.value,
                                            'valor': float(dados[5]) * float(precoUnitario.value),
                                            'dataRequisicao': dados[6],
                                            'status': dados[7],
                                            'usuario': dados[8],
                                            'dataDecisao': _getdate(),
                                            'notas': notas.value,
                                            'fornecedor': fornecedor.value,
                                            'cidade': cidade.value,
                                            'morada': morada.value,
                                            'nuit': nuit.value,
                                            'iva': iva.value
                                        }
                                        
                                        inserir_dados(
                                            nomeTabela='arquivadas',
                                            dados=colunas
                                        )
                                        
                                decisao.value = None
                                notas.value = ''
                                precoUnitario.value = ''
                                fornecedor.value = ''
                                cidade.value = ''
                                morada.value = ''
                                nuit.value = ''
                                iva.value = ''
                            
                            else:
                                snack_bar = SnackBar(value=f'Preencha todos os campos',icon=ft.icons.CLOSE, color=ft.colors.RED)
                                page.overlay.append(snack_bar)
                                snack_bar.open = True
                        
                        elif decisao.value == 'Reprovado':
                            if notas.value != '':
                                for row in tabela_requisicoes.rows:
                                    if row.cells[0].content.value == True:
                                        id = int(row.cells[1].content.value)
                                        
                                        editar_dados(
                                            nomeTabela='pendentes',
                                            dados=['status','Reprovado',f'id ="{id}"']
                                        )
                                        
                                        dados = ver_dados(
                                            nomeTabela='pendentes',
                                            conditions=f'id = "{id}"'
                                        )[0]
                                        
                                        criar_tabela('arquivadas')
                                        
                                        colunas = {
                                            'indice': id,
                                            'departamento': dados[1],
                                            'categoria': dados[2],
                                            'produto': dados[3],
                                            'descricao': dados[4],
                                            'quantidades': dados[5],
                                            'precoUnitario': 0,
                                            'valor': float(dados[5]) * 0,
                                            'dataRequisicao': dados[6],
                                            'status': dados[7],
                                            'usuario': dados[8],
                                            'dataDecisao': _getdate(),
                                            'notas': notas.value,
                                            'fornecedor': fornecedor.value,
                                            'cidade': cidade.value,
                                            'morada': morada.value,
                                            'nuit': nuit.value,
                                            'iva': iva.value
                                        }
                                        
                                        inserir_dados(
                                            nomeTabela='arquivadas',
                                            dados=colunas
                                        )
                                
                                decisao.value = None
                                notas.value = ''
                                precoUnitario.value = ''
                                fornecedor.value = ''
                                cidade.value = ''
                                morada.value = ''
                                nuit.value = ''
                                iva.value = ''
                            
                            else:
                                snack_bar = SnackBar(value=f'Preencha a justificativa da reprovação',icon=ft.icons.CLOSE, color=ft.colors.RED)
                                page.overlay.append(snack_bar)
                                snack_bar.open = True
                    
                    else:
                        snack_bar = SnackBar(value=f'Indique o tipo de decisão',icon=ft.icons.CLOSE, color=ft.colors.RED)
                        page.overlay.append(snack_bar)
                        snack_bar.open = True
                
                else:
                    snack_bar = SnackBar(value=f'Selecione pelo menos uma requisição',icon=ft.icons.CLOSE, color=ft.colors.RED)
                    page.overlay.append(snack_bar)
                    snack_bar.open = True
            
            else:
                snack_bar = SnackBar(value=f'Não existe nenhuma requisição pendente',icon=ft.icons.CLOSE, color=ft.colors.RED)
                page.overlay.append(snack_bar)
                snack_bar.open = True
            
            load_requests()
            page.update()
        
        tela_principal.content = ft.Column(
                controls=[
                    ft.Text(
                        value='Gestão de Requisições'.upper(),
                        color=ft.colors.WHITE,
                        size=15,
                        weight='bold'
                    ),
                    
                    ft.ResponsiveRow(
                        controls=[
                            decisao := ft.Dropdown(
                                label='Decisão',
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
                                
                                prefix_icon=ft.icons.RECYCLING,
                                bgcolor=ft.colors.WHITE,
                                options=[
                                    ft.dropdown.Option(text='Aprovado'),
                                    ft.dropdown.Option(text='Reprovado'),
                                ],
                                col={'sm': 12, 'md': 6, 'lg': 3.80},
                                on_change=supplier_details
                            ),
                            
                            notas := TextField(
                                hint_text='Notas de aprovação',
                                size=13,
                                color=ft.colors.BLACK,
                                prefix_icon=ft.icons.NOTES,
                                autofocus=True,
                                col={'sm': 12, 'md': 6, 'lg': 3.80}
                            ),
                            
                            precoUnitario := TextField(
                                hint_text='Preço unitário',
                                size=13,
                                color=ft.colors.BLACK,
                                prefix_icon=ft.icons.MONETIZATION_ON,
                                col={'sm': 12, 'md': 6, 'lg': 3.80}
                            ),
                            
                            btn_decision := FloatingButton(
                                bgcolor=ft.colors.BLUE,
                                icon=ft.icons.ADD,
                                col={'sm': 12, 'md': 6, 'lg': 0.6},
                                on_click=manage_request
                            )
                        ]
                    ),
                    
                    detalhes_fornecedor := ft.ResponsiveRow(
                        controls=[
                            fornecedor := TextField(
                                hint_text='Fornecedor',
                                size=13,
                                color=ft.colors.BLACK,
                                prefix_icon=ft.icons.PERSON,
                                autofocus=True,
                                col={'sm': 12, 'md': 12, 'lg': 2.40}
                            ),
                            
                            cidade := TextField(
                                hint_text='cidade',
                                size=13,
                                color=ft.colors.BLACK,
                                prefix_icon=ft.icons.PERSON,
                                autofocus=True,
                                col={'sm': 12, 'md': 6, 'lg': 2.40}
                            ),
                            
                            morada := TextField(
                                hint_text='morada',
                                size=13,
                                color=ft.colors.BLACK,
                                prefix_icon=ft.icons.PERSON,
                                autofocus=True,
                                col={'sm': 12, 'md': 6, 'lg': 2.40}
                            ),
                            
                            nuit := TextField(
                                hint_text='NUIT',
                                size=13,
                                color=ft.colors.BLACK,
                                prefix_icon=ft.icons.PERSON,
                                autofocus=True,
                                col={'sm': 12, 'md': 9, 'lg': 2.40}
                            ),
                            
                            iva := TextField(
                                hint_text='IVA',
                                size=13,
                                color=ft.colors.BLACK,
                                prefix_icon=ft.icons.PERCENT,
                                col={'sm': 12, 'md': 3, 'lg': 2.40}
                            )
                        ],
                        visible= False
                    ),
                    
                    ft.Divider(
                        height=2,
                        color=ft.colors.WHITE,
                        visible=True
                    ),
                    
                    ft.Text(
                        value='Requisições pendentes'.upper(),
                        color=ft.colors.WHITE,
                        size=15,
                        weight='bold'
                    ),
                    
                    ft.Column(
                        controls=[
                            tabela_requisicoes := ft.DataTable(
                                show_bottom_border=True,
                                width=page.window.width,
                                
                                columns=[
                                    ft.DataColumn(label=ft.Text(value='Gerir', size=13, color=ft.colors.WHITE, weight='bold')),
                                    ft.DataColumn(label=ft.Text(value='ID', size=13, color=ft.colors.WHITE, weight='bold')),
                                    ft.DataColumn(label=ft.Text(value='Departamento', size=13, color=ft.colors.WHITE, weight='bold')),
                                    ft.DataColumn(label=ft.Text(value='Categoria', size=13, color=ft.colors.WHITE, weight='bold')),
                                    ft.DataColumn(label=ft.Text(value='Produto', size=13, color=ft.colors.WHITE, weight='bold')),
                                    ft.DataColumn(label=ft.Text(value='Descrição', size=13, color=ft.colors.WHITE, weight='bold')),
                                    ft.DataColumn(label=ft.Text(value='Quantidades', size=13, color=ft.colors.WHITE, weight='bold'), numeric=True),
                                    ft.DataColumn(label=ft.Text(value='Usuário', size=13, color=ft.colors.WHITE, weight='bold')),
                                    ft.DataColumn(label=ft.Text(value='Data', size=13, color=ft.colors.WHITE, weight='bold')),
                                ],
                                
                                rows= [
                                    
                                ]
                            )
                        ],
                        height=500,
                        scroll=ft.ScrollMode.ADAPTIVE
                    )
                ],
                scroll=ft.ScrollMode.AUTO
            )
            
        def on_resize(e):
            tabela_requisicoes.width = page.window.width
            page.update()

        page.on_resized.subscribe(on_resize)
        load_requests()
        
        page.update()
    
    def archive_requests(e: ft.ControlEvent):
        
        def clear_all(e):
            decisao.value = None
            departamento.value = ''
            usuario.value = ''
            
            load_requests(e)
            
            page.update()
        
        def load_requests(e):
            
            condictions = '1 = 1 '
            colunas = 'indice, departamento, categoria, produto, descricao, quantidades, valor, status, dataDecisao, notas'
            
            if decisao.value != None:
                condictions += f'AND status LIKE "%{decisao.value}%" '
            
            if departamento.value != '':
                condictions += f'AND departamento LIKE "%{departamento.value}%" '
            
            if usuario.value != '':
                condictions += f'AND usuario LIKE "%{usuario.value}%"'
            
            dados = ver_dados(
                nomeTabela='arquivadas',
                conditions=condictions,
                colunas=colunas
            )
            
            tabela_requisicoes.rows.clear()
            for dado in dados:
                tabela_requisicoes.rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(
                                ft.Row(
                                    controls=[
                                        IconButton(icon=ft.icons.EDIT,color=ft.colors.BLUE, size=18, on_click=clicked),
                                        IconButton(icon=ft.icons.DELETE,color=ft.colors.RED, size=18, on_click=clicked)
                                    ]
                                )
                            ),
                            
                            ft.DataCell(ft.Text(value=dado[0], color=ft.colors.WHITE, size=12, weight='bold')),
                            ft.DataCell(ft.Text(value=dado[1], color=ft.colors.WHITE, size=12, weight='bold')),
                            ft.DataCell(ft.Text(value=dado[2], color=ft.colors.WHITE, size=12, weight='bold')),
                            ft.DataCell(ft.Text(value=dado[3], color=ft.colors.WHITE, size=12, weight='bold')),
                            ft.DataCell(ft.Text(value=dado[4], color=ft.colors.WHITE, size=12, weight='bold')),
                            ft.DataCell(ft.Text(value=dado[5], color=ft.colors.WHITE, size=12, weight='bold')),
                            ft.DataCell(ft.Text(value=dado[6], color=ft.colors.WHITE, size=12, weight='bold')),
                            ft.DataCell(ft.Text(value=dado[7], color=ft.colors.WHITE, size=12, weight='bold')),
                            ft.DataCell(ft.Text(value=dado[8], color=ft.colors.WHITE, size=12, weight='bold')),
                            ft.DataCell(ft.Text(value=dado[9], color=ft.colors.WHITE, size=12, weight='bold')),
                        ]
                    )
                )
            
            page.update()
                
        
        tela_principal.content = ft.Column(
                controls=[
                    ft.Text(
                        value='Gestão de Requisições'.upper(),
                        color=ft.colors.WHITE,
                        size=15,
                        weight='bold'
                    ),
                    
                    ft.ResponsiveRow(
                        controls=[
                            decisao := ft.Dropdown(
                                label='Decisão',
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
                                
                                prefix_icon=ft.icons.FILTER_ALT,
                                bgcolor=ft.colors.WHITE,
                                options=[
                                    ft.dropdown.Option(text='Aprovado'),
                                    ft.dropdown.Option(text='Reprovado'),
                                ],
                                col={'sm': 12, 'md': 6, 'lg': 3.80},
                                on_change=lambda e: load_requests(e)
                            ),
                            
                            departamento := TextField(
                                hint_text='Departamento',
                                size=13,
                                color=ft.colors.BLACK,
                                prefix_icon=ft.icons.FILTER_ALT,
                                autofocus=True,
                                col={'sm': 12, 'md': 6, 'lg': 3.80},
                                on_change=lambda e: load_requests(e)
                            ),
                            
                            usuario := TextField(
                                hint_text='Usuário',
                                size=13,
                                color=ft.colors.BLACK,
                                prefix_icon=ft.icons.FILTER_ALT,
                                col={'sm': 12, 'md': 6, 'lg': 3.80},
                                on_change=lambda e: load_requests(e)
                            ),
                            
                            btn_decision := FloatingButton(
                                bgcolor=ft.colors.BLUE,
                                icon=ft.icons.CLEAR_ALL,
                                col={'sm': 12, 'md': 6, 'lg': 0.6},
                                on_click=clear_all
                            )
                        ]
                    ),
                    
                    ft.Divider(
                        height=2,
                        color=ft.colors.WHITE,
                        visible=True
                    ),
                    
                    ft.Text(
                        value='Requisições Arquivadas'.upper(),
                        color=ft.colors.WHITE,
                        size=15,
                        weight='bold'
                    ),
                    
                    ft.Column(
                        controls=[
                            tabela_requisicoes := ft.DataTable(
                                show_bottom_border=True,
                                width=page.window.width,
                                
                                columns=[
                                    ft.DataColumn(label=ft.Text(value='Gerir', size=13, color=ft.colors.WHITE, weight='bold')),
                                    ft.DataColumn(label=ft.Text(value='ID', size=13, color=ft.colors.WHITE, weight='bold')),
                                    ft.DataColumn(label=ft.Text(value='Departamento', size=13, color=ft.colors.WHITE, weight='bold')),
                                    ft.DataColumn(label=ft.Text(value='Categoria', size=13, color=ft.colors.WHITE, weight='bold')),
                                    ft.DataColumn(label=ft.Text(value='Produto', size=13, color=ft.colors.WHITE, weight='bold')),
                                    ft.DataColumn(label=ft.Text(value='Descrição', size=13, color=ft.colors.WHITE, weight='bold')),
                                    ft.DataColumn(label=ft.Text(value='Quantidades', size=13, color=ft.colors.WHITE, weight='bold'), numeric=True),
                                    ft.DataColumn(label=ft.Text(value='Valor', size=13, color=ft.colors.WHITE, weight='bold'), numeric=True),
                                    ft.DataColumn(label=ft.Text(value='Decisao', size=13, color=ft.colors.WHITE, weight='bold')),
                                    ft.DataColumn(label=ft.Text(value='DataDecisao', size=13, color=ft.colors.WHITE, weight='bold')),
                                    ft.DataColumn(label=ft.Text(value='Notas', size=13, color=ft.colors.WHITE, weight='bold')),
                                ],
                                
                                rows= [
                                    
                                ]
                            )
                        ],
                        height=500,
                        scroll=ft.ScrollMode.ADAPTIVE
                    )
                ],
                scroll=ft.ScrollMode.AUTO
            )
            
        def on_resize(e):
            tabela_requisicoes.width = page.window.width
            page.update()

        page.on_resized.subscribe(on_resize)
        load_requests(e)
        page.update()
    
    adminpanel = ft.Container(
        width=page.window.width,
        height=page.window.height,
        
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
                                    on_click=manage_requests
                                ),
                                
                                IconButton(
                                    icon=ft.icons.ARCHIVE,
                                    color=ft.colors.WHITE,
                                    size=25,
                                    on_click=archive_requests
                                ),
                            ],
                            
                        ),
                        
                        tela_principal := ft.Container(
                            width=page.window.width - 89,
                            height=page.window.height,
                            
                        )
                    ],
                    vertical_alignment=ft.CrossAxisAlignment.START
                )
            ]
        )
    )
    
    def on_resize(e):
        adminpanel.width=page.window.width
        adminpanel.height=page.window.height
        
        tela_principal.width=page.window.width - 89
        tela_principal.height=page.window.height
        
        page.update()
    
    page.on_resized.subscribe(on_resize)
    
    return adminpanel