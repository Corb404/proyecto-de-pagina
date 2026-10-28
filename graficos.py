import pandas as pd
import plotly.express as px
import json

def grafico_muertes_por_mes(df):
    # 1. Agrupar: contar cuántas muertes hay en cada mes
    por_mes = df.groupby("MES").size().reset_index(name="TOTAL")
    nombres_meses = {1: "Ene", 2: "Feb", 3: "Mar", 4: "Abr", 5: "May", 6: "Jun", 7:"Jul", 
                     8:"Agto",9:"Sept",10:"Oct",11:"Nov",12:"Dic"}   
    por_mes["NOMBRE_MES"] = por_mes["MES"].map(nombres_meses)
    # 2. Graficar
    fig = px.line(por_mes, x="NOMBRE_MES", y="TOTAL", markers=True,
                  title="Total de muertes por mes en Colombia, 2019",
                  labels={"NOMBRE_MES": "Mes", "TOTAL": "Número de muertes"})
    return fig

def tabla_top10_causas(df):
    top10 = (df.groupby(["COD_MUERTE", "CAUSA"])   # código y nombre de la causa
               .size()
               .reset_index(name="TOTAL")
               .sort_values("TOTAL", ascending=False)   # de mayor a menor
               .head(10))
    return top10

def grafico_sexo_por_departamento(df):
    # 1. Traducir los códigos de sexo
    nombres_sexo = {1: "Hombre", 2: "Mujer", 3: "Indeterminado"}
    df = df.copy()
    df["SEXO_NOMBRE"] = df["SEXO"].map(nombres_sexo)

    por_depto = df.groupby(["DEPARTAMENTO", "SEXO_NOMBRE"]).size().reset_index(name="TOTAL")

    # 3. Graficar barras apiladas
    fig = px.bar(por_depto, x="DEPARTAMENTO", y="TOTAL", color="SEXO_NOMBRE",
                 barmode="stack",
                 title="Muertes por sexo en cada departamento, 2019",
                 labels={"TOTAL": "Número de muertes", "SEXO_NOMBRE": "Sexo"})
    fig.update_xaxes(categoryorder="total descending")
    return fig
def grafico_edades(df):
    bordes = [-1, 4, 6, 8, 10, 11, 13, 16, 19, 24, 28, 29]
    categorias = ["Neonatal", "Infantil", "Primera infancia", "Niñez",
                  "Adolescencia", "Juventud", "Adultez temprana",
                  "Adultez intermedia", "Vejez", "Longevidad", "Desconocida"]

    df = df.copy()
    df["CATEGORIA_EDAD"] = pd.cut(df["GRUPO_EDAD1"], bins=bordes, labels=categorias)

    fig = px.histogram(df, x="CATEGORIA_EDAD",
                       category_orders={"CATEGORIA_EDAD": categorias},
                       title="Distribución de muertes por ciclo de vida, 2019",
                       labels={"CATEGORIA_EDAD": "Grupo de edad"})
    fig.update_yaxes(title="Número de muertes")
    return fig
def grafico_ciudades_violentas(df):
    # 1. Filtrar: solo homicidios con arma de fuego
    homicidios = df[df["COD_MUERTE"].str.startswith("X95")]

    # 2. Agrupar por ciudad y quedarse con las 5 mayores
    top5 = (homicidios.groupby(["DEPARTAMENTO", "MUNICIPIO"])
                      .size()
                      .reset_index(name="TOTAL")
                      .nlargest(5, "TOTAL"))

    # 3. Graficar
    fig = px.bar(top5, x="MUNICIPIO", y="TOTAL",
                 hover_data=["DEPARTAMENTO"],
                 title="5 ciudades con más homicidios por arma de fuego (X95), 2019",
                 labels={"MUNICIPIO": "Ciudad", "TOTAL": "Homicidios"})
    return fig

def grafico_menor_mortalidad(df):
    por_ciudad = (df.groupby(["DEPARTAMENTO", "MUNICIPIO"])
                    .size()
                    .reset_index(name="TOTAL"))
    minimo = por_ciudad["TOTAL"].min()
    empatados = (por_ciudad["TOTAL"] == minimo).sum()
    print(f"Mínimo: {minimo} muertes. Municipios empatados: {empatados}")

    menores = por_ciudad.nsmallest(10, "TOTAL")
    print(menores)   # ← temporal

    menores["CIUDAD"] = menores["MUNICIPIO"] + " (" + menores["DEPARTAMENTO"] + ")"

    fig = px.pie(menores, names="CIUDAD", values="TOTAL",
                 title="10 municipios con menor número de muertes, 2019")
    return fig

def grafico_mapa(df):
    with open("data/colombia_departamentos.geojson", encoding="utf-8") as f:
        geo = json.load(f)

    por_depto = (df.groupby(["COD_DEPARTAMENTO", "DEPARTAMENTO"])
                   .size()
                   .reset_index(name="TOTAL"))
    por_depto["DPTO"] = por_depto["COD_DEPARTAMENTO"].astype(str).str.zfill(2)

    fig = px.choropleth(por_depto,
                        geojson=geo,
                        locations="DPTO",                
                        featureidkey="properties.DPTO",  
                        color="TOTAL",
                        hover_name="DEPARTAMENTO",
                        color_continuous_scale="Reds",
                        title="Total de muertes por departamento, 2019")
    fig.update_geos(fitbounds="locations", visible=False)
    return fig

if __name__ == "__main__":
    from procesamiento import cargar_datos
    df = cargar_datos()
    fig = grafico_muertes_por_mes(df)
    fig.show()
    print(tabla_top10_causas(df))
    fig = grafico_sexo_por_departamento(df)
    fig.show()
    fig = grafico_edades(df)
    fig.show()
    fig = grafico_ciudades_violentas(df)
    fig.show()
    fig = grafico_menor_mortalidad(df)
    fig.show()
    fig = grafico_mapa(df)
    fig.show()
