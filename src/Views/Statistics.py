import flet as ft



def Show(page: ft.Page):
    page.clean()
    page.window_width=600
    page.add(
        ft.Text("Statistics page - TODO"),
    )
    page.update()