import streamlit as st
from Introducción import configuraciones
import pandas as pd
import io
import plotly.express as px

#! Código de Colores

#<h1> #ef476f
#<h2> #ffd166
#<h3> #06d6a0
#<h4> #118ab2
#<h5> #118ab2

configuraciones("AED", "📝")





st.html('''<h1><font color="#ef476f">Exploración y Limpieza de Datos</font></h1>''')
st.divider()

st.html('''<h2><font color="ffd166">1. Carga de Datos</font></h2>''')
df=pd.read_csv('Data/Online-Retail.csv',sep=';')
df['UnitPrice'] = df['UnitPrice'].str.replace(',', '.').astype(float)
df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
df['Country'] = df['Country'].str.replace('EIRE','Ireland')

with st.expander('Dataset'):
    st.code('''df=pd.read_csv('Data/Online-Retail.csv',sep=';')
df['UnitPrice'] = df['UnitPrice'].str.replace(',', '.').astype(float)
df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
df['Country'] = df['Country'].str.replace('EIRE','Ireland')''')
    st.dataframe(df,height=500)

st.divider()

st.html('''<h2><font color="ffd166">2. Primeras Observaciones</font></h2>''')
st.html('''<h3><font color="06d6a0">2.1. Tamaño del Dataset</font></h3>''')
with st.expander('df.shape'):
    st.text(f"""El dataset está compuesto por:
    • {df.shape[0]} registros
    • {df.shape[1]} atributos""")


atributos_info =[
    ['InvoiceNo','Identificador único de la factura'],
    ['StockCode','Código del producto'],
    ['Description','Descripción del producto'],
    ['Quantity','Cantidad de productos'],
    ['InvoiceDate','Fecha de la factura'],
    ['UnitPrice','Precio unitario del producto'],
    ['CustomerID','Código del cliente'],
    ['Country','Nombre del país']
]

atributos_df = pd.DataFrame(
    atributos_info,
    columns=['Atributo','Descripción']
    )

st.html('''<h3><font color="06d6a0">2.2. Objetivos de los Atributos</font></h3>''')
with st.expander('Atributos'):
    st.dataframe(atributos_df)


st.html('''<h3><font color="06d6a0">2.3. Tipos de Datos</font></h3>''')
with st.expander('df.info()'):
    buffer = io.StringIO()
    df.info(buf=buffer)
    s = buffer.getvalue()
    st.text(s)

st.html('''<h3><font color="06d6a0">2.4. Estadística Preliminar</font></h3>''')
with st.expander('Estadística'):
    st.code('''df.describe().round(2)''')
    st.dataframe(df.describe().round(2))


st.html('''<h3><font color="06d6a0">2.5. Detección de Valores Nulos</font></h3>''')
customerid_nulos = df[df['CustomerID'].isnull()]
with st.expander('Valores Nulos'):
    st.code('''customerid_nulos = df[df['CustomerID'].isnull()]
customerid_nulos''')
    st.dataframe(customerid_nulos)

st.html('''<h3><font color="06d6a0">2.6. Agregamos columna de total</font></h3>''')
with st.expander('DataFrame con Totales'):
    st.code('''df['Total'] = df['Quantity'] * df['UnitPrice']
df''')
    df['Total'] = df['Quantity'] * df['UnitPrice']
    st.dataframe(df)

st.divider()

st.html('''<h2><font color="ffd166">3. Limpieza del DataFrame</font></h2>''')

st.html('''<h3><font color="06d6a0">3.1. Eliminamos los registros con CustomerID nulos</font></h3>''')
with st.expander('Limpieza de Nulos'):
    st.code('''df_limpio = df[~df.index.isin(customerid_nulos.index)]
df_limpio''')
    df_limpio = df[~df.index.isin(customerid_nulos.index)]
    st.dataframe(df_limpio)

st.html('''<h3><font color="06d6a0">3.2. Detección de ventas que tuvieron devoluciones</font></h3>''')
st.write('Creamos una columna "CamposAgrupados" para concatenar StockCode, CustomerID y Price y de esa columna detectamos duplicados. Sumamos cada duplicado y si da cero borramos esos registros.')
with st.expander('Identificación de Devoluciones'):
    st.code('''df_limpio['CamposAgrupados'] = df_limpio['StockCode'].astype(str) + '-' + df_limpio['CustomerID'].astype(str) + '-' + df_limpio['UnitPrice'].astype(str)

grupos_a_eliminar = df_limpio.groupby('CamposAgrupados')['Quantity'].sum().reset_index()
grupos_a_eliminar = grupos_a_eliminar[grupos_a_eliminar['Quantity'] == 0]['CamposAgrupados']

registros_a_borrar = df_limpio[df_limpio['CamposAgrupados'].isin(grupos_a_eliminar) & (df_limpio['Quantity'] != 0)]
registros_a_borrar= registros_a_borrar.sort_values(by='CustomerID')

registros_a_borrar['Tipo'] = registros_a_borrar['Quantity'].apply(lambda x: 'Compra' if x > 0 else 'Devolución')

total_devoluciones = registros_a_borrar[registros_a_borrar['Tipo'] == 'Devolución']['Total'].sum()

total_compras = registros_a_borrar[registros_a_borrar['Tipo'] == 'Compra']['Total'].sum()

pd.dataframe({
            'Total de devoluciones': [total_devoluciones.round(0)],
            'Total de compras': [total_compras.round(0)]
            })
pd''')
            
    df_limpio['CamposAgrupados'] = df_limpio['StockCode'].astype(str) + '-' + df_limpio['CustomerID'].astype(str) + '-' + df_limpio['UnitPrice'].astype(str)

    grupos_a_eliminar = df_limpio.groupby('CamposAgrupados')['Quantity'].sum().reset_index()
    grupos_a_eliminar = grupos_a_eliminar[grupos_a_eliminar['Quantity'] == 0]['CamposAgrupados']

    registros_a_borrar = df_limpio[df_limpio['CamposAgrupados'].isin(grupos_a_eliminar) & (df_limpio['Quantity'] != 0)]
    registros_a_borrar= registros_a_borrar.sort_values(by='CustomerID')

    registros_a_borrar['Tipo'] = registros_a_borrar['Quantity'].apply(lambda x: 'Compra' if x > 0 else 'Devolución')

    total_devoluciones = registros_a_borrar[registros_a_borrar['Tipo'] == 'Devolución']['Total'].sum()

    total_compras = registros_a_borrar[registros_a_borrar['Tipo'] == 'Compra']['Total'].sum()

    st.dataframe({'Total de devoluciones': [total_devoluciones.round(0)], 'Total de compras': [total_compras.round(0)]})


