import flet as ft
from core.theme import Colors, Radius, Typography

def main(page: ft.Page):
    page.title = "SMS — Mensageria & Guia Local"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = Colors.BACKGROUND
    page.padding = 0
    page.window.width = 410
    page.window.height = 840
    page.window.resizable = True
    page.fonts = {
        Typography.FONT_FAMILY: "https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap"
    }
    
    # Estado da aplicação
    current_mode = "pessoal" # 'pessoal' ou 'comercial'
    
    def switch_mode(e):
        nonlocal current_mode
        current_mode = "comercial" if current_mode == "pessoal" else "pessoal"
        update_ui()
    
    header = ft.Container(
        content=ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                ft.Row(
                    controls=[
                        ft.IconButton(
                            icon=ft.icons.MENU,
                            icon_color=Colors.ON_SURFACE,
                            on_click=lambda e: print("Abrir menu lateral")
                        ),
                        ft.Text("Mensagens", size=20, weight=ft.FontWeight.W_700, color=Colors.ON_SURFACE)
                    ]
                ),
                ft.Row(
                    controls=[
                        ft.IconButton(icon=ft.icons.SEARCH, icon_color=Colors.ON_SURFACE),
                        ft.IconButton(icon=ft.icons.MAP_OUTLINED, icon_color=Colors.PRIMARY),
                    ]
                )
            ]
        ),
        padding=ft.padding.symmetric(horizontal=12, vertical=8),
        bgcolor=Colors.SURFACE_CONTAINER_LOWEST,
        border=ft.border.only(bottom=ft.border.BorderSide(0.5, Colors.OUTLINE))
    )
    
    mode_indicator = ft.Container(
        content=ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                ft.ElevatedButton(
                    text="Alternar Modo (Pessoal / Comercial)",
                    icon=ft.icons.SWAP_HORIZ,
                    style=ft.ButtonStyle(
                        bgcolor=Colors.PRIMARY,
                        color=Colors.ON_PRIMARY,
                        shape=ft.RoundedRectangleBorder(radius=Radius.FULL)
                    ),
                    on_click=switch_mode
                )
            ]
        ),
        padding=10
    )
    
    feed_list = ft.ListView(
        expand=True,
        spacing=8,
        padding=12,
        controls=[
            ft.Container(
                content=ft.Row(
                    controls=[
                        ft.CircleAvatar(
                            content=ft.Icon(ft.icons.STOREFRONT, color=Colors.ON_PRIMARY),
                            bgcolor=Colors.SECONDARY,
                            radius=24
                        ),
                        ft.Column(
                            controls=[
                                ft.Row(
                                    controls=[
                                        ft.Text("Café Bistrô & Confeitaria", weight=ft.FontWeight.BOLD, size=15, color=Colors.ON_SURFACE),
                                        ft.Icon(ft.icons.VERIFIED, color=Colors.SECONDARY, size=16),
                                    ],
                                    alignment=ft.MainAxisAlignment.START,
                                    spacing=4
                                ),
                                ft.Text("Pedido #104 confirmado com sucesso", size=13, color=Colors.TEXT_SECONDARY)
                            ],
                            spacing=2,
                            expand=True
                        ),
                        ft.Column(
                            controls=[
                                ft.Text("10:42", size=11, color=Colors.TEXT_SECONDARY),
                                ft.Container(
                                    content=ft.Text("1", size=10, color=Colors.ON_PRIMARY, weight=ft.FontWeight.BOLD),
                                    bgcolor=Colors.PRIMARY,
                                    border_radius=Radius.FULL,
                                    padding=ft.padding.symmetric(horizontal=6, vertical=2)
                                )
                            ],
                            horizontal_alignment=ft.CrossAxisAlignment.END,
                            spacing=4
                        )
                    ]
                ),
                padding=12,
                bgcolor=Colors.SURFACE_CONTAINER_LOWEST,
                border_radius=Radius.LG,
                border=ft.border.all(0.5, Colors.OUTLINE)
            )
        ]
    )
    
    def update_ui():
        if current_mode == "pessoal":
            mode_indicator.content.controls[0].style.bgcolor = Colors.PRIMARY
            mode_indicator.content.controls[0].text = "Modo Atual: Pessoal (Esmeralda)"
        else:
            mode_indicator.content.controls[0].style.bgcolor = Colors.SECONDARY
            mode_indicator.content.controls[0].text = "Modo Atual: Comercial (Ciano)"
        page.update()

    page.add(
        ft.Column(
            controls=[
                header,
                mode_indicator,
                feed_list
            ],
            expand=True,
            spacing=0
        )
    )

if __name__ == "__main__":
    ft.app(target=main)
