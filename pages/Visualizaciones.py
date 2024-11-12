import streamlit as st
from Introducción import configuraciones
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from pages.AED import df_limpio3

configuraciones("Visualizaciones", "📊")

st.html('''<h1><font color="#ef476f">Visualizaciones</font></h1>''')
st.divider()


st.html('''<h2><font color="ffd166">5. Análisis de ventas por mes, país y días</font></h2>''')

st.html('''<h3><font color="06d6a0">5.1. Visualización de ventas por mes</font></h3>''')


import plotly.io as pio
pio.templates.default = "plotly"
pio.templates["plotly"].layout.colorway = px.colors.qualitative.Vivid
pio.templates["plotly"].layout.xaxis.tickangle = -90


# Agrupamiento de datos
df_ventas_por_año = df_limpio3.groupby(['Year', 'Month'])['Total'].sum().reset_index()
df_ventas_por_año['Total'] = df_ventas_por_año['Total'].astype(int)
df_ventas_por_año['Año y mes'] = df_ventas_por_año['Year'].astype(str) + '-' + df_ventas_por_año['Month'].astype(str)

df_limpio3_sinUK = df_limpio3[df_limpio3['Country'] != 'United Kingdom']
df_ventas_por_año_sinUK = df_limpio3_sinUK.groupby(['Year', 'Month'])['Total'].sum().reset_index()
df_ventas_por_año_sinUK['Total'] = df_ventas_por_año_sinUK['Total'].astype(int)
df_ventas_por_año_sinUK['Año y mes'] = df_ventas_por_año_sinUK['Year'].astype(str) + '-' + df_ventas_por_año_sinUK['Month'].astype(str)

max_total_all = df_ventas_por_año['Total'].max()
max_total_sinUK = df_ventas_por_año_sinUK['Total'].max()

colors_all = ['Otras Ventas' if total != max_total_all else 'Venta Máxima' for total in df_ventas_por_año['Total']]
colors_sinUK = ['Otras Ventas' if total != max_total_sinUK else 'Venta Máxima' for total in df_ventas_por_año_sinUK['Total']]

fig1 = px.bar(df_ventas_por_año, x='Año y mes', y='Total', color=colors_all, title='Ventas por mes (con todos los países)')
fig1.update_layout(xaxis_title='Mes-Año', yaxis_title='Total')

fig2 = px.bar(df_ventas_por_año_sinUK, x='Año y mes', y='Total', color=colors_sinUK, title='Ventas por mes (sin United Kingdom)')
fig2.update_layout(xaxis_title='Mes-Año', yaxis_title='Total', yaxis_range=[0, max_total_sinUK * 1.1])


st.write('''Visualizamos en un gráfico de barras las ventas (Total) por mes de diciembre 2010 a diciembre 2011 con todos los países y en otro lo mismo pero sin UK.

La ausencia del Reino Unido hace que las cifras sean considerablemente más bajas en el segundo gráfico, lo que indica que el Reino Unido es un mercado dominante en el total de ventas. Además, la tendencia general en ambos gráficos es similar, pero el impacto del Reino Unido es claramente significativo en el total general, especialmente en los picos de ventas en ciertos meses del año.''')

with st.expander('Código'):
    st.code('''import plotly.express as px
import plotly.io as pio

# Configuración global de parámetros
pio.templates.default = "plotly"
pio.templates["plotly"].layout.colorway = px.colors.qualitative.Vivid
pio.templates["plotly"].layout.xaxis.tickangle = -90

df_ventas_por_año = df_limpio3.groupby(['Year', 'Month'])['Total'].sum().reset_index()
df_ventas_por_año['Total'] = df_ventas_por_año['Total'].astype(int)
df_ventas_por_año['Año y mes'] = df_ventas_por_año['Year'].astype(str) + '-' + df_ventas_por_año['Month'].astype(str)

df_limpio3_sinUK = df_limpio3[df_limpio3['Country'] != 'United Kingdom']
df_ventas_por_año_sinUK = df_limpio3_sinUK.groupby(['Year', 'Month'])['Total'].sum().reset_index()
df_ventas_por_año_sinUK['Total'] = df_ventas_por_año_sinUK['Total'].astype(int)
df_ventas_por_año_sinUK['Año y mes'] = df_ventas_por_año_sinUK['Year'].astype(str) + '-' + df_ventas_por_año_sinUK['Month'].astype(str)

max_total_all = df_ventas_por_año['Total'].max()
max_total_sinUK = df_ventas_por_año_sinUK['Total'].max()

colors_all = ['Otras Ventas' if total != max_total_all else 'Venta Máxima' for total in df_ventas_por_año['Total']]
colors_sinUK = ['Otras Ventas' if total != max_total_sinUK else 'Venta Máxima' for total in df_ventas_por_año_sinUK['Total']]

fig1 = px.bar(df_ventas_por_año, x='Año y mes', y='Total', color=colors_all, title='Ventas por mes (con todos los países)')
fig1.update_layout(xaxis_title='Mes-Año', yaxis_title='Total')

fig2 = px.bar(df_ventas_por_año_sinUK, x='Año y mes', y='Total', color=colors_sinUK, title='Ventas por mes (sin United Kingdom)')
fig2.update_layout(xaxis_title='Mes-Año', yaxis_title='Total', yaxis_range=[0, max_total_sinUK * 1.1])''')

