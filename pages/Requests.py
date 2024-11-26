import streamlit as st
import pandas as pd
from datetime import datetime

st.subheader("Solicitudes realizadas por el personal de TRS en espera de aprobación")

# Abrimos nuestro CSV
df = pd.read_csv('Databases/TRS_csv 1.csv', index_col="ID")
blocked_cols = ["ID",
                "Fecha",
                "Nombre",
                "Puesto",
                "Tipo de solicitud",
                "EPP a solicitar",
                "Justificacion de reemplazo",
                "EPP a reemplazar",
                "Comentarios",
                "Ultima modificacion"]


# Mostrar el editor de datos
edited_df = st.data_editor(df, disabled=blocked_cols, use_container_width=True)

# Verificar si se han realizado cambios
if not edited_df.equals(df):
    # Encontrar las filas donde se ha modificado la columna "Estado"
    cambios = edited_df[edited_df["Estado"] != df["Estado"]]
    
    # Actualizar la columna "Ultima modificacion" para las filas modificadas
    for index in cambios.index:
        edited_df.at[index, "Ultima modificacion"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Guardar los cambios en el CSV
    edited_df.to_csv('Databases/TRS_csv 1.csv')

    st.success("Los cambios se han guardado correctamente.")

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
