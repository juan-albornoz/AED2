import streamlit as st
from Introducción import configuraciones
import pandas as pd
import plotly.express as px

configuraciones("AED", "📝")

st.title('Análisis Exploratorio de Datos')
st.write('Acá es donde vamos a mostrar toda la limpieza de nuestros datos.')
df=pd.read_csv('Data/Online-Retail.csv',sep=';')
df['UnitPrice'] = df['UnitPrice'].str.replace(',', '.').astype(float)
df['Total'] = df['Quantity'] * df['UnitPrice']
df_top5 = df.groupby('Country')['Total'].sum().nlargest(5).reset_index()
st.write('Top 5 países por ventas totales:')
st.dataframe(df_top5)
fig=px.bar(df_top5,x='Country',y='Total',title='Ventas por País')
st.plotly_chart(fig)