# Selector para ver ventas con y sin UK
with st.expander('Visualización de Ventas por Mes'):
    opcion = st.selectbox('Seleccionar vista de ventas:', ['Con UK', 'Sin UK'], index=0)

    if opcion == 'Con UK':
        st.plotly_chart(fig1)
    else:
        st.plotly_chart(fig2)



st.html('''<h3><font color="06d6a0">5.2. Top 5 de Ventas por país</font></h3>''')
st.html('''<h4><font color="118ab2">5.2.1. Tratamiento de los datos</font></h4>''')

st.write('Agrupamos y sumamos los totales por país, ordenamos de forma descendente y visualizamos los primeros')

top_venta_pais = df_limpio3.groupby(['Country'])['Total'].sum().reset_index()
top_venta_pais = top_venta_pais.sort_values(by='Total', ascending=False)

with st.expander('Top 5 de Ventas por país'):
    st.code('''top_venta_pais = df_limpio3.groupby(['Country'])['Total'].sum().reset_index()
top_venta_pais = top_venta_pais.sort_values(by='Total', ascending=False)
top_venta_pais.head(5).round(2)''')
    st.dataframe(top_venta_pais.head(5).round(2))


st.html('''<h4><font color="118ab2">5.2.2. DataFrame Top 5 Año: País, Total y Año-Mes</font></h4>''')

paises_top5 = ['United Kingdom', 'France', 'Germany', 'Netherlands', 'Ireland']

df_top5_ventas_por_mes = df_limpio3[df_limpio3['Country'].isin(paises_top5)]

df_top5_columnas = df_top5_ventas_por_mes.groupby(['Year', 'Month', 'Country'])['Total'].sum().reset_index()
df_top5_columnas['Total'] = df_top5_columnas['Total'].astype(int)
df_top5_columnas['Año y mes'] = (df_top5_columnas['Year'].astype(str) + '-' + df_top5_columnas['Month'].astype(str))
df_top5_columnas = df_top5_columnas.drop(columns=['Year','Month'])


with st.expander('DataFrame Top 5 Año'):
    st.code('''paises_top5 = ['United Kingdom', 'France', 'Germany', 'Netherlands', 'Ireland']

df_top5_ventas_por_mes = df_limpio3[df_limpio3['Country'].isin(paises_top5)]

df_top5_columnas = df_top5_ventas_por_mes.groupby(['Year', 'Month', 'Country'])['Total'].sum().reset_index()
df_top5_columnas['Total'] = df_top5_columnas['Total'].astype(int)
df_top5_columnas['Año y mes'] = (df_top5_columnas['Year'].astype(str) + '-' + df_top5_columnas['Month'].astype(str))
df_top5_columnas = df_top5_columnas.drop(columns=['Year','Month'])
df_top5_columnas''')
    st.dataframe(df_top5_columnas)


st.html('''<h4><font color="118ab2">5.2.3 Gráfico de líneas: top 5 países - venta por mes</font></h4>''')

# Crear gráficos de líneas con Plotly
fig3 = px.line(df_top5_columnas, x='Año y mes', y='Total', color='Country', markers=True, title='Total por mes-año para cada país')
fig3.update_layout(xaxis_title='Mes-Año', yaxis_title='Total')

df_top_sinUK = df_top5_columnas[df_top5_columnas['Country'] != 'United Kingdom']
fig4 = px.line(df_top_sinUK, x='Año y mes', y='Total', color='Country', markers=True, title='Total por mes-año sin United Kingdom')
fig4.update_layout(xaxis_title='Mes-Año', yaxis_title='Total')

with st.expander('Código'):
    st.code('''fig3 = px.line(df_top5_columnas, x='Año y mes', y='Total', color='Country', markers=True, title='Total por mes-año para cada país')
fig3.update_layout(xaxis_title='Mes-Año', yaxis_title='Total')

df_top_sinUK = df_top5_columnas[df_top5_columnas['Country'] != 'United Kingdom']
fig4 = px.line(df_top_sinUK, x='Año y mes', y='Total', color='Country', markers=True, title='Total por mes-año sin United Kingdom')
fig4.update_layout(xaxis_title='Mes-Año', yaxis_title='Total')''')

# Mostrar gráficos uno al lado del otro
with st.expander('Visualización'):
    col1, col2 = st.columns(2)

with col1:
    st.plotly_chart(fig3)
    st.write('''- UK tiene un volumen de ventas significativamente mayor que los otros países (Irlanda, Francia, Alemania y Países Bajos) en todos los períodos del año. Esto hace que las fluctuaciones de los demás países sean difíciles de distinguir en la escala general.

- UK muestra picos de ventas particularmente altos alrededor de septiembre y octubre de 2011.''')

with col2:
    st.plotly_chart(fig4)
    st.write('''- **Variabilidad de ventas:** cada país muestra fluctuaciones a lo largo del año, esto indica una demanda inestable.

- **Picos de ventas:** Francia y los Países Bajos registran picos en noviembre. Alemania alcanza su punto máximo en mayo, mientras que Irlanda tiene ventas más constantes con un pico en febrero.''')

