import streamlit as st
import requests
import os

API_URL = os.getenv("API_URL", "http://api:8000")

st.title("📍 Zones")
st.write("Gestión de zonas: listar, filtrar, crear, editar y eliminar.")


st.subheader("Filtros")

filter_active = st.selectbox(
    "Estado",
    ["Todos", "Activos", "Inactivos"]
)

filter_borough = st.text_input("Borough", key="filter_borough")


st.subheader("Ver Zones")

if st.button("Cargar Zones"):
    try:
        params = {}

        if filter_active == "Activos":
            params["active"] = True
        elif filter_active == "Inactivos":
            params["active"] = False

        if filter_borough:
            params["borough"] = filter_borough

        response = requests.get(f"{API_URL}/zones", params=params)

        if response.status_code == 200:
            zones = response.json()
            if zones:
                st.table(zones)
            else:
                st.info("No hay zones que coincidan con los filtros.")
        else:
            st.error(response.text)

    except Exception:
        st.error("No se pudo conectar con el backend.")


st.divider()
st.subheader("Crear nueva Zone")

zone_id = st.number_input(
    "ID (TLC LocationID)",
    min_value=1,
    step=1
)
borough = st.text_input("Borough",key="create_borough")
zone_name = st.text_input("Zone Name")
service_zone = st.text_input("Service Zone")

if st.button("Crear Zone"):
    payload = {
        "id": int(zone_id),
        "borough": borough,
        "zone_name": zone_name,
        "service_zone": service_zone,
        "active": True
    }

    try:
        response = requests.post(f"{API_URL}/zones", json=payload)

        if response.status_code == 201:
            st.success("✅ Zone creada correctamente")
        else:
            st.error(response.text)

    except Exception:
        st.error("Error conectando con el backend.")


st.divider()
st.subheader("Editar Zone")

edit_id = st.number_input(
    "ID de la Zone a editar",
    min_value=1,
    step=1,
    key="edit_zone_id"
)

edit_borough = st.text_input("Nuevo Borough")
edit_zone_name = st.text_input("Nuevo Zone Name")
edit_service_zone = st.text_input("Nuevo Service Zone")
edit_active = st.checkbox("Activa", value=True)

if st.button("Actualizar Zone"):
    payload = {
        "borough": edit_borough,
        "zone_name": edit_zone_name,
        "service_zone": edit_service_zone,
        "active": edit_active
    }

    try:
        response = requests.put(
            f"{API_URL}/zones/{int(edit_id)}",
            json=payload
        )

        if response.status_code == 200:
            st.success("✏️ Zone actualizada correctamente")
        else:
            st.error(response.text)

    except Exception:
        st.error("Error conectando con el backend.")


st.divider()
st.subheader("Eliminar Zone")

delete_id = st.number_input(
    "ID de la Zone a eliminar",
    min_value=1,
    step=1,
    key="delete_zone_id"
)

if st.button("Eliminar Zone"):
    try:
        response = requests.delete(
            f"{API_URL}/zones/{int(delete_id)}"
        )

        if response.status_code == 204:
            st.success("🗑️ Zone eliminada correctamente")
        else:
            st.error(response.text)

    except Exception:
        st.error("Error conectando con el backend.")
