import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler as scaler 

samsung_df = pd.read_json("data.json",dtype=False)
all_df = pd.read_json("data2.json",dtype=False)

#print(type(samsung_df["PuntajeAntutu"][0]))
#print(all_df.head())
#input()

def clean_numeric_row(parameter, unit):
    '''
    Function to clean numeric rows meant to use with pandas df.apply function
    name = string, name of the columns that needs to be converted to a number
    unit = string, units of the column (e.g. Gb, mAh, GHz...)
    '''
    if type(parameter) == str:
        try:
            parameter = parameter.replace(unit,"").replace(".","").strip()
            return int(parameter)
        except:
            return None
    elif parameter is not None:
        return parameter
    else:
        return None
    
def get_resolution(resolution):
    if resolution is None:
        return None
    resolution = resolution.lower()
    if "3088" in resolution or "quad hd+" in resolution:
        return 3088
    if "1080" in resolution or "fhd+" in resolution or "(fhd)+" in resolution:
        return 1080
    if "720" in resolution or "hd+" in resolution:
        return 720
    return 480

def get_watter_resistance(watter_resistance):
    if watter_resistance is None:
        return None
    if "Resistente al Agua y el Polvo" in watter_resistance:
        return 1
    if "Resistente a Salpicaduras" in watter_resistance:
        return 0.5
    return 0

def clean_scale_numeric_columns (df,columns,units):
    for column,unit in list(zip(columns,units)):
        df[column]=df.apply(lambda row: clean_numeric_row(row[column],unit),axis=1)
        df["{}_S".format(column)]=scaler(feature_range=(0.1,1)).fit_transform(np.array(df[column]).reshape(1,-1).transpose())
    return df

def score(row):
    ans = row["Bateria_S"]+row["CamaraFrontal_S"]+row["CamaraPosterior_S"]*0.5+row["Garantia_S"]
    ans = ans + row["MemoriaInterna_S"] + row["RAM_S"]*2 
    return ans/6.5

def price_quality(row):
    try:
        ans = row["Score"]/row["Price_S"]
    except:
        ans = None
    return ans

def clean_df(df):
    df = df.fillna("None")
    df = df.replace([""," ","None"],[None,None,None])    
    numeric_columns = ["Bateria","CamaraFrontal","CamaraPosterior","Garantia",
                       "MemoriaInterna","RAM","Price","PuntajeAntutu","PuntajeK"]
    units = ["mAh","Mpx","Mpx","Meses","GB","GB","$","",""]
    df = clean_scale_numeric_columns(df, numeric_columns,units)    
    df["ResistenciaAgua"] = df.apply(lambda row:get_watter_resistance(row["ResistenciaAgua"]),axis=1)
    df["Resolucion"] = df.apply(lambda row:get_resolution(row["Resolucion"]),axis=1)
    df["Resolucion_S"] = scaler(feature_range=(0.1,1)).fit_transform(np.array(df["Resolucion"]).reshape(1,-1).transpose())
    df["Score"] = df.apply(score,axis=1)
    df["CalidadPrecio"]=df.apply(price_quality,axis=1)
    
    return df

def report(df,title):
    print("-"*50)
    print("Analisis de {}".format(title))
    print("-"*50)
    df = df.sort_values(by="Score",ascending=False, ignore_index=True)
    print("El celular con mayor puntaje estimado({:.2f}) es {}\ncon un precio de ${} COP".format(df["Score"][0],df["Name"][0],df["Price"][0]))
    df = df.sort_values(by="CalidadPrecio",ascending=False,ignore_index=True)
    top_5 = df[["Name","Price","CalidadPrecio"]][:5]
    print("Los 5 celulares con mejor relacion calidad precio estimada son:")
    print(top_5)
    df = df.sort_values(by="PuntajeAntutu",ascending=False,ignore_index=True)
    print("El celular con mayor puntaje de Antutu Benchmark({}) (aka. mayor rendimiento) es {}".format(df["PuntajeAntutu"][0],df["NombreAntutu"][0]))
    print("con un precio de: {}".format(df["Price"][0]))
    df = df.sort_values(by="PuntajeK",ascending=False,ignore_index=True)
    #print("El celular con la mejor relacion calidad precio({}) (segun kimovil)\nes: {}".format(df["PuntajeK"][0],df["NombreAntutu"][0]))
    top_5 = df[["NombreAntutu","Price","PuntajeK"]][:5]
    print("Los 5 celulares con mejor relacion calidad precio segun kiwimovil son:")
    print(top_5)

samsung_df = clean_df(samsung_df)
all_df = clean_df(all_df)

#print(samsung_df["Score"])

report(samsung_df, "Celulares Samsung")
report(all_df, "Todos los celulares")



