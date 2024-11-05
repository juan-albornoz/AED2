import streamlit as st
from Introducción import configuraciones
import pandas as pd
import plotly.express as px
from pages.AED import df 

configuraciones("Visualizaciones", "📊")

st.title('Visualizaciones')
st.write('En esta página vamos a reflejar el análisis a través de los gráficos.')
fig=px.bar(df,x='Country',y='Total',title='Ventas por País')
st.plotly_chart(fig)
