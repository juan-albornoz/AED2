import streamlit as st
from Introducción import configuraciones
import pandas as pd
import io
import plotly.express as px

#! Colores
# Amarillo: "Yellow"
# Cyan: "#00ffbf"
# Rosa: "#e600e6"

#<h1> #BFECFF
#<h2> #CDC1FF
#<h3> #FFF6E3
#<h4> #FFCCEA

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
#df['CustomerID'] = df['CustomerID'].astype(str)
#df['CustomerID'] = df['CustomerID'].str.replace('.0','')
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

#
#st.html('''<h2><font color="ffd166">5. Análisis de ventas por mes, país y días</font></h2>''')
#
#st.html('''<h3><font color="06d6a0">5.1. Visualización de ventas por mes</font></h3>''')
#
#
#import plotly.io as pio
#pio.templates.default = "plotly"
#pio.templates["plotly"].layout.colorway = px.colors.qualitative.Vivid
#pio.templates["plotly"].layout.xaxis.tickangle = -90
#
#
## Agrupamiento de datos
#df_ventas_por_año = df_limpio3.groupby(['Year', 'Month'])['Total'].sum().reset_index()
#df_ventas_por_año['Total'] = df_ventas_por_año['Total'].astype(int)
#df_ventas_por_año['Año y mes'] = df_ventas_por_año['Year'].astype(str) + '-' + df_ventas_por_año['Month'].astype(str)
#
#df_limpio3_sinUK = df_limpio3[df_limpio3['Country'] != 'United Kingdom']
#df_ventas_por_año_sinUK = df_limpio3_sinUK.groupby(['Year', 'Month'])['Total'].sum().reset_index()
#df_ventas_por_año_sinUK['Total'] = df_ventas_por_año_sinUK['Total'].astype(int)
#df_ventas_por_año_sinUK['Año y mes'] = df_ventas_por_año_sinUK['Year'].astype(str) + '-' + df_ventas_por_año_sinUK['Month'].astype(str)
#
#max_total_all = df_ventas_por_año['Total'].max()
#max_total_sinUK = df_ventas_por_año_sinUK['Total'].max()
#
#colors_all = ['Otras Ventas' if total != max_total_all else 'Venta Máxima' for total in df_ventas_por_año['Total']]
#colors_sinUK = ['Otras Ventas' if total != max_total_sinUK else 'Venta Máxima' for total in df_ventas_por_año_sinUK['Total']]
#
#fig1 = px.bar(df_ventas_por_año, x='Año y mes', y='Total', color=colors_all, title='Ventas por mes (con todos los países)')
#fig1.update_layout(xaxis_title='Mes-Año', yaxis_title='Total')
#
#fig2 = px.bar(df_ventas_por_año_sinUK, x='Año y mes', y='Total', color=colors_sinUK, title='Ventas por mes (sin United Kingdom)')
#fig2.update_layout(xaxis_title='Mes-Año', yaxis_title='Total', yaxis_range=[0, max_total_sinUK * 1.1])
#
#
#st.write('''Visualizamos en un gráfico de barras las ventas (Total) por mes de diciembre 2010 a diciembre 2011 con todos los países y en otro lo mismo otro sin Uk.
#
#La ausencia del Reino Unido hace que las cifras sean considerablemente más bajas en el segundo gráfico, lo que indica que el Reino Unido es un mercado dominante en el total de ventas. Además, la tendencia general en ambos gráficos es similar, pero el impacto del Reino Unido es claramente significativo en el total general, especialmente en los picos de ventas en ciertos meses del año.''')
#
#with st.expander('Código'):
#    st.code('''import plotly.express as px
#import plotly.io as pio
#
## Configuración global de parámetros
#pio.templates.default = "plotly"
#pio.templates["plotly"].layout.colorway = px.colors.qualitative.Vivid
#pio.templates["plotly"].layout.xaxis.tickangle = -90
#
#df_ventas_por_año = df_limpio3.groupby(['Year', 'Month'])['Total'].sum().reset_index()
#df_ventas_por_año['Total'] = df_ventas_por_año['Total'].astype(int)
#df_ventas_por_año['Año y mes'] = df_ventas_por_año['Year'].astype(str) + '-' + df_ventas_por_año['Month'].astype(str)
#
#df_limpio3_sinUK = df_limpio3[df_limpio3['Country'] != 'United Kingdom']
#df_ventas_por_año_sinUK = df_limpio3_sinUK.groupby(['Year', 'Month'])['Total'].sum().reset_index()
#df_ventas_por_año_sinUK['Total'] = df_ventas_por_año_sinUK['Total'].astype(int)
#df_ventas_por_año_sinUK['Año y mes'] = df_ventas_por_año_sinUK['Year'].astype(str) + '-' + df_ventas_por_año_sinUK['Month'].astype(str)
#
#max_total_all = df_ventas_por_año['Total'].max()
#max_total_sinUK = df_ventas_por_año_sinUK['Total'].max()
#
#colors_all = ['Otras Ventas' if total != max_total_all else 'Venta Máxima' for total in df_ventas_por_año['Total']]
#colors_sinUK = ['Otras Ventas' if total != max_total_sinUK else 'Venta Máxima' for total in df_ventas_por_año_sinUK['Total']]
#
#fig1 = px.bar(df_ventas_por_año, x='Año y mes', y='Total', color=colors_all, title='Ventas por mes (con todos los países)')
#fig1.update_layout(xaxis_title='Mes-Año', yaxis_title='Total')
#
#fig2 = px.bar(df_ventas_por_año_sinUK, x='Año y mes', y='Total', color=colors_sinUK, title='Ventas por mes (sin United Kingdom)')
#fig2.update_layout(xaxis_title='Mes-Año', yaxis_title='Total', yaxis_range=[0, max_total_sinUK * 1.1])''')
#
## Selector para ver ventas con y sin UK
#with st.expander('Visualización de Ventas por Mes'):
#    opcion = st.selectbox('Seleccionar vista de ventas:', ['Con UK', 'Sin UK'], index=0)
#
#    if opcion == 'Con UK':
#        st.plotly_chart(fig1)
#    else:
#        st.plotly_chart(fig2)
#
#
#
#st.html('''<h3><font color="06d6a0">5.2. Top 5 de Ventas por país</font></h3>''')
#st.html('''<h4><font color="118ab2">5.2.1. Tratamiento de los datos</font></h4>''')
#
#st.write('Agrupamos y sumamos los totales por país, ordenamos de forma descendente y visualizamos los primeros')
#
#top_venta_pais = df_limpio3.groupby(['Country'])['Total'].sum().reset_index()
#top_venta_pais = top_venta_pais.sort_values(by='Total', ascending=False)
#
#with st.expander('Top 5 de Ventas por país'):
#    st.code('''top_venta_pais = df_limpio3.groupby(['Country'])['Total'].sum().reset_index()
#top_venta_pais = top_venta_pais.sort_values(by='Total', ascending=False)
#top_venta_pais.head(5).round(2)''')
#    st.dataframe(top_venta_pais.head(5).round(2))
#
#
#st.html('''<h4><font color="118ab2">5.2.2. DataFrame Top 5 Año: País, Total y Año-Mes</font></h4>''')
#
#paises_top5 = ['United Kingdom', 'France', 'Germany', 'Netherlands', 'Ireland']
#
#df_top5_ventas_por_mes = df_limpio3[df_limpio3['Country'].isin(paises_top5)]
#
#df_top5_columnas = df_top5_ventas_por_mes.groupby(['Year', 'Month', 'Country'])['Total'].sum().reset_index()
#df_top5_columnas['Total'] = df_top5_columnas['Total'].astype(int)
#df_top5_columnas['Año y mes'] = (df_top5_columnas['Year'].astype(str) + '-' + df_top5_columnas['Month'].astype(str))
#df_top5_columnas = df_top5_columnas.drop(columns=['Year','Month'])
#
#
#with st.expander('DataFrame Top 5 Año'):
#    st.code('''paises_top5 = ['United Kingdom', 'France', 'Germany', 'Netherlands', 'EIRE']
#
#df_top5_ventas_por_mes = df_limpio3[df_limpio3['Country'].isin(paises_top5)]
#
#df_top5_columnas = df_top5_ventas_por_mes.groupby(['Year', 'Month', 'Country'])['Total'].sum().reset_index()
#df_top5_columnas['Total'] = df_top5_columnas['Total'].astype(int)
#df_top5_columnas['Año y mes'] = (df_top5_columnas['Year'].astype(str) + '-' + df_top5_columnas['Month'].astype(str))
#df_top5_columnas = df_top5_columnas.drop(columns=['Year','Month'])
#df_top5_columnas''')
#    st.dataframe(df_top5_columnas)
#
#
#st.html('''<h4><font color="118ab2">5.2.3 Gráfico de líneas: top 5 países - venta por mes</font></h4>''')
#
## Crear gráficos de líneas con Plotly
#fig3 = px.line(df_top5_columnas, x='Año y mes', y='Total', color='Country', markers=True, title='Total por mes-año para cada país')
#fig3.update_layout(xaxis_title='Mes-Año', yaxis_title='Total')
#
#df_top_sinUK = df_top5_columnas[df_top5_columnas['Country'] != 'United Kingdom']
#fig4 = px.line(df_top_sinUK, x='Año y mes', y='Total', color='Country', markers=True, title='Total por mes-año sin United Kingdom')
#fig4.update_layout(xaxis_title='Mes-Año', yaxis_title='Total')
#
#with st.expander('Código'):
#    st.code('''fig3 = px.line(df_top5_columnas, x='Año y mes', y='Total', color='Country', markers=True, title='Total por mes-año para cada país')
#fig3.update_layout(xaxis_title='Mes-Año', yaxis_title='Total')
#
#df_top_sinUK = df_top5_columnas[df_top5_columnas['Country'] != 'United Kingdom']
#fig4 = px.line(df_top_sinUK, x='Año y mes', y='Total', color='Country', markers=True, title='Total por mes-año sin United Kingdom')
#fig4.update_layout(xaxis_title='Mes-Año', yaxis_title='Total')''')
#
## Selector para ver evolución de ventas con y sin UK
#with st.expander('Visualización de Evolución de Ventas'):
#    opcion_evolucion = st.selectbox('Seleccionar vista de evolución de ventas:', ['Con UK', 'Sin UK'], index=0)
#
#    if opcion_evolucion == 'Con UK':
#        st.plotly_chart(fig3)
#        st.write('''- UK tiene un volumen de ventas significativamente mayor que los otros países (Irlanda, Francia, Alemania y Países Bajos) en todos los períodos del año. Esto hace que las fluctuaciones de los demás países sean difíciles de distinguir en la escala general.
#
#- UK muestra picos de ventas particularmente altos alrededor de septiembre y octubre de 2011.''')
#    else:
#        st.plotly_chart(fig4)
#        st.write('''- **Variabilidad de ventas:** cada país muestra fluctuaciones a lo largo del año, esto indica una demanda inestable.
#
#- **Picos de ventas:** Francia y los Países Bajos registran picos en noviembre. Alemania alcanza su punto máximo en mayo, mientras que Irlanda tiene ventas más constantes con un pico en febrero.''')
#    st.write('''**Con estos datos podemos sugerir realizar promociones específicas en los meses con menor demanda. También, estrategias promocionales enfocadas en los picos de ventas para aumentar los ticket promedio**''')
#
#
#
#
#
#
#
#
#
#
#
## Ventas por mes con todos los países
##ventas_por_mes = df_limpio3.groupby(['Year', 'Month'])['Total'].sum().reset_index()
##fig1 = px.bar(ventas_por_mes, x='Month', y='Total', color='Year', title='Ventas por Mes (Todos los Países)')
##st.plotly_chart(fig1)
#
## Ventas por mes sin UK
##ventas_por_mes_sin_uk = df_limpio3[df_limpio3['Country'] != 'United Kingdom'].groupby(['Year', 'Month'])['Total'].sum().reset_index()
##fig2 = px.bar(ventas_por_mes_sin_uk, x='Month', y='Total', color='Year', title='Ventas por Mes (Sin UK)')
##st.plotly_chart(fig2)
#
#
#
#
#
#
#
#





















#df['Total'] = df['Quantity'] * df['UnitPrice']
#df_top5 = df.groupby('Country')['Total'].sum().nlargest(5).reset_index()
#st.write('Top 5 países por ventas totales:')
#st.dataframe(df_top5)
#fig=px.bar(df_top5,x='Country',y='Total',title='Ventas por País')
#st.plotly_chart(fig)