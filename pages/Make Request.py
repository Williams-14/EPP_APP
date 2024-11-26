import streamlit as st
import datetime
import sqlite3 as sql
import pandas as pd
from time import sleep

pages = ["Home", "Make Request", "Requests"]

st.image(image="https://dam.bakerhughes.com/m/6ce7dc7bd0fc30fc/original/Baker-Hughes-Logo.svg", use_container_width=True)

st.title("Crear una nueva solicitud")

# Campo de fecha con la fecha actual como predeterminada
date = st.date_input("Fecha de solicitud", value=datetime.date.today())

#Crear conexión con base de datos para su actualización 
conn = sql.connect('Databases/TRS_Personal 1.db')
cursor = conn.cursor()


# Campo de texto para el nombre del solicitante

data_nombres = cursor.execute("SELECT Nombre FROM Usuarios").fetchall()

nombres_operadores = [nombre[0] for nombre in data_nombres]
name = st.selectbox("Nombre del solicitante*", nombres_operadores, placeholder="Nombre", index=None)

# Campo par ingresar el puesto del solicitante
puesto_emp = st.text_input("Puesto que desempeña")

# Selector de tipo de solicitud usando selectbox
tipo_solicitud = st.selectbox("Tipo de solicitud*", ["Nueva solicitud", "Reemplazo"])

# Inicializar variables
EPP_solicitado = ""
justificacion = ""
epp_reemplazo = ""

# Mostrar campos adicionales basados en la selección del tipo de solicitud
if tipo_solicitud == "Nueva solicitud":
    EPP_solicitado = st.multiselect("Selecciona el EPP", 
                                    ["Botas de cuero", 
                                     "Botas de hule", 
                                     "Casco", 
                                     "Gafas de protección", 
                                     "Guantes de alto impacto", 
                                     "Barbiquejo", 
                                     "Impermeable", 
                                     "Tyvek", 
                                     "Overol"])
else:
    epp_reemplazo = st.text_input("Que epp desea reemplazar", placeholder="Solo nombres específicos")
    
    justificacion = st.text_input("Justificación por reemplazo", placeholder="Breve justificación para darle seguimiento")

comentarios = st.text_input("Comentarios adicionales a su solicitud", placeholder="Sin comentarios",help="Si solicita algo que requiera talla, favor de colocarlo aquí")

# estado = st.selectbox("Estado de la solicitud", ["En proceso", "Aprobado", "Negado"], index=0)

st.info("Veras el estado de tu solicitud en la pagina principal", icon="ℹ️")



# Parte modificada para trabajar desde un CSV

def add_to_csv(fecha, nombre, tiposolicitud, puesto, EPP_soli=" ", justificacion=" ", comentario=" ", EPP_cambio=" ", Estado="En proceso"): # cspell: disable-line
    ruta = "Databases/TRS_csv 1.csv"
    df = pd.read_csv(ruta, encoding="latin-1")
    new_id = df["ID"].max() + 1 if not df.empty else 1 # Agregar de manera automática los indices de las solicitudes 
    
    # Agregar los datos a la base de datos de excel 
    new_order = pd.DataFrame([{
        "ID":new_id,
        "Fecha":fecha,
        "Nombre":nombre,
        "Puesto":puesto,
        "Tipo de solicitud":tiposolicitud,
        "EPP a solicitar":EPP_soli,
        "Justificacion de reemplazo":justificacion,
        "EPP a reemplazar":EPP_cambio,
        "Comentarios":comentario,
        "Estado":Estado,
        "Ultima modificacion":" "
    }])
    df = pd.concat([df, new_order], ignore_index=True)
    df.to_csv(ruta, index=False)

# Botón para enviar la información 
if not name or not tipo_solicitud:
    st.error("Favor de no dejar espacios sin rellenar")
else:
    if st.button("Enviar", icon="📝", use_container_width=True):
        add_to_csv(date, name, tipo_solicitud, puesto_emp, ",".join(EPP_solicitado), justificacion, comentarios, epp_reemplazo)
        st.success("Solicitud enviada con éxito")
        st.warning("Vuelve a la página principal para ver el estado de tu solicitud")

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
















# def agregar_datos(fecha, nombre, tiposolicitud, puesto, EPP_soli="", justificacion="No reemplazo", comentario="Sin comentario", EPP_cambio=" ", Estado="En proceso"): # cspell: disable-line
#     cursor.execute('''INSERT INTO Solicitudes (Fecha, Nombre_usuario, Puesto, Tipo_solicitud, EPP_eleccion, Justificacion_reemplazo, Comentarios, Estado, EPP_cambio) # cspell: disable-line
#                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''', (fecha, nombre, puesto, tiposolicitud, EPP_soli, justificacion, comentario, Estado, EPP_cambio)) # cspell: disable-line
#     conn.commit()

# Llamar a la función para agregar datos solo si el formulario ha sido enviado

# # Cerrar la conexión
# conn.close()
