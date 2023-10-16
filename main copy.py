import pandas as pd
import flet as ft
from sqlalchemy import create_engine

# establish connection to MySQL database using SQLAlchemy
engine = create_engine('mysql+mysqlconnector://root:root@localhost/vquijandria')

# create datatable from pandas dataframe
def main(page: ft.Page):

    # read data from MySQL table into pandas dataframe
    df = pd.read_sql('SELECT * FROM factura', con=engine)
    def get_rows():
        rows = []
        for index, row in df.iterrows():
            rows.append(
                ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(row.iloc[1])),
                            ft.DataCell(ft.Text(row.iloc[2])),
                            ft.DataCell(ft.Text(row.iloc[3]), on_tap=open_dlg_crud),
                        ],
            )
            )
        return rows
    
    
    
    def create_row(e):
        ruc = dlg_crud.content.controls[1].value
        razon_social = dlg_crud.content.controls[3].value
        direccion = dlg_crud.content.controls[5].value
        new_row = pd.DataFrame({'ruc': [ruc], 'razon_social': [razon_social], 'direccion': [direccion]})
        new_row.to_sql('factura', con=engine, if_exists='append', index=False)
        df = pd.read_sql('SELECT * FROM factura', con=engine)
        page.update()



    dlg_crud = ft.AlertDialog(
        modal=True,
        title=ft.Text("Crear Registro"),
        content=ft.Column(
            controls=[
                ft.Text("RUC: "),
                ft.TextField(),
                ft.Text("Razon Social: "),
                ft.TextField(),
                ft.Text("Direccion: "),
                ft.TextField(),
            ]
        ),
        actions=[
            ft.TextButton(text="Crear", on_click=create_row),
            ft.TextButton(text="Actualizar"),
        ],
        on_dismiss=lambda: setattr(dlg_crud, "open", False),
    )
    
    def open_dlg_crud(e):
        page.dialog = dlg_crud
        dlg_crud.open = True
        page.update()
        if dlg_crud.open == False:     #No funciona
            page.dialog = None
            page.update()


    page.add(
    ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("RUC"), numeric=True),
            ft.DataColumn(ft.Text("Razon Social")),
            ft.DataColumn(ft.Text("Direccion")),
            ],
        rows=get_rows(),
        )
    )

    page.add(ft.ElevatedButton("CRUD", on_click=open_dlg_crud))


ft.app(target=main)