st.write('''**Con estos datos podemos sugerir realizar promociones específicas en los meses con menor demanda. También, estrategias promocionales enfocadas en los picos de ventas para aumentar los ticket promedio**''')


st.html('''<h3><font color="06d6a0">5.3. Distribución de ventas por día de la semana</font></h3>''')

st.write('''Visualizamos cómo son las ventas por día, qué día tiene más ventas, menos y en cuál no se realizaron ventas.''')

# Crear una columna con el día de la semana
df_limpio3['DayOfWeek'] = df_limpio3['InvoiceDate'].dt.day_name()

# Agrupar por día de la semana y sumar el total de ventas
ventas_por_dia = df_limpio3.groupby('DayOfWeek')['Total'].sum().reindex(
    ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
)

# Establecer las ventas del sábado a 0

max_day = ventas_por_dia.idxmax()
colors = ['Otros días' if day != max_day else 'Día con más ventas' for day in ventas_por_dia.index]

fig5 = px.bar(ventas_por_dia.reset_index(), x='DayOfWeek', y='Total', color=colors, title='Distribución de Ventas por Día de la Semana',height=700)
fig5.update_layout(xaxis_title='Día de la Semana', yaxis_title='Total de Ventas', xaxis={'categoryorder':'array', 'categoryarray':['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']})

with st.expander('Código'):
    st.code('''# Crear una columna con el día de la semana
df_limpio3['DayOfWeek'] = df_limpio3['InvoiceDate'].dt.day_name()

# Agrupar por día de la semana y sumar el total de ventas
ventas_por_dia = df_limpio3.groupby('DayOfWeek')['Total'].sum().reindex(
    ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
)

fig5 = px.bar(ventas_por_dia.reset_index(), x='DayOfWeek', y='Total', color_discrete_sequence=['#5d54e7'], title='Distribución de Ventas por Día de la Semana')
    fig5.update_layout(xaxis_title='Día de la Semana', yaxis_title='Total de Ventas', xaxis={'categoryorder':'array', 'categoryarray':['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']})''')


with st.expander('Análisis por día de la semana'):
    st.plotly_chart(fig5)
    st.write('''El jueves es el día de mayores ventas, se pueden planificar promociones específicas ese día para mas volumen de ventas. Para estos días de mayor tráfico se debe asegurar y garantizar el correcto funcionamiento del sitio.

El domingo es el día con menos ventas. Se pueden probar promociones especiales como descuentos en algunos productos o envío exprés para incentivar la compra y así aumentar la actividad.''')



st.html('''<h2><font color="ffd166">6. Análisis Geográfico de las Ventas</font></h2>''')

st.html('''<h3><font color="06d6a0">6.1. Evolución de las Ventas (país y mes)</font></h3>''')



with st.expander('Código'):
    st.code('''fig6=px.scatter_geo(
    df_top5_columnas,
    locations='Country',
    locationmode='country names',
    color='Country',
    hover_name='Country',
    hover_data='Total',
    projection='natural earth',
    size="Total",
    animation_frame='Año y mes',
    scope='europe',
    width=800
    )
fig6.update_layout(title='Evolución de las Ventas por Pais y por mes')
fig6.show()''')

df_top5_columnas_sinUK = df_top5_columnas[df_top5_columnas['Country'] != 'United Kingdom']

fig6=px.scatter_geo(
    df_top5_columnas,
    locations='Country',
    locationmode='country names',
    color='Country',
    hover_name='Country',
    hover_data='Total',
    projection='natural earth',
    size="Total",
    animation_frame='Año y mes',
    scope='europe'
    )
fig6.update_layout(title='Evolución de las Ventas por Pais y por mes')


fig7 = px.scatter_geo(
    df_top5_columnas_sinUK,
    locations='Country',
    locationmode='country names',
    color='Country',
    hover_name='Country',
    hover_data='Total',
    projection='natural earth',
    size="Total",
    animation_frame='Año y mes',
    scope='europe'
)
fig7.update_layout(title='Evolución de las Ventas por Pais y por mes (Sin UK)')

with st.expander('Visualización'):
    opcion_mapa = st.selectbox('Seleccionar vista de ventas:', ['Con UK', 'Sin UK'], index=0, key='mapa')

    if opcion_mapa == 'Con UK':
        st.plotly_chart(fig6)
        st.write('''El gráfico muestra la evolución de las ventas por país y por mes, destacando la importancia del Reino Unido en el volumen total de ventas. Se observa que el Reino Unido tiene un impacto significativo en las ventas mensuales, con picos notables en ciertos meses. Esto sugiere que las estrategias de marketing y ventas deben considerar la estacionalidad y la importancia del mercado del Reino Unido para maximizar el rendimiento.''')
    else:
        st.plotly_chart(fig7)
        st.write('''El gráfico muestra la evolución de las ventas por país y por mes, excluyendo al Reino Unido. Se observa que, sin el Reino Unido, Francia y Alemania tienen un impacto significativo en las ventas mensuales, con picos notables en ciertos meses. Esto sugiere que, aunque el Reino Unido es un mercado dominante, otros países también juegan un papel importante en el volumen total de ventas. Las estrategias de marketing y ventas deben considerar la estacionalidad y la importancia de estos mercados para maximizar el rendimiento y diversificar la base de clientes.''')


