from Auxiliar.controls import *

def adminPanel(page: ft.Page, username: str = 'Admin'):
    
    def clicked(e):
        page.snack_bar = SnackBar(value=f'{e.control}',icon=ft.icons.MENU_BOOK, color=ft.colors.BLUE)
        page.snack_bar.open = True
        
        page.update()
    
    def manage_users(e):
        
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
                        
                        FloatingButton(
                            bgcolor=ft.colors.BLUE,
                            icon=ft.icons.ADD,
                            col={'sm': 12, 'md': 4, 'lg': 0.6},
                            on_click=clicked
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
                    width=page.window_width,
                    
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
        
        def on_resize(e):
            tabela_usuarios.width = page.window_width
            page.update()
    
        page.on_resize.subscribe(on_resize)
        
        page.update()
    
    adminpanel = ft.Container(
        width=page.window_width,
        height=page.window_height,
        
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
                            width=page.window_width - 89,
                            height=page.window_height,
                            
                        )
                    ],
                    vertical_alignment=ft.CrossAxisAlignment.START
                )
            ]
        )
    )
    
    def on_resize(e):
        adminpanel.width=page.window_width
        adminpanel.height=page.window_height
        
        tela_principal.width=page.window_width - 89
        tela_principal.height=page.window_height
        
        page.update()
    
    page.on_resize.subscribe(on_resize)
    
    return adminpanel