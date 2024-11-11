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
    configuraciones("Introducción", "💻")
    st.image('IFTS_18.png', width=200)
    st.html('''<h1><font color="ef476f">Análisis Exploratorio Grupo N°2</font></h1>''')
    st.html('<h3><b>🏫 Instituto:</b> IFTS 18.</h3>')
    st.html('<h3><b>📝 Materia:</b> Análisis Exploratorio de Datos.</h3>')
    st.html('<h3><b>👨🏻‍🏫 Docente:</b> Ing. Miguel Pita.</h3>')
    st.html('<h3><b>💾 Dataset:</b> <code><font color="ef476f">online_retail</font></code></h3>')

if __name__ == '__main__':
    app()