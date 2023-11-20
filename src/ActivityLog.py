import flet as ft
from Views import Home, Activities, Projects, Statistics

def main(page: ft.Page):
    page.theme_mode = "dark"
    page.title = "Activity Log"
    page.window_always_on_top = True
    page.window_height = 600
    page.window_min_height = 600
    page.window_min_width=600
    page.window_center()
    page.scroll = ft.ScrollMode.AUTO
    

    page.navigation_bar = ft.NavigationBar(
        destinations=[
            ft.NavigationDestination(icon=ft.icons.CALENDAR_MONTH, label="Activity Overview"),
            ft.NavigationDestination(icon=ft.icons.ASSIGNMENT_ADD, label="Add Activity"),
            ft.NavigationDestination(icon=ft.icons.BUSINESS_CENTER, label="Projects"),
            ft.NavigationDestination(icon=ft.icons.DATA_EXPLORATION, label="Statistics")
        ], on_change=lambda e: nav_bar_click(e.control.selected_index)
    )

    page.banner = ft.Banner(
        bgcolor=ft.colors.RED_200,
        leading=ft.Icon(ft.icons.WARNING_AMBER_ROUNDED, color=ft.colors.RED_400, size=50))
    

    # Function to handle navigation menu buttons
    def nav_bar_click(e):
        match e:
            case 0:
                Home.Show(page)
            case 1:
                Activities.Show(page)
            case 2:
                Projects.Show(page)
            case 3:
                Statistics.Show(page)
                

    Home.Show(page)

ft.app(target=main)            


