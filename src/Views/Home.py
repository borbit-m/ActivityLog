import flet as ft
import copy
from Helpers import SQLite
from datetime import datetime, date, timedelta


###### Functions ######    
def rev_click(e):
    global actYear
    global weekNumberSelected
    weekNumberSelected -= 1
    if (weekNumberSelected <= 0):
        actYear -= 1
        weekNumberSelected = date(actYear,12,28).isocalendar().week
    
    e.page.controls[1] = week_activities(week_start_date(weekNumberSelected))
    update_month(weekNumberSelected)
    #yearButton.content.value = str(actYear)
    e.page.update()

    print(actYear)
    print(weekNumberSelected)
    
    

def fwd_click(e):
    global actYear
    global weekNumberSelected
    weekNumberSelected += 1
    if (weekNumberSelected > date(actYear,12,28).isocalendar().week):
        actYear +=1
        weekNumberSelected = 1
    e.page.controls[1] = week_activities(week_start_date(weekNumberSelected))
    update_month(weekNumberSelected)
    #yearButton.content.value = str(actYear)
    e.page.update()

    print(actYear)
    print(weekNumberSelected)


def month_change(e):
    global actYear
    global weekNumberSelected
    monthNum = datetime.strptime(e.control.text, '%B').month
    weekNumberSelected = date(actYear,monthNum,1).isocalendar().week
    e.page.controls[1] = week_activities(week_start_date(weekNumberSelected))
    update_month(weekNumberSelected)
    e.page.update()


def today_button_click(e):
    global weekNumberSelected
    weekNumberSelected = date.today().isocalendar().week
    e.page.controls[1] = week_activities(week_start_date(weekNumberSelected))
    update_month(weekNumberSelected)
    e.page.update()
    

def edit_mode_change(e):
    global editMode
    editMode = not editMode
    e.control.icon_color = ft.colors.BLUE if editMode else '#C2C7CF'
    e.page.update()


def projectChg(e):
    global project, duration, activityDesc
    project = e.control.value
    duration = e.page.dialog.content.controls[2].value
    activityDesc = e.page.dialog.content.controls[4].value



def durationChg(e):
    global project, duration, activityDesc
    duration = e.control.value
    project = e.page.dialog.content.controls[0].value
    activityDesc = e.page.dialog.content.controls[4].value


def activityDescChg(e):
    global project, duration, activityDesc
    activityDesc = e.control.value
    project = e.page.dialog.content.controls[0].value
    duration = e.page.dialog.content.controls[2].value
    


def open_actDialog(e):
    actID = e.control.image_src
    db = SQLite.ActivitivityLogDB()
    act = db.selectActivity(actID)
    proj = db.selectProject(act[4])
    projList = []
    projExist = False
    rows = db.select_all("projects")
    for row in rows:
        if row[2]:
            projList.append(ft.dropdown.Option(row[0]))
            if(not projExist):
               projExist = row[0] == act[4]

    if(not projExist):
        projList.append(ft.dropdown.Option(act[4]))

    db.connection.close()

    if(editMode):
        actDialog.content = ft.Column([
                                ft.Dropdown(width=240, height=60, bgcolor='#24292F', border_color='#3C4757', filled=True, on_change=projectChg,
                                    options=projList, value=act[4]),
                                ft.Divider(height=10, color=ft.colors.TRANSPARENT),
                                ft.TextField(label="Duration [h]", value=act[5], on_change=durationChg, bgcolor='#24292F', border_color='#3C4757', width=240),
                                ft.Divider(height=10, color=ft.colors.TRANSPARENT),
                                ft.TextField(label="Activity", value=act[6], on_change=activityDescChg, multiline=True, max_lines=6, bgcolor='#24292F', border_color='#3C4757', width=240)
                            ], alignment=ft.MainAxisAlignment.START)
        actDialog.actions = [ft.TextButton("Delete", on_click= lambda e: close_dlg(e, actID)), ft.TextButton("Update", on_click=lambda e: close_dlg(e, actID)), ft.TextButton("Cancel", on_click=lambda e: close_dlg(e, actID))]
        actDialog.actions_alignment=ft.MainAxisAlignment.END
        actDialog.modal = True
    else:
        actDialog.content = ft.Column([
                                ft.TextField(label="Project", value=act[4], read_only=True, bgcolor='#24292F', border_color='#3C4757', width=240),
                                ft.Divider(height=10, color=ft.colors.TRANSPARENT),
                                ft.TextField(label="Duration [h]", value=act[5], read_only=True, bgcolor='#24292F', border_color='#3C4757', width=240),
                                ft.Divider(height=10, color=ft.colors.TRANSPARENT),
                                ft.TextField(label="Job Number:", value=proj[1], read_only=True, bgcolor='#24292F', border_color='#3C4757', width=240),
                                ft.Divider(height=10, color=ft.colors.TRANSPARENT),
                                ft.TextField(label="Activity", value=act[6], read_only=True, multiline=True, max_lines=6, bgcolor='#24292F', border_color='#3C4757', width=240)
                            ], alignment=ft.MainAxisAlignment.START)
        actDialog.actions = None
        actDialog.modal = False

    
    e.page.dialog = actDialog
    actDialog.open = True
    e.page.update()


