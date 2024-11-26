import streamlit as st
import pandas as pd

st.image(image="https://dam.bakerhughes.com/m/6ce7dc7bd0fc30fc/original/Baker-Hughes-Logo.svg", width=800)
st.title("Pagina principal")

st.info("El estado sera modificado por el encargado de aprobar esta solicitud", icon="⚠️")

# Abrimos nuestro CSV

df = pd.read_csv('Databases/TRS_csv 1.csv')
df.columns = df.columns.str.strip()

blocked_cos = ["ID",
                "Fecha",
                "Nombre",
                "Puesto",
                "Tipo de solicitud",
                "EPP a solicitar",
                "Justificacion de reemplazo",
                "EPP a reemplazar",
                "Comentarios",
                "Ultima modificacion"]

# Opciones de visualización 

tab1, tab2 = st.tabs(["Vista general", "Vista en tabla completa"])

with tab1:
    for index, datos in df.iterrows():
        with st.container(border=True):
            equipo_solicitado = datos["EPP a solicitar"]
            if pd.isna(equipo_solicitado) or equipo_solicitado.strip() == "":
                equipo_solicitado = datos["EPP a reemplazar"]
            
            st.write(f'ID de orden: {datos["ID"]}')
            st.write(f'Fecha de solicitud: {datos["Fecha"]}')
            st.write(f'Equipo Solicitado: {equipo_solicitado}')
            st.write(f'Comentarios: {datos["Comentarios"]}')
            st.write(f'Estado de solicitud: {datos["Estado"]}')
            
            if datos["Estado"].lower() == "negado":
                st.warning("Ha sido negada su solicitud", icon="❌")
            elif datos["Estado"].lower() == "en proceso":
                st.status("Se sigue en estado de aprobación")
            else:
                st.success("Solicitud aprobada!", icon="✅")
            
with tab2:
    st.dataframe(df)
    
    
# Definir el HTML y CSS para el footer
footer = """
    <style>
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #FFFFFF;
        color: black;
        text-align: center;
        padding: 10px;
    }
    </style>
    <div class="footer">
        <p> ® Baker Hughes Confidential</p>
    </div>
    """
    # Insertar el footer en la aplicación
st.markdown(footer, unsafe_allow_html=True)
