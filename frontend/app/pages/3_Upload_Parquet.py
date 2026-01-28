import streamlit as st
import requests
import os

API_URL = os.getenv("API_URL", "http://api:8000")

st.title("📤 Upload Parquet")
st.write("Sube un archivo Parquet para procesarlo en el backend.")


uploaded_file = st.file_uploader(
    "Selecciona un archivo Parquet",
    type=["parquet"]
)

if uploaded_file is not None:
    st.success(f"Archivo seleccionado: {uploaded_file.name}")

    if st.button("Subir archivo"):
        try:
            files = {
                "file": (
                    uploaded_file.name,
                    uploaded_file.getvalue(),
                    "application/octet-stream"
                )
            }

            response = requests.post(
                f"{API_URL}/upload",
                files=files
            )

            if response.status_code == 200:
                st.success("Archivo procesado correctamente")

                
                st.subheader("Resumen del archivo")
                st.json(response.json())

            else:
                st.error(response.text)

        except Exception:
            st.error("No se pudo conectar con el backend.")