def close_dlg(e, actID):
    global editMode
    editMode = False
    e.page.controls[0].controls[2].icon_color = '#C2C7CF'
    
    actDialog.open = False
    e.page.update()

    if(e.control.text == "Delete"):
        e.page.banner.actions=[ft.ElevatedButton("Delete", on_click=lambda e: close_banner(e, actID)), ft.ElevatedButton("Cancel", on_click=lambda e: close_banner(e, actID))]
        e.page.banner.content=ft.Text("Do you want to delete this activity?", color='#3B4858', size=20, weight=ft.FontWeight.W_500)
        e.page.banner.open = True
        e.page.update()
    
    elif(e.control.text == "Update"):
        db = SQLite.ActivitivityLogDB()
        db.updateActivity(actID, project, duration, activityDesc)
        db.connection.close()

        global weekNumberSelected
        e.page.controls[1] = week_activities(week_start_date(weekNumberSelected))
        monthButton.content = update_month(weekNumberSelected)
        e.page.show_snack_bar(ft.SnackBar(ft.Text("Activity updated successfully!"), bgcolor=ft.colors.GREEN_200, open=True))
        e.page.update()
    

def close_banner(e, actID):
    e.page.banner.open = False
    e.page.update()
    
    if(e.control.text == "Delete"):
        db = SQLite.ActivitivityLogDB()
        db.deleteActivity(actID)
        db.connection.close()

        global weekNumberSelected
        e.page.controls[1] = week_activities(week_start_date(weekNumberSelected))
        monthButton.content = update_month(weekNumberSelected)
        e.page.show_snack_bar(ft.SnackBar(ft.Text("Activity deleted successfully!"), bgcolor=ft.colors.GREEN_200, open=True))
        e.page.update()
       