st.html('''<h3><font color="06d6a0">6.2. Total de Ventas (país)</font></h3>''')


fig8=px.scatter_geo(
df_top5_columnas,
    locations='Country',
    locationmode='country names',
    color='Country',
    hover_name='Country',
    hover_data='Total',
    projection='natural earth',
    size="Total",
    scope='europe',
    width=800
    )
fig8.update_layout(title='Total de las Ventas por Pais')


fig9 = px.scatter_geo(
    df_top5_columnas_sinUK,
    locations='Country',
    locationmode='country names',
    color='Country',
    hover_name='Country',
    hover_data='Total',
    projection='miller',
    size="Total",
    scope='europe',
    labels={'Total': 'Total de Ventas'},
    width=800
)
fig9.update_layout(title='Evolución de las Ventas por Pais y por mes (Sin UK)')

with st.expander('Código'):
    st.code('''fig8=px.scatter_geo(
    df_top5_columnas,
    locations='Country',
    locationmode='country names',
    color='Country',
    hover_name='Country',
    hover_data='Total',
    projection='natural earth',
    size="Total",
    scope='europe',
    width=800
    )
fig8.update_layout(title='Total de las Ventas por Pais')''')
    
with st.expander('Visualización'):
    opcion_mapa_total = st.selectbox('Seleccionar vista de ventas:', ['Con UK', 'Sin UK'], index=0, key='mapa_total')

    if opcion_mapa_total == 'Con UK':
        st.plotly_chart(fig8)
        st.write('''El gráfico muestra que el Reino Unido es el país con el mayor volumen de ventas, seguido por Francia, Alemania, Países Bajos e Irlanda. Esto resalta la importancia del mercado del Reino Unido en el total de ventas. Las estrategias de marketing y ventas deben enfocarse en mantener y aumentar la participación en estos mercados clave.''')
    else:
        st.plotly_chart(fig9)
        st.write('''El gráfico muestra que, sin incluir al Reino Unido, Francia y Alemania son los países con el mayor volumen de ventas, seguidos por los Países Bajos e Irlanda. Esto indica que, aunque el Reino Unido es un mercado dominante, estos otros países también representan una parte significativa del total de ventas. Las estrategias de marketing y ventas deben considerar estos mercados para diversificar y reducir la dependencia del Reino Unido.''')



st.html('''<h2><font color="ffd166">7. Análisis por producto</font></h2>''')

st.html('''<h3><font color="06d6a0">7.1. Unidades Vendidas y Ganancia Generada</font></h3>''')

df_productos = df_limpio3

# Top 10 productos por unidades vendidas
top_quantity = df_productos.groupby('Description')['Quantity'].sum().nlargest(10).reset_index().sort_values(by='Quantity', ascending=True)

# Top 10 productos por ganancia generada
top_revenue = df_productos.groupby('Description')['Total'].sum().nlargest(10).reset_index().sort_values(by='Total', ascending=True)

# Crear gráfico de barras para unidades vendidas
fig10 = go.Figure()
fig10.add_trace(go.Bar(x=top_quantity['Quantity'], y=top_quantity['Description'], orientation='h',
                      marker=dict(color=px.colors.qualitative.Vivid), name="Unidades Vendidas"))
fig10.update_layout(title_text="Top 10 Productos por Unidades Vendidas")
fig10.update_xaxes(title_text="Unidades Vendidas")
fig10.update_yaxes(title_text="Producto")

# Crear gráfico de barras para ganancia generada
fig11 = go.Figure()
fig11.add_trace(go.Bar(x=top_revenue['Total'], y=top_revenue['Description'], orientation='h',
                     marker=dict(color=px.colors.qualitative.Vivid), name="Ganancia Generada"))
fig11.update_layout(title_text="Top 10 Productos por Ganancia Generada")
fig11.update_xaxes(title_text="Ganancia ($)")
fig11.update_yaxes(title_text="Producto")

st.write("""Analizamos las ventas por productos es importante distinguir entre qué es lo más vendido (gráfico de la izquierda) y qué genera más ingresos (gráfico de la derecha), y vemos que no necesariamente coincide. Esto sirve para comprender cuáles de los productos vendidos son más atractivos para los clientes y cuáles de los mismos generan más ganancia para la empresa. En base a eso se pueden realizar luego análisis adicionales para determinar si es conveniente dejar de vender un producto que aunque popular no conlleva ganancias acordes, o si es posible propocionar ciertos productos que dejan mayor margen de ganancia y buscar generar interés en los clientes. Asimismo vemos que en ambos gráficos los puestos 2 y 3 de cada ranking están ocupados por los mismos productos. Eso indicaría que fomentar la venta de los mismos puede aumentar en paralelo el interés de los clientes y las ganancias de la empresa.""")

