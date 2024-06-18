from Auxiliar.controls import *

def main(page: ft.Page):
    page.title = 'Request Manager System'
    page.window_maximized = True
    page.theme_mode = ft.ThemeMode.DARK
    
    container = ft.Container(
        width= page.window_width,
        height= page.window_height,
        alignment=ft.alignment.center,
        
        content=ft.Column(
            controls=[
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
                            
                            btn_login := FloatingButton(
                                bgcolor=ft.colors.BLUE,
                                text='Login',
                                width=320,
                                height=40,
                            ),
                            
                            forgot_password := ft.TextButton(
                                text='Esqueci minha senha',
                                width=320,
                                
                                style=ft.ButtonStyle(
                                    color=ft.colors.BLUE,
                                ),
                            )
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    )
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER
        )
    )
    
    page.add(container)


if __name__ == '__main__':
    ft.app(target=main, assets_dir='assets')