def week_activities(startDate: date):
    db = SQLite.ActivitivityLogDB()
    tableExist = db.tableExist("activities")
    
    days = ['MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT', 'SUN']
    dateContainers = []
    activityColumns = []
    totTimeColumns = []
    actContainersSpacing = 2
    tmpDateCont = copy.deepcopy(emptyContainer)
    tmpTotTimeCont = copy.deepcopy(emptyContainer)
    tmpActivityCont = copy.deepcopy(actContainer)
    tmpActivityCont.on_click = lambda e: open_actDialog(e)

    for i in range(0, 7):
        columnDate = startDate + timedelta(days=i)

        # Populate activities
        actSingleColumn = []
        totTime = 0
        if tableExist:
            rows = db.selectActivities(columnDate)
            if len(rows) > 0:
                for row in rows:
                    totTime += row[5]
                        
                    tmpActivityCont.content = ft.Column([
                                                ft.Text((row[4][:11] + '..') if len(row[4]) > 11 else row[4], color=ft.colors.GREY_400, size=14),
                                                ft.Text("("+str(row[5])+"h)", color=ft.colors.GREY_400, size=12, visible=True if row[5] >= 2 else False)
                                            ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
                    spacingCorrection = ((len(rows) - 1 ) * actContainersSpacing * 2 / len(rows)) * 2
                    tmpActivityCont.height = (row[5] / 8 * 240) - spacingCorrection
                    tmpActivityCont.image_src = row[0]

                    actSingleColumn.append(copy.deepcopy(tmpActivityCont))
                
            else:
                actSingleColumn.append(emptyContainer)

            tmpTotTimeCont.content = ft.Column([
                                    ft.Text("Total [h]: "+str(totTime), color='#C2C7CF', size=14),
                                ], alignment=ft.MainAxisAlignment.START, horizontal_alignment=ft.CrossAxisAlignment.CENTER)    
        
        # Populate dates
        if(columnDate.weekday() > 4):
            dayColor = '#E14105'
        else:
            dayColor = '#C2C7CF'
        
        if (columnDate == date.today()):
            dayColor = ft.colors.BLUE

        tmpDateCont.content = ft.Column([
                                    ft.Text(days[columnDate.weekday()], color=dayColor, size=12),
                                    ft.Text(columnDate.day, color=dayColor, size=24, weight=ft.FontWeight.W_500),
                                ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=3)


        dateContainers.append(copy.deepcopy(tmpDateCont))
        activityColumns.append(copy.deepcopy(ft.Column(actSingleColumn, spacing=actContainersSpacing)))
        totTimeColumns.append(copy.deepcopy(tmpTotTimeCont))
        
    db.connection.close()

    return ft.Column([
                ft.Divider(thickness=0.5, height=4, color='#3C4757'),
                ft.Row(dateContainers, alignment=ft.MainAxisAlignment.SPACE_EVENLY),
                ft.Divider(thickness=0.5, height=4, color='#3C4757'),
                ft.Row(activityColumns, alignment=ft.MainAxisAlignment.SPACE_EVENLY, vertical_alignment=ft.CrossAxisAlignment.START),
                ft.Divider(thickness=0.5, height=4, color='#3C4757'),
                ft.Row(totTimeColumns, alignment=ft.MainAxisAlignment.SPACE_EVENLY)
            ])


def week_start_date(weekNumber):
    global actYear
    yearBeginWeekday=date(actYear, 1, 1).weekday()
    if (yearBeginWeekday == 0):
        return date(actYear, 1, 1) + timedelta(days=((weekNumber-1)*7))
    else:
        return date(actYear, 1, 1) + timedelta(days=((weekNumber)*7)-yearBeginWeekday)


def update_month(weekNumber):
    global actYear
    weekEndDate = week_start_date(weekNumber) + timedelta(days=6)
    month = weekEndDate.strftime('%B')
    monthButton.content.value = month
    yearButton.content.value = str(weekEndDate.year)
    monthButton.page.update()


monthButton = ft.PopupMenuButton(
                content=ft.Text(
                            value=datetime.now().strftime('%B'), 
                            size=18,
                            weight=ft.FontWeight.W_500,
                            color=ft.colors.PRIMARY),
                items=[
                    ft.PopupMenuItem(text="January", on_click=lambda e: month_change(e)),
                    ft.PopupMenuItem(text="February", on_click=lambda e: month_change(e)),
                    ft.PopupMenuItem(text="March", on_click=lambda e: month_change(e)),
                    ft.PopupMenuItem(text="April", on_click=lambda e: month_change(e)),
                    ft.PopupMenuItem(text="May", on_click=lambda e: month_change(e)),
                    ft.PopupMenuItem(text="June", on_click=lambda e: month_change(e)),
                    ft.PopupMenuItem(text="July", on_click=lambda e: month_change(e)),
                    ft.PopupMenuItem(text="August", on_click=lambda e: month_change(e)),
                    ft.PopupMenuItem(text="September", on_click=lambda e: month_change(e)),
                    ft.PopupMenuItem(text="October", on_click=lambda e: month_change(e)),
                    ft.PopupMenuItem(text="November", on_click=lambda e: month_change(e)),
                    ft.PopupMenuItem(text="December", on_click=lambda e: month_change(e))
                    ]
                )


actDialog = ft.AlertDialog(shape = ft.RoundedRectangleBorder(radius=8))

actYear = date.today().isocalendar().year
weekNumberSelected = date.today().isocalendar().week

yearButton = ft.TextButton(content=ft.Text(str(actYear), size=18))

emptyContainer = ft.Container(width=120, height=60, margin=3)
actContainer = ft.Container(
                margin=3,
                width=120,
                border_radius=5,
                ink=True,
                bgcolor='#24292F',
                shadow = ft.BoxShadow(
                            spread_radius=0.1,
                            blur_radius=2,
                            color=ft.colors.BLACK,
                            offset=ft.Offset(1, 1),
                            blur_style=ft.ShadowBlurStyle.NORMAL)
            )

editMode = False
project = ""
duration = 0
activityDesc = ""


def Show(page: ft.Page):
    global editMode
    editMode = False

    page.clean()
    page.window_width=920
    page.floating_action_button = ft.FloatingActionButton(visible=False)
    page.add(
        ft.Row([
                ft.FilledTonalButton(text="Today", on_click=today_button_click),
                ft.Container(
                    content=ft.Row([
                        ft.IconButton(icon=ft.icons.ARROW_BACK_IOS, on_click=rev_click),
                        monthButton,
                        yearButton,
                        ft.IconButton(icon=ft.icons.ARROW_FORWARD_IOS, on_click=fwd_click)
                    ], )      
                ),
                ft.IconButton(icon=ft.icons.EDIT, icon_color='#C2C7CF', on_click=edit_mode_change)   
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
        week_activities(week_start_date(weekNumberSelected)) 
    )
    page.update()

