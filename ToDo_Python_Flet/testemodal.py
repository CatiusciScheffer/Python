from flet import (
    Page, 
    app, 
    Row, 
    Container, 
    colors, 
    TextField, 
    FloatingActionButton, 
    icons, 
    Tabs, 
    Tab,
    Column,
    Checkbox, 
    MainAxisAlignment,
    alignment,
    IconButton,
    CrossAxisAlignment,
    Text,
    OutlinedButton, 
    Divider,
    ScrollMode,
    TextThemeStyle,
    AlertDialog,
    TextButton,
    ElevatedButton)

def main(page: Page):
    page.title = "AlertDialog examples"

   
    def close_dlg(e):
        dlg_modal.open = False
        page.update()

    dlg_modal = AlertDialog(
        modal=True,
        title=Text("Please confirm"),
        content=Text("Do you really want to delete all those files?"),
        actions=[
            TextButton("Yes", on_click=close_dlg),
            TextButton("No", on_click=close_dlg),
        ],
        actions_alignment=MainAxisAlignment.END,
        on_dismiss=lambda e: print("Modal dialog dismissed!"),
    )

    def open_dlg_modal(e):
        page.dialog = dlg_modal
        dlg_modal.open = True
        page.update()

    page.add(
        ElevatedButton("Open modal dialog", on_click=open_dlg_modal),
    )

app(target=main)