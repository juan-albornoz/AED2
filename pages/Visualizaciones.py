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
    st.code('''paises_top5 = ['United Kingdom', 'France', 'Germany', 'Netherlands', 'EIRE']

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

# Selector para ver evolución de ventas con y sin UK
with st.expander('Visualización de Evolución de Ventas'):
    opcion_evolucion = st.selectbox('Seleccionar vista de evolución de ventas:', ['Con UK', 'Sin UK'], index=0)

    if opcion_evolucion == 'Con UK':
        st.plotly_chart(fig3)
        st.write('''- UK tiene un volumen de ventas significativamente mayor que los otros países (Irlanda, Francia, Alemania y Países Bajos) en todos los períodos del año. Esto hace que las fluctuaciones de los demás países sean difíciles de distinguir en la escala general.

- UK muestra picos de ventas particularmente altos alrededor de septiembre y octubre de 2011.''')
    else:
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
max_day = ventas_por_dia.idxmax()
colors = ['Otros días' if day != max_day else 'Día con más ventas' for day in ventas_por_dia.index]

fig5 = px.bar(ventas_por_dia.reset_index(), x='DayOfWeek', y='Total', color=colors, title='Distribución de Ventas por Día de la Semana')
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
    scope='europe',
    width=800
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
    opcion_producto=st.selectbox('Seleccionar vista de ventas:', ['Unidades Vendidas', 'Ganancia Generada'], index=0, key='productos')
    if opcion_producto == 'Unidades Vendidas':
        st.plotly_chart(fig10)
        st.write('''El gráfico muestra los 10 productos más vendidos por unidades. Se observa que los productos más vendidos son 'WORLD WAR 2 GLIDERS ASSTD DESIGNS' y 'JUMBO BAG RED RETROSPOT'. Esto indica que estos productos tienen una alta demanda y podrían ser considerados para promociones especiales o para mantener un inventario adecuado para satisfacer la demanda del mercado.''')
    else:
        st.plotly_chart(fig11)
        st.write('''El gráfico muestra los 10 productos que generan más ganancias. Se observa que los productos que generan más ganancias son 'REGENCY CAKESTAND 3 TIER' y 'WHITE HANGING HEART T-LIGHT HOLDER'. Esto indica que estos productos tienen un alto valor de venta y podrían ser considerados para estrategias de marketing y ventas para aumentar la rentabilidad.''')



st.html('''<h2><font color="ffd166">8. Análisis de Clientes</font></h2>''')

st.html('''<h3><font color="06d6a0">7.1. Mapa Coroplético</font></h3>''')


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



st.html('''<h3><font color="06d6a0">7.2. Cantidad de clientes por pais (Top 10)</font></h3>''')

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











