import flet as ft
from Helpers import SQLite
from datetime import date



def addToDatabase(e):
    if (project.value != "Select Project...") & (actDescription.value != ""):
        db = SQLite.ActivitivityLogDB()
        db.insertActivity((year.value, month.value, day.value, project.value,
                        hoursText.value, actDescription.value))
        
        e.page.show_snack_bar(ft.SnackBar(ft.Text("Activity was added successfully!"), bgcolor=ft.colors.GREEN_200, open=True))
        db.connection.close()

        #clear the form after insrting data to DB
        project.value = "Select Project..."
        hoursSlider.value = 1
        actDescription.value = ""
        e.page.update()

    else:
        e.page.show_snack_bar(ft.SnackBar(ft.Text("Project and Activity must be entered!"), bgcolor=ft.colors.RED_200, open=True))


def project_changed(e):
    if(e.control.value != "Select Project..."):
        e.page.floating_action_button.visible = True
        e.page.update()
    
    else:
        e.page.floating_action_button.visible = False
        e.page.update()


def slider_changed(e):
    hoursText.value = e.control.value
    e.page.update()


def updateProjects():
    db = SQLite.ActivitivityLogDB()
    if db.tableExist("projects"):
        project.options=[ft.dropdown.Option("Select Project...")]
        rows = db.select_all("projects")
        for row in rows:
            if row[2]:
                project.options.append(ft.dropdown.Option(row[0]))    
            
    db.connection.close()
    


day    = ft.TextField(label="Date", bgcolor='#24292F', border_color='#3C4757',  width=120 ,value= date.today().day, expand=True)
month   = ft.TextField(label="Month", bgcolor='#24292F', border_color='#3C4757', width=120, value= date.today().month, expand=True)
year    = ft.TextField(label="Year", bgcolor='#24292F', border_color='#3C4757', width=120, value= date.today().year, expand=True)

project = ft.Dropdown(
            width=380,
            border_color='#3C4757',
            bgcolor='#24292F',
            filled=True,
            options=[ft.dropdown.Option("Select Project...")],
            value="Select Project...",
            on_change=project_changed,
            expand=True)


hoursSlider = ft.Slider(min=0, max=8, divisions=8, value=1, label="{value} h", on_change=slider_changed, expand=True)
hoursText   = ft.TextField(label="Duration [h]", bgcolor='#24292F', border_color='#3C4757', width=120, value= 1)

actDescription = ft.TextField(
                    label="Activity Description", 
                    border_color='#3C4757',
                    bgcolor='#24292F',
                    multiline=True,
                    max_lines=3,
                    expand=True
                )

space_20x80 = ft.Container(width=20, height=80)
space_10x80 = ft.Container(width=10, height=80)


def Show(page: ft.Page):
    updateProjects()
    page.clean()
    #page.window_min_width=600
    page.window_width=600
    page.floating_action_button = ft.FloatingActionButton(icon=ft.icons.ADD, on_click=addToDatabase, bgcolor=ft.colors.BLUE, visible=False)
    page.add(
        ft.Row([space_10x80, project, space_10x80], alignment=ft.MainAxisAlignment.CENTER),
        ft.Row([space_20x80, day, space_20x80, month, space_20x80, year, space_20x80], alignment=ft.MainAxisAlignment.SPACE_EVENLY),
        ft.Row([space_10x80, hoursText, space_20x80, hoursSlider, ]),
        ft.Row([space_10x80, actDescription, space_10x80]),
        
    )
    page.update()