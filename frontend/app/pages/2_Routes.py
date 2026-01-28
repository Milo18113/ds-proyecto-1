import streamlit as st
import requests
import os

API_URL = os.getenv("API_URL", "http://api:8000")

st.title("🛣️ Routes")
st.write("Gestión completa de rutas (CRUD).")

# =========================
# CARGAR ZONES
# =========================
def get_zones():
    try:
        r = requests.get(f"{API_URL}/zones")
        if r.status_code == 200:
            return r.json()
    except Exception:
        pass
    return []

zones = get_zones()

zone_options = {
    f"{z['id']} - {z['zone_name']} ({z['borough']})": z["id"]
    for z in zones
}

# =========================
# FILTROS
# =========================
st.subheader("Filtros")

filter_active = st.selectbox(
    "Estado",
    ["Todos", "Activas", "Inactivas"]
)

filter_pickup = st.selectbox(
    "Pickup Zone",
    ["Todas"] + list(zone_options.keys())
)

filter_dropoff = st.selectbox(
    "Dropoff Zone",
    ["Todas"] + list(zone_options.keys())
)

# =========================
# LISTAR ROUTES
# =========================
st.subheader("Ver Routes")

if st.button("Cargar Routes"):
    params = {}

    if filter_active == "Activas":
        params["active"] = True
    elif filter_active == "Inactivas":
        params["active"] = False

    if filter_pickup != "Todas":
        params["pickup_zone_id"] = zone_options[filter_pickup]

    if filter_dropoff != "Todas":
        params["dropoff_zone_id"] = zone_options[filter_dropoff]

    try:
        r = requests.get(f"{API_URL}/routes", params=params)

        if r.status_code == 200:
            routes = r.json()
            if routes:
                st.table(routes)
            else:
                st.info("No hay rutas que coincidan con los filtros.")
        else:
            st.error(r.text)

    except Exception:
        st.error("No se pudo conectar con el backend.")

# =========================
# GET ROUTE POR ID
# =========================
st.divider()
st.subheader("Buscar Route por ID")

get_id = st.number_input(
    "ID de la Route",
    min_value=1,
    step=1,
    key="get_route"
)

if st.button("Buscar Route"):
    try:
        r = requests.get(f"{API_URL}/routes/{int(get_id)}")

        if r.status_code == 200:
            st.json(r.json())
        else:
            st.error(r.text)

    except Exception:
        st.error("Error conectando con el backend.")

# =========================
# CREAR ROUTE
# =========================
st.divider()
st.subheader("Crear Route")

route_id = st.number_input(
    "ID de la Route",
    min_value=1,
    step=1,
    key="create_id"
)

route_name = st.text_input("Nombre de la Route")

if not zone_options:
    st.warning("Primero crea zones.")
else:
    pickup_label = st.selectbox(
        "Pickup Zone",
        list(zone_options.keys()),
        key="create_pickup"
    )

    dropoff_label = st.selectbox(
        "Dropoff Zone",
        list(zone_options.keys()),
        key="create_dropoff"
    )

    if st.button("Crear Route"):
        payload = {
            "id": int(route_id),
            "name": route_name,
            "pickup_zone_id": zone_options[pickup_label],
            "dropoff_zone_id": zone_options[dropoff_label],
            "active": True
        }

        try:
            r = requests.post(f"{API_URL}/routes", json=payload)

            if r.status_code == 200:
                st.success("✅ Route creada correctamente")
            else:
                st.error(r.text)

        except Exception:
            st.error("Error conectando con el backend.")

# =========================
# EDITAR ROUTE
# =========================
st.divider()
st.subheader("Editar Route")

edit_id = st.number_input(
    "ID de la Route a editar",
    min_value=1,
    step=1,
    key="edit_route"
)

edit_name = st.text_input("Nuevo nombre")

edit_active = st.checkbox("Activa", value=True)

edit_pickup = st.selectbox(
    "Nuevo Pickup Zone",
    list(zone_options.keys()),
    key="edit_pickup"
)

edit_dropoff = st.selectbox(
    "Nuevo Dropoff Zone",
    list(zone_options.keys()),
    key="edit_dropoff"
)

if st.button("Actualizar Route"):
    payload = {
        "name": edit_name,
        "pickup_zone_id": zone_options[edit_pickup],
        "dropoff_zone_id": zone_options[edit_dropoff],
        "active": edit_active
    }

    try:
        r = requests.put(
            f"{API_URL}/routes/{int(edit_id)}",
            json=payload
        )

        if r.status_code == 200:
            st.success("✏️ Route actualizada")
        else:
            st.error(r.text)

    except Exception:
        st.error("Error conectando con el backend.")

# =========================
# ELIMINAR ROUTE
# =========================
st.divider()
st.subheader("Eliminar Route")

delete_id = st.number_input(
    "ID de la Route a eliminar",
    min_value=1,
    step=1,
    key="delete_route"
)

if st.button("Eliminar Route"):
    try:
        r = requests.delete(f"{API_URL}/routes/{int(delete_id)}")

        if r.status_code == 204:
            st.success("🗑️ Route eliminada correctamente")
        else:
            st.error(r.text)

    except Exception:
        st.error("Error conectando con el backend.")
