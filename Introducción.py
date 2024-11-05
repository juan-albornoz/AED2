import streamlit as st

def configuraciones(page_title, page_icon):
    st.set_page_config(page_title, page_icon, layout='wide')
    with st.sidebar:
        st.logo("IFTS_18.png")
        st.title('Grupo N°2')
        with st.expander('Integrantes'):
            st.write('''- Juan José Albornoz
- Estefany Herrera Martínez
- Cecilia Estevez
- Micaela Manzan
- Gonzalo Rey del Castillo''')


def app():
    configuraciones("Introdución", "💻")
    st.image('IFTS_18.png')
    st.title('Introducción')
    st.write('Bienvenido al Análisis Exploratorio de Datos del Grupo N°2 por la Materia de Análisis Exploratorio de Datos a Cargo del Ing. Miguel Pita.')
    st.markdown('''Vamos a trabajar con el dataset de `online_retail.xlsx`, el cual contiene información de ventas de una empresa de artículos de cotillón.
''')

if __name__ == '__main__':
    app()