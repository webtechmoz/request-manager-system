from Auxiliar.controls import *

def adminPanel(page: ft.Page, username: str = 'Admin'):
    
    def clicked(e):
        page.snack_bar = SnackBar(value=f'{e.control}',icon=ft.icons.MENU_BOOK, color=ft.colors.BLUE)
        page.snack_bar.open = True
        
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
                                    on_click=clicked
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