st.html('''<h3><font color="06d6a0">3.3. Eliminación de registros identificados como compra y devolución</font></h3>''')

df_limpio2 = df_limpio[~df_limpio['CamposAgrupados'].isin(grupos_a_eliminar)]
df_limpio2 = df_limpio2.drop(columns=['CamposAgrupados'])

with st.expander('Eliminación de Devoluciones'):
    st.code('''df_limpio2 = df_limpio[~df_limpio['CamposAgrupados'].isin(grupos_a_eliminar)]
df_limpio2 = df_limpio2.drop(columns=['CamposAgrupados'])
df_limpio2''')
    st.dataframe(df_limpio2)


st.html('''<h3><font color="06d6a0">3.4. Detección y eliminación de ventas anuladas por totales y duplicados</font></h3>''')

df_limpio2['Total_abs'] = df_limpio2['Total'].abs()

pares_devoluciones = df_limpio2.merge(
    df_limpio2,
    on=['CustomerID', 'Total_abs'],
    suffixes=('_1', '_2')
)

pares_devoluciones = pares_devoluciones[
    (pares_devoluciones['Total_1'] + pares_devoluciones['Total_2'] == 0) &
    (pares_devoluciones['InvoiceNo_1'] != pares_devoluciones['InvoiceNo_2'])
]

pares_devoluciones = pares_devoluciones[[
    'CustomerID', 'InvoiceNo_1', 'StockCode_1', 'Quantity_1', 'Total_1','InvoiceDate_1',
    'InvoiceNo_2', 'StockCode_2', 'Quantity_2', 'Total_2','InvoiceDate_2'
]].drop_duplicates()

indices_a_eliminar = pares_devoluciones[['InvoiceNo_1', 'InvoiceNo_2']].stack().unique()

df_sin_pares_devoluciones = df_limpio2[~df_limpio2['InvoiceNo'].isin(indices_a_eliminar)].reset_index(drop=True)

df_limpio3 = df_sin_pares_devoluciones.drop(columns=['Total_abs'])
df_limpio3 = df_limpio3[df_limpio3['Quantity'] > 0].reset_index(drop=True)

with st.expander('Eliminación de Devoluciones'):
    st.code('''df_limpio2['Total_abs'] = df_limpio2['Total'].abs()

pares_devoluciones = df_limpio2.merge(
    df_limpio2,
    on=['CustomerID', 'Total_abs'],
    suffixes=('_1', '_2')
)

pares_devoluciones = pares_devoluciones[
    (pares_devoluciones['Total_1'] + pares_devoluciones['Total_2'] == 0) &
    (pares_devoluciones['InvoiceNo_1'] != pares_devoluciones['InvoiceNo_2'])
]

pares_devoluciones = pares_devoluciones[[
    'CustomerID', 'InvoiceNo_1', 'StockCode_1', 'Quantity_1', 'Total_1','InvoiceDate_1',
    'InvoiceNo_2', 'StockCode_2', 'Quantity_2', 'Total_2','InvoiceDate_2'
]].drop_duplicates()

indices_a_eliminar = pares_devoluciones[['InvoiceNo_1', 'InvoiceNo_2']].stack().unique()

df_sin_pares_devoluciones = df_limpio2[~df_limpio2['InvoiceNo'].isin(indices_a_eliminar)].reset_index(drop=True)

df_limpio3 = df_sin_pares_devoluciones.drop(columns=['Total_abs'])
df_limpio3 = df_limpio3[df_limpio3['Quantity'] > 0].reset_index(drop=True)
df_limpio3''')
    st.dataframe(df_limpio3)


st.html('''<h3><font color="06d6a0">3.5. Agregado de columnas <code><font color="06d6a0">Year</font></code> y <code><font color="06d6a0">Month</font></code></font></h3>''')

df_limpio3['Year'] = df_limpio3['InvoiceDate'].dt.year
df_limpio3['Month'] = df_limpio3['InvoiceDate'].dt.month

with st.expander('Agregado de Columnas'):
    st.code('''df_limpio3['Year'] = df_limpio3['InvoiceDate'].dt.year
df_limpio3['Month'] = df_limpio3['InvoiceDate'].dt.month
df_limpio3''')
    st.dataframe(df_limpio3)

st.divider()

st.html('''<h2><font color="ffd166">4. Estadística Descriptiva del DataFrame Limpio</font></h2>''')

with st.expander('Estadística Descriptiva'):
    st.code('''df_limpio3.describe().round(2)''')
    st.dataframe(df_limpio3.describe().round(2))


st.html('''<h3><font color="06d6a0">4.1. Validamos los tipos de datos</font></h3>''')

with st.expander('df_limpio3.info()'):
    buffer1 = io.StringIO()
    df_limpio3.info(buf=buffer1)
    s1 = buffer1.getvalue()
    st.text(s1)