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
    
    
    
    def create_row(e, df):
        ruc = dlg_crud.content.controls[1].value
        razon_social = dlg_crud.content.controls[3].value
        direccion = dlg_crud.content.controls[5].value
        new_row = pd.DataFrame({'ruc': [ruc], 'razon_social': [razon_social], 'direccion': [direccion]})
        new_row.to_sql('factura', con=engine, if_exists='append', index=False)
        df = pd.read_sql('SELECT * FROM factura', con=engine)
        page.update()
        print(f"Registro creado con el RUC {ruc}")


    def update_row(e, df):
        ruc = dlg_crud.content.controls[1].value
        razon_social = dlg_crud.content.controls[3].value
        direccion = dlg_crud.content.controls[5].value
        

        # Buscar el índice del registro existente por RUC
        existing_row_index = df.index[df['ruc'] == ruc].tolist()

        if existing_row_index:
            # Eliminar el registro existente por su índice
            df.drop(index=existing_row_index, inplace=True)

            # Crear un nuevo DataFrame con los datos actualizados
            new_row = pd.DataFrame({'ruc': [ruc], 'razon_social': [razon_social], 'direccion': [direccion]})

            # Concatenar el nuevo registro al DataFrame
            df = pd.concat([df, new_row], ignore_index=True)

            # Guardar el DataFrame actualizado en la base de datos
            df.to_sql('factura', con=engine, if_exists='replace', index=False)
            page.update()
            print(f"Registro actualizado con el RUC {ruc}")
        else:
            # Si no se encuentra el registro, mostrar un mensaje de error o hacer lo que consideres necesario
            print(f"No se encontró un registro con el RUC {ruc}")

    def delete_row(e, df):
        ruc = dlg_crud.content.controls[1].value

        # Buscar el índice del registro existente por RUC
        existing_row_index = df.index[df['ruc'] == ruc].tolist()

        if existing_row_index:
            # Eliminar el registro existente por su índice
            df.drop(index=existing_row_index, inplace=True)

            # Guardar el DataFrame actualizado en la base de datos
            df.to_sql('factura', con=engine, if_exists='replace', index=False)
            page.update()
            print(f"Registro eliminado con el RUC {ruc}")
        else:
            # Si no se encuentra el registro, mostrar un mensaje de error o hacer lo que consideres necesario
            print(f"No se encontró un registro con el RUC {ruc}")

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
            ft.TextButton(text="Crear", on_click= lambda e: create_row(e, df)),
            ft.TextButton(text="Actualizar", on_click= lambda e: update_row(e, df)),
            ft.TextButton(text="Eliminar", on_click= lambda e: delete_row(e, df)),
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