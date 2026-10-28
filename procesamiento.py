import pandas as pd

def cargar_datos():
    df = pd.read_csv("data/NoFetal2019.csv")

    # Divipola: nombres de departamento y municipio
    divipola = pd.read_excel("data/Divipola.xlsx")
    divi = divipola[["COD_DANE", "DEPARTAMENTO", "MUNICIPIO"]]
    df = df.merge(divi, on="COD_DANE", how="left")

    # Códigos de muerte: nombre de la causa
    codigos = pd.read_excel("data/CodigosDeMuerte.xlsx", header=8)
    codigos.columns = ["CAPITULO", "NOMBRE_CAPITULO", "COD_3", "CAUSA_3", "COD_MUERTE", "CAUSA"]
    cod = codigos[["COD_MUERTE", "CAUSA"]]
    df = df.merge(cod, on="COD_MUERTE", how="left")
    causas_3 = codigos.drop_duplicates("COD_3").set_index("COD_3")["CAUSA_3"]
    df["CAUSA"] = df["CAUSA"].fillna(df["COD_MUERTE"].map(causas_3))
    return df


if __name__ == "__main__":
    df = cargar_datos()
    print(df.shape)
    print("Sin causa:", df["CAUSA"].isna().sum())