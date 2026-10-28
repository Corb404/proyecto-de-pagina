from dash import Dash, html, dcc, dash_table


from procesamiento import cargar_datos
from graficos import (grafico_muertes_por_mes, tabla_top10_causas,
                      grafico_sexo_por_departamento, grafico_edades,
                      grafico_ciudades_violentas, grafico_menor_mortalidad,
                      grafico_mapa)
# 1. Cargar los datos UNA sola vez, al arrancar
df = cargar_datos()
top10 = tabla_top10_causas(df)
# 2. Crear la app
app = Dash(__name__)
server = app.server   # Render lo necesitará

app.layout = html.Div(style={"fontFamily": "Arial", "padding": "20px"}, children=[
    html.H1("Mortalidad en Colombia, 2019"),
    html.P("Análisis de las defunciones no fetales registradas por el DANE."),

    dcc.Tabs([
        dcc.Tab(label="Mapa por departamento", children=[
            dcc.Graph(figure=grafico_mapa(df), style={"height": "700px"}),
        ]),
        dcc.Tab(label="Muertes por mes", children=[
            dcc.Graph(figure=grafico_muertes_por_mes(df)),
        ]),
        dcc.Tab(label="Ciudades más violentas", children=[
            dcc.Graph(figure=grafico_ciudades_violentas(df)),
        ]),
        dcc.Tab(label="Menor mortalidad", children=[
            dcc.Graph(figure=grafico_menor_mortalidad(df)),
        ]),
        dcc.Tab(label="Principales causas", children=[
            html.H3("10 principales causas de muerte"),
            dash_table.DataTable(
                data=top10.to_dict("records"),
                columns=[{"name": "Código", "id": "COD_MUERTE"},
                         {"name": "Causa", "id": "CAUSA"},
                         {"name": "Total", "id": "TOTAL"}],
                style_cell={"textAlign": "left", "whiteSpace": "normal"},
                style_header={"fontWeight": "bold"},
            ),
        ]),
        dcc.Tab(label="Sexo por departamento", children=[
            dcc.Graph(figure=grafico_sexo_por_departamento(df), style={"height": "600px"}),
        ]),
        dcc.Tab(label="Grupos de edad", children=[
            dcc.Graph(figure=grafico_edades(df)),
        ]),
    ]),
])
if __name__ == "__main__":
    app.run(debug=True)