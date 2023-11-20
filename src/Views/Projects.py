import flet as ft
from Helpers import SQLite



def updateListView():
    db = SQLite.ActivitivityLogDB()
    if db.tableExist("projects"):
        rows = db.select_all("projects")
        projListView.controls.clear()
        for row in rows:
            projListView.controls.append(
                ft.Container(
                    content=ft.ListTile(
                                leading=ft.Checkbox(value=bool(row[2]), disabled=True),
                                title=ft.Row([
                                        ft.Text("Project: ", size=14, color=ft.colors.GREY_700),
                                        ft.Text(row[0], size=18, color=ft.colors.GREY_400, selectable=True)]),
                                subtitle=ft.Row([
                                            ft.Text("Job      : ", size=14, color=ft.colors.GREY_700),
                                            ft.Text(row[1], size=14, color=ft.colors.GREY_400, selectable=True)]),
                                trailing=ft.PopupMenuButton(
                                            icon=ft.icons.MORE_VERT,
                                            items=[
                                                ft.PopupMenuItem(text="Edit", icon=row[0], on_click=open_dlg_modal),
                                                ft.PopupMenuItem(text="Delete", icon=row[0], on_click=open_dlg_modal)
                                            ])),
                    bgcolor='#24292F',
                    border_radius=5,
                    margin=4,
                    shadow = ft.BoxShadow(
                                spread_radius=0.1,
                                blur_radius=2,
                                color=ft.colors.BLACK,
                                offset=ft.Offset(1, 1),
                                blur_style=ft.ShadowBlurStyle.NORMAL)
                )
            )

    db.connection.close()


def open_dlg_modal(e):
    global projectName, jobNumber, jobEnab

    if(str(e.control).startswith('popupmenuitem')):
        if(e.control.text == "Edit"):
            db = SQLite.ActivitivityLogDB()
            row = db.selectProject(e.control.icon)
            db.connection.close()
            dlg_modal.content = ft.Stack([
                                    ft.Row([ft.TextField(label="Project Name", value=row[0], disabled=True, on_change=projNameChg, border_color=ft.colors.GREY, width=220)], top=10),
                                    ft.Row([ft.TextField(label="Job Number", value=row[1], on_change=jobNumberChg,border_color=ft.colors.GREY, width=220)], top=90),
                                    ft.Row([ft.Checkbox(label="Show in activity dropdown", value=bool(row[2]), on_change=jobEnabChg)], top=170)
                                ], expand=True)
            dlg_modal.actions = [ft.TextButton("Update", on_click=close_dlg), ft.TextButton("Cancel", on_click=close_dlg)]
            
            projectName = row[0]
            jobNumber = row[1]
            jobEnab = row[2]

            e.page.dialog = dlg_modal
            dlg_modal.open = True
            e.page.update()

        elif(e.control.text == "Delete"):
            db = SQLite.ActivitivityLogDB()
            db.deleteProject(e.control.icon)
            db.connection.close()
            updateListView()
            e.page.update()
            e.page.show_snack_bar(ft.SnackBar(ft.Text("Project deleted successfully!"), bgcolor=ft.colors.GREEN_200, open=True))

    else:
        dlg_modal.content = ft.Stack([
                                ft.Row([ft.TextField(label="Project Name", value="", on_change=projNameChg, border_color=ft.colors.GREY, width=220)], top=10),
                                ft.Row([ft.TextField(label="Job Number", value="", on_change=jobNumberChg,border_color=ft.colors.GREY, width=220)], top=90),
                                ft.Row([ft.Checkbox(label="Show in activity dropdown", value=True, on_change=jobEnabChg)], top=170)
                            ], expand=True)
        dlg_modal.actions = [ft.TextButton("Save", on_click=close_dlg), ft.TextButton("Cancel", on_click=close_dlg)]
        
        e.page.dialog = dlg_modal
        dlg_modal.open = True
        e.page.update()

    


def close_dlg(e):
    dlg_modal.open = False
    e.page.update()
    
    if(e.control.text == "Save"):
        if (projectName != ""):
            db = SQLite.ActivitivityLogDB()
            if db.tableExist("projects"):
                rows = db.select_all("projects")
                for row in rows:
                    if(row[0] == projectName):
                        e.page.show_snack_bar(ft.SnackBar(ft.Text("Project already exist!"), bgcolor=ft.colors.RED_200, open=True))
                        return
            if jobNumber != "":        
                db.insertProject((projectName, jobNumber, True, ""))
            else:
                db.insertProject((projectName, "Not defined", True, ""))
            
            db.connection.close()

            updateListView()
            e.page.update()
            e.page.show_snack_bar(ft.SnackBar(ft.Text("Project was added successfully!"), bgcolor=ft.colors.GREEN_200, open=True))
        else:
            e.page.show_snack_bar(ft.SnackBar(ft.Text("Project name must be entered!"), bgcolor=ft.colors.RED_200, open=True))

    elif(e.control.text == "Update"):
        db = SQLite.ActivitivityLogDB()
        if jobNumber != "":
            db.updateProject(projectName, jobNumber, bool(jobEnab))
        else:
            db.updateProject(projectName, "Not defined", bool(jobEnab))

        db.connection.close()

        updateListView()
        e.page.update()
        e.page.show_snack_bar(ft.SnackBar(ft.Text("Project was updated successfully!"), bgcolor=ft.colors.GREEN_200, open=True))


def win_resize(page: ft.Page):
    projListView.height = page.window_height - 200


def projNameChg(e):
    global projectName
    projectName = e.control.value


def jobNumberChg(e):
    global jobNumber
    jobNumber = e.control.value

def jobEnabChg(e):
    global jobEnab
    jobEnab = e.control.value


projectName = ""
jobNumber = ""
jobEnab = True

projListView = ft.ListView(spacing=5, padding=10, auto_scroll=True)

dlg_modal = ft.AlertDialog(
    modal=True,
    title=ft.Text("Project info:"),
    actions_alignment=ft.MainAxisAlignment.END
)


def Show(page: ft.Page):
    updateListView()
    page.clean()
    #self.page.window_min_width=600
    page.window_width=600
    page.floating_action_button = ft.FloatingActionButton(icon=ft.icons.ADD, on_click=lambda e: open_dlg_modal(e), bgcolor=ft.colors.BLUE)
    page.on_resize = win_resize(page)
    page.add(
        ft.Column([
            projListView,
        ])  
    )
    page.update()