with st.expander('Código'):
    st.code('''df_productos = df_limpio3

# Top 10 productos por unidades vendidas
top_quantity = df_productos.groupby('Description')['Quantity'].sum().nlargest(10).reset_index().sort_values(by='Quantity', ascending=True)

# Top 10 productos por ganancia generada
top_revenue = df_productos.groupby('Description')['Total'].sum().nlargest(10).reset_index().sort_values(by='Total', ascending=True)

# Crear gráfico de barras para unidades vendidas
fig10 = go.Figure()
fig10.add_trace(go.Bar(x=top_quantity['Quantity'], y=top_quantity['Description'], orientation='h',
                      marker=dict(color=px.colors.qualitative.Vivid), name="Unidades Vendidas"))
fig10.update_layout(title_text="Top 10 Productos por Unidades Vendidas")
fig10.update_xaxes(title_text="Unidades Vendidas")
fig10.update_yaxes(title_text="Producto")

# Crear gráfico de barras para ganancia generada
fig11 = go.Figure()
fig11.add_trace(go.Bar(x=top_revenue['Total'], y=top_revenue['Description'], orientation='h',
                     marker=dict(color=px.colors.qualitative.Vivid), name="Ganancia Generada"))
fig11.update_layout(title_text="Top 10 Productos por Ganancia Generada")
fig11.update_xaxes(title_text="Ganancia ($)")
fig11.update_yaxes(title_text="Producto")''')

with st.expander('Visualización'):
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(fig10)
    with col2:
        st.plotly_chart(fig11)

st.write('''Alineado con los datos previamente visualizados donde se evidencia la preponderancia de Reino Unido en comparación a otros países al analizar los productos más vendidos cambia significativamente si dejamos por fuera a UK.''')
st.html('''<h3><font color="06d6a0">7.2. Top 5 Productos en los 5 países con más ventas</font></h3>''')

# Filtrar el DataFrame para incluir solo cantidades mayores a cero
df_positive_sales = df_productos[df_productos['Quantity'] > 0]

# Paso 1: Encontrar los 5 países con mayor cantidad de ventas (sumando la columna "Quantity")
top_5_countries = (df_positive_sales.groupby('Country')['Quantity']
                   .sum()
                   .nlargest(5)
                   .reset_index())
top_5_countries_list = top_5_countries['Country'].tolist()

# Paso 2: Filtrar el DataFrame solo para estos 5 países
df_top_countries = df_positive_sales[df_positive_sales['Country'].isin(top_5_countries_list)]

# Paso 3: Agrupar por país y producto para sumar las cantidades vendidas
top_products_in_top_countries = (df_top_countries.groupby(['Country', 'Description'])['Quantity']
                                 .sum()
                                 .reset_index()
                                 .sort_values(['Country', 'Quantity'], ascending=[True, False]))

# Paso 4: Seleccionar los 5 productos más vendidos por país
top_5_products_in_top_countries = top_products_in_top_countries.groupby('Country').head(5)

# Crear DataFrame sin UK
df_top_countries_sinUK = df_top_countries[df_top_countries['Country'] != 'United Kingdom']
top_products_in_top_countries_sinUK = (df_top_countries_sinUK.groupby(['Country', 'Description'])['Quantity']
                                       .sum()
                                       .reset_index()
                                       .sort_values(['Country', 'Quantity'], ascending=[True, False]))
top_5_products_in_top_countries_sinUK = top_products_in_top_countries_sinUK.groupby('Country').head(5)

# Paso 5: Graficar
fig_top_products_top_countries = px.bar(top_5_products_in_top_countries, x='Quantity', y='Description',
                                        color='Country', orientation='h',
                                        title="Top 5 Productos Más Vendidos en los 5 Países con Más Ventas",
                                        labels={"Quantity": "Cantidad de Unidades", "Description": "Producto", "Country": "País"})
fig_top_products_top_countries.update_layout(xaxis_title="Unidades Vendidas", yaxis_title="Producto",
                                             title_x=0.5, font=dict(size=12), barmode='stack')

fig_top_products_top_countries_sinUK = px.bar(top_5_products_in_top_countries_sinUK, x='Quantity', y='Description',
                                              color='Country', orientation='h',
                                              title="Top 5 Productos Más Vendidos en los 5 Países con Más Ventas (Sin UK)",
                                              labels={"Quantity": "Cantidad de Unidades", "Description": "Producto", "Country": "País"})
fig_top_products_top_countries_sinUK.update_layout(xaxis_title="Unidades Vendidas", yaxis_title="Producto",
                                                   title_x=0.5, font=dict(size=12), barmode='stack')

