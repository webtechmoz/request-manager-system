import flet as ft

def TextField(hint_text: str, size: int, color: ft.colors, prefix_icon: ft.icons = None, sufix_icon: ft.icons = None, autofocus: bool = False, border: ft.InputBorder = ft.InputBorder.OUTLINE, on_change: ft.ControlEvent = None, password: bool = False, col: dict = {'sm': 12, 'md': 4}):
    
    textfield = ft.TextField(
        hint_text=hint_text,
        hint_style=ft.TextStyle(
            size=size,
            weight='bold',
            color=ft.colors.with_opacity(0.2, color)
        ),
        
        text_style=ft.TextStyle(
            size=size,
            weight='bold',
            color=color
        ),
        
        prefix_icon=prefix_icon,
        suffix_icon=sufix_icon,
        border=border,
        on_change=on_change,
        password=password,
        autofocus=autofocus,
        col=col
    )
    
    return textfield

def FloatingButton(bgcolor: ft.colors, text: str = None, icon: ft.icons = None, on_click: ft.ControlEvent = None, width: int = None, height: int = None, col: dict = {'sm': 12, 'md': 4}):
    
    floatingbutton = ft.FloatingActionButton(
        bgcolor=bgcolor,
        height=height,
        width=width,
        text=text,
        icon=icon,
        col=col,
        on_click=on_click,
        mouse_cursor=ft.MouseCursor.CLICK
    )
    
    return floatingbutton
