import streamlit as st
import requests
import os

API_URL = os.getenv("API_URL", "http://api:8000")

st.title("Demand Prediction Service")
st.write(
    "Sistema de predicción de demanda, usando FastAPI en backend "
    "y Streamlit en frontend."
)
st.sidebar.success("Usa el menú para navegar entre las páginas")
st.divider()

if st.button("¿El sistema funciona?"):
    try:
        response = requests.get(f"{API_URL}/health")
        if response.status_code == 200:
            st.success("✅ Backend funcionando correctamente")
        else:
            st.error("❌ Backend respondió con error")
    except Exception as e:
        st.error("❌ No se pudo conectar con el backend")