with st.expander('Código'):
    st.code('''# Filtrar el DataFrame para incluir solo cantidades mayores a cero
df_positive_sales = df_productos[df_productos['Quantity'] > 0]

# Paso 1: Encontrar los 5 países con mayor cantidad de ventas (sumando la columna "Quantity")
top_5_countries = (df_positive_sales.groupby('Country')['Quantity']
                   .sum()
                   .nlargest(5)
                   .reset_index())
top_5_countries_list = top_5_countries['Country'].tolist()

# Paso 2: Filtrar el DataFrame solo para estos 5 países
df_top_countries = df_positive_sales[df_positive_sales['Country'].isin(top_5_countries_list)]

# Paso 3: Agrupar por país y producto para sumar las cantidades vendidas
top_products_in_top_countries = (df_top_countries.groupby(['Country', 'Description'])['Quantity']
                                 .sum()
                                 .reset_index()
                                 .sort_values(['Country', 'Quantity'], ascending=[True, False]))

# Paso 4: Seleccionar los 5 productos más vendidos por país
top_5_products_in_top_countries = top_products_in_top_countries.groupby('Country').head(5)

# Crear DataFrame sin UK
df_top_countries_sinUK = df_top_countries[df_top_countries['Country'] != 'United Kingdom']
top_products_in_top_countries_sinUK = (df_top_countries_sinUK.groupby(['Country', 'Description'])['Quantity']
                                       .sum()
                                       .reset_index()
                                       .sort_values(['Country', 'Quantity'], ascending=[True, False]))
top_5_products_in_top_countries_sinUK = top_products_in_top_countries_sinUK.groupby('Country').head(5)

# Paso 5: Graficar
fig_top_products_top_countries = px.bar(top_5_products_in_top_countries, x='Quantity', y='Description',
                                        color='Country', orientation='h',
                                        title="Top 5 Productos Más Vendidos en los 5 Países con Más Ventas",
                                        labels={"Quantity": "Cantidad de Unidades", "Description": "Producto", "Country": "País"})
fig_top_products_top_countries.update_layout(xaxis_title="Unidades Vendidas", yaxis_title="Producto",
                                             title_x=0.5, font=dict(size=12), barmode='stack')

fig_top_products_top_countries_sinUK = px.bar(top_5_products_in_top_countries_sinUK, x='Quantity', y='Description',
                                              color='Country', orientation='h',
                                              title="Top 5 Productos Más Vendidos en los 5 Países con Más Ventas (Sin UK)",
                                              labels={"Quantity": "Cantidad de Unidades", "Description": "Producto", "Country": "País"})
fig_top_products_top_countries_sinUK.update_layout(xaxis_title="Unidades Vendidas", yaxis_title="Producto",
                                                   title_x=0.5, font=dict(size=12), barmode='stack')''')

with st.expander('Visualización'):
    opcion_top_productos = st.selectbox('Seleccionar vista de ventas:', ['Con UK', 'Sin UK'], index=0, key='top_productos')
    if opcion_top_productos == 'Con UK':
        st.plotly_chart(fig_top_products_top_countries)
    else:
        st.plotly_chart(fig_top_products_top_countries_sinUK)


st.html('''<h2><font color="ffd166">8. Análisis de Clientes</font></h2>''')

st.html('''<h3><font color="06d6a0">8.1. Frecuencia de Compra y Gasto Promedio</font></h3>''')

# Frecuencia de compras
compras_por_cliente = df_limpio3.groupby('CustomerID')['InvoiceNo'].count().reset_index()
compras_por_cliente.sort_values(by='InvoiceNo', ascending=False, inplace=True)
compras_por_cliente.rename(columns={'InvoiceNo': 'CantidadCompras'}, inplace=True)

# Gastos promedio cliente
df_sinUK = df_limpio3[df_limpio3['Country'] != 'United Kingdom']
gasto_promedio_cliente = df_sinUK.groupby('CustomerID')['Total'].mean().reset_index()
gasto_promedio_cliente.sort_values(by='Total', ascending=True, inplace=True)
gasto_promedio_cliente.rename(columns={'Total': 'GastoPromedio'}, inplace=True)

# Crear gráficos con Plotly
fig_frecuencia = px.histogram(compras_por_cliente, x='CantidadCompras', nbins=100, title='Frecuencia de Compras por Cliente')
fig_frecuencia.update_layout(xaxis_title='Cantidad de Compras', yaxis_title='Frecuencia')

fig_gasto_promedio = px.scatter(gasto_promedio_cliente, x='CustomerID', y='GastoPromedio', title='Gasto Promedio por Cliente')
fig_gasto_promedio.update_layout(xaxis_title='ID de Cliente', yaxis_title='Gasto Promedio (USD)')

# Selector para ver frecuencia de compras o gasto promedio

with st.expander('Código'):
    st.code('''# Frecuencia de compras
# cantidad de compras por cliente.
compras_por_cliente = df_limpio3.groupby('CustomerID')['InvoiceNo'].count().reset_index()
compras_por_cliente.sort_values(by='InvoiceNo', ascending=False)
compras_por_cliente.rename(columns={'InvoiceNo': 'CantidadCompras'}, inplace=True)
compras_por_cliente =compras_por_cliente['CantidadCompras']
#print(compras_por_cliente)

# gastos promedio cliente
df_sinUK = df_limpio3[df_limpio3['Country'] != 'United Kingdom']
# Calcula el gasto promedio por cliente
gasto_promedio_cliente= df_sinUK.groupby('CustomerID')['Total'].mean()
print(gasto_promedio_cliente.sort_values(ascending=True))


# Crea la figura con dos subplots
fig, axes = plt.subplots(1, 2, figsize=(16, 6))

# Histograma de frecuencia de compras
axes[0].hist(compras_por_cliente, bins=100, edgecolor='black')
axes[0].set_xlabel('Cantidad de Compras')
axes[0].set_ylabel('Frecuencia')
axes[0].set_title('Frecuencia de Compras por cliente')
axes[0].set_xlim(0, 900)  # Establece el límite del eje x

# Gráfico de dispersión del gasto promedio por cliente
axes[1].scatter(gasto_promedio_cliente.index, gasto_promedio_cliente.values)
axes[1].set_xlabel('ID de Cliente')
axes[1].set_ylabel('Gasto promedio (USD)')
axes[1].set_title('Gasto Promedio por Cliente')''')

