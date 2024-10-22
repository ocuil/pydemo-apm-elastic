import streamlit as st
from elasticapm import Client
import time
import psutil

# Configuración del agente APM
if 'apm_client' not in st.session_state:
    st.session_state.apm_client = Client({
        'DEBUG': True,
        'SERVICE_NAME': '',
        'SECRET_TOKEN': '',
        'SERVER_URL': '',
        'SERVICE_VERSION': '0.1',
    })

apm_client = st.session_state.apm_client  # Evita crear múltiples instancias

st.title('Prueba del APM Agent con Streamlit')

# Simulación de una operación sencilla
st.write("Simulando operaciones para el APM...")

# Simular una tarea (usando captura de mensaje o excepción)
if st.button('Simular tarea'):
    try:
        time.sleep(2)  # Simulación de tarea de 2 segundos
        apm_client.capture_message("Tarea larga completada")
        st.success("¡Tarea completada!")
    except Exception as e:
        apm_client.capture_exception()
        st.error("Hubo un error durante la simulación de tarea.")

# Manejo de excepciones y captura de errores en APM
if st.button('Causa un error'):
    try:
        1 / 0
    except Exception as e:
        apm_client.capture_exception()  # Captura el error en APM
        st.error("¡Oops! Se ha capturado un error.")

st.write("La aplicación está monitoreada por Elastic APM.")

# Finaliza la transacción de APM (solo como referencia, ya que Streamlit maneja flujo continuo)
apm_client.end_transaction("streamlit_request", "success")