with st.expander('Visualización'):
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(fig_frecuencia)
    with col2:
        st.plotly_chart(fig_gasto_promedio)


st.html('''<h3><font color="06d6a0">8.2.  Top 5 de clientes con mayor gasto en compras y top 5 de productos más adquiridos por estos clientes.</font></h3>''')

# Top 5 de clientes que más gastaron (customerID, Total), redondeando Total.
top_5_clientes = df_limpio3.groupby('CustomerID')['Total'].sum().round(2).nlargest(5).reset_index()

# Obtener la lista de los CustomerID de los top 5 clientes
top_5_customer_ids = top_5_clientes['CustomerID']

# Filtrar el DataFrame para incluir solo las compras de los top 5 clientes
df_top_customers = df_limpio3[df_limpio3['CustomerID'].isin(top_5_customer_ids)]

# Agrupar por descripción del producto y sumar la cantidad
top_products = df_top_customers.groupby('Description')['Quantity'].sum().nlargest(5).reset_index()

# Graficar los resultados con Plotly
fig_top_products = px.bar(top_products, x='Description', y='Quantity', title='Top 5 Productos más consumidos por los Top 5 Clientes',height=700)
fig_top_products.update_layout(xaxis_title='Descripción del Producto', yaxis_title='Cantidad', xaxis_tickangle=-45)

with st.expander("Código"):
    st.code("""# Top 5 de clientes que más gastaron (customerID, Total), redondeando Total.
top_5_clientes = df_limpio3.groupby('CustomerID')['Total'].sum().round(2).nlargest(5).reset_index()
print(top_5_clientes)

# Obtener la lista de los CustomerID de los top 5 clientes
top_5_customer_ids = top_5_clientes['CustomerID']

# Filtrar el DataFrame para incluir solo las compras de los top 5 clientes
df_top_customers = df_limpio3[df_limpio3['CustomerID'].isin(top_5_customer_ids)]

# Agrupar por descripción del producto y sumar la cantidad
top_products = df_top_customers.groupby('Description')['Quantity'].sum().nlargest(5).reset_index()

# Mostrar los resultados
#print("Top 5 productos más comprados por los top 5 clientes:")
#print(top_products)


# Graficar los resultados
import matplotlib.pyplot as plt

plt.figure(figsize=(10, 6))
plt.bar(top_products['Description'], top_products['Quantity'])
plt.xlabel("Descripción del Producto")
plt.ylabel("Cantidad")
plt.title("Top 5 Productos más consumidos por los Top 5 Clientes")
plt.xticks(rotation=45, ha="right")""")

with st.expander('Visualización'):
    st.write(top_5_clientes)
    st.plotly_chart(fig_top_products)



st.divider()

st.html('''<h1><font color="#ef476f">Conclusiones</font></h1>''')

with st.expander("Conclusiones:"):
    st.write('''El análisis detallado de las ventas y el comportamiento del mercado proporciona una base sólida para desarrollar estrategias comerciales y de marketing efectivas. Al enfocarse en los mercados clave, optimizar el inventario, personalizar las ofertas para los clientes y expandir la presencia en mercados menos explotados, la empresa puede mejorar su rendimiento y aumentar su rentabilidad.''')











st.divider()


st.html('''<h1><font color="#ef476f">De Yapa</font></h1>''')
st.html('''<h2><font color="ffd166">9. Análisis de Clientes</font></h2>''')

st.html('''<h3><font color="06d6a0">9.1. Mapa Coroplético</font></h3>''')


# Crear DataFrame para cantidad de clientes por país
clientes_por_pais = df_limpio3.groupby('Country')['CustomerID'].nunique().reset_index()
clientes_por_pais.columns = ['Country', 'CustomerCount']

# Crear DataFrame sin UK
clientes_por_pais_sinUK = clientes_por_pais[clientes_por_pais['Country'] != 'United Kingdom']

# Crear mapa coroplético con todos los países
fig12 = px.choropleth(
    clientes_por_pais,
    locations='Country',
    locationmode='country names',
    color='CustomerCount',
    hover_name='Country',
    title='Cantidad de Clientes por País',
    width=1920
)
#fig12.update_layout(geo=dict(scope='europe'))

# Crear mapa coroplético sin UK
fig13 = px.choropleth(
    clientes_por_pais_sinUK,
    locations='Country',
    locationmode='country names',
    color='CustomerCount',
    hover_name='Country',
    title='Cantidad de Clientes por País (Sin UK)',
    width=1920
)
#fig13.update_layout(geo=dict(scope='europe'))

with st.expander('Código'):
    st.code('''# Crear DataFrame para cantidad de clientes por país
clientes_por_pais = df_limpio3.groupby('Country')['CustomerID'].nunique().reset_index()
clientes_por_pais.columns = ['Country', 'CustomerCount']

# Crear DataFrame sin UK
clientes_por_pais_sinUK = clientes_por_pais[clientes_por_pais['Country'] != 'United Kingdom']

# Crear mapa coroplético con todos los países
fig12 = px.choropleth(
    clientes_por_pais,
    locations='Country',
    locationmode='country names',
    color='CustomerCount',
    hover_name='Country',
    title='Cantidad de Clientes por País',
    width=1920
)
#fig12.update_layout(geo=dict(scope='europe'))

# Crear mapa coroplético sin UK
fig13 = px.choropleth(
    clientes_por_pais_sinUK,
    locations='Country',
    locationmode='country names',
    color='CustomerCount',
    hover_name='Country',
    title='Cantidad de Clientes por País (Sin UK)',
    width=1920
)''')

with st.expander('Visualización'):
    opcion_clientes = st.selectbox('Seleccionar vista de clientes:', ['Con UK', 'Sin UK'], index=0, key='clientes')

#    if opcion_clientes == 'Con UK':
#        st.plotly_chart(fig12)
#    else:
#        st.plotly_chart(fig13)

    scope_option = st.selectbox('Seleccionar alcance del mapa:', ['Europa', 'Todo el mundo'], index=0, key='scope')

    if opcion_clientes == 'Con UK':
        if scope_option == 'Europa':
            fig12.update_layout(geo=dict(scope='europe'))
        else:
            fig12.update_layout(geo=dict(scope='world'))
        st.plotly_chart(fig12)
    else:
        if scope_option == 'Europa':
            fig13.update_layout(geo=dict(scope='europe'))
        else:
            fig13.update_layout(geo=dict(scope='world'))
        st.plotly_chart(fig13)



st.html('''<h3><font color="06d6a0">9.2. Cantidad de clientes por pais (Top 10)</font></h3>''')

# Top 10 países con mayor cantidad de clientes
top_10_paises_mas_clientes = clientes_por_pais.nlargest(10, 'CustomerCount').sort_values(by='CustomerCount', ascending=True)

# Top 10 países con menor cantidad de clientes
top_10_paises_menos_clientes = clientes_por_pais.nsmallest(10, 'CustomerCount').sort_values(by='CustomerCount', ascending=True)

# Crear gráfico de barras para los 10 países con mayor cantidad de clientes
fig14 = go.Figure()
fig14.add_trace(go.Bar(x=top_10_paises_mas_clientes['CustomerCount'], y=top_10_paises_mas_clientes['Country'], orientation='h',
                      marker=dict(color=px.colors.qualitative.Vivid), name="Cantidad de Clientes"))
fig14.update_layout(title_text="Top 10 Países con Mayor Cantidad de Clientes")
fig14.update_xaxes(title_text="Cantidad de Clientes")
fig14.update_yaxes(title_text="País")

# Crear gráfico de barras para los 10 países con menor cantidad de clientes
fig15 = go.Figure()
fig15.add_trace(go.Bar(x=top_10_paises_menos_clientes['CustomerCount'], y=top_10_paises_menos_clientes['Country'], orientation='h',
                      marker=dict(color=px.colors.qualitative.Vivid), name="Cantidad de Clientes"))
fig15.update_layout(title_text="Top 10 Países con Menor Cantidad de Clientes")
fig15.update_xaxes(title_text="Cantidad de Clientes")
fig15.update_yaxes(title_text="País")

with st.expander('Visualización'):
    opcion_clientes_top = st.selectbox('Seleccionar vista de clientes:', ['Top 10 Países con Mayor Cantidad de Clientes', 'Top 10 Países con Menor Cantidad de Clientes'], index=0, key='clientes_top')

    if opcion_clientes_top == 'Top 10 Países con Mayor Cantidad de Clientes':
        incluir_uk = st.checkbox('Incluir UK en el análisis', value=True, key='incluir_uk')
        if not incluir_uk:
            top_10_paises_mas_clientes = top_10_paises_mas_clientes[top_10_paises_mas_clientes['Country'] != 'United Kingdom']
        fig14 = go.Figure()
        fig14.add_trace(go.Bar(x=top_10_paises_mas_clientes['CustomerCount'], y=top_10_paises_mas_clientes['Country'], orientation='h',
                              marker=dict(color=px.colors.qualitative.Vivid), name="Cantidad de Clientes"))
        fig14.update_layout(title_text="Top 10 Países con Mayor Cantidad de Clientes")
        fig14.update_xaxes(title_text="Cantidad de Clientes")
        fig14.update_yaxes(title_text="País")
        st.plotly_chart(fig14)
        st.write('''El gráfico muestra los 10 países con mayor cantidad de clientes. Se observa que el Reino Unido tiene la mayor cantidad de clientes, seguido por Alemania y Francia. Esto indica que estos países son mercados clave y deben ser considerados en las estrategias de marketing y ventas para maximizar el rendimiento.''')
    else:
        st.plotly_chart(fig15)
        st.write('''El gráfico muestra los 10 países con menor cantidad de clientes. Se observa que estos países tienen una base de clientes más pequeña, lo que sugiere que hay oportunidades para expandir la presencia en estos mercados a través de estrategias de marketing y ventas específicas.''')











