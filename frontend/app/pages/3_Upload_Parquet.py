import streamlit as st
import requests
import os
import pandas as pd
from io import BytesIO

API_URL = os.getenv("API_URL", "http://api:8000")

st.title("📤 Upload Parquet - Zones")
st.write("Sube un archivo Parquet para agregar zonas a la base de datos.")

uploaded_file = st.file_uploader(
    "Selecciona un archivo Parquet",
    type=["parquet"]
)

if uploaded_file is not None:
    st.success(f"Archivo seleccionado: {uploaded_file.name}")
    
    # Preview de datos
    try:
        df = pd.read_parquet(BytesIO(uploaded_file.getvalue()))
        st.subheader("Vista previa de datos")
        st.dataframe(df.head())
        st.write(f"Total de filas: {len(df)}")
        st.write(f"Columnas disponibles: {list(df.columns)}")
    except Exception as e:
        st.error(f"Error al leer el archivo: {e}")

    if st.button("Agregar zonas"):
        try:
            df = pd.read_parquet(BytesIO(uploaded_file.getvalue()))
            zone_id_col = None
            borough_col = None
            zone_name_col = None
            service_zone_col = None
            
            # Pasar columnas
            for col in df.columns:
                col_lower = col.lower()
                if 'locationid' in col_lower or 'zone_id' in col_lower or 'id' in col_lower:
                    zone_id_col = col
                elif 'borough' in col_lower:
                    borough_col = col
                elif 'zone' in col_lower and 'name' in col_lower:
                    zone_name_col = col
                elif 'service' in col_lower and 'zone' in col_lower:
                    service_zone_col = col
            
            if zone_id_col is None:
                st.error("No se encontró una columna de ID de zona (LocationID, zone_id, o id)")
            
            created_count = 0
            error_count = 0
            results = []
            
            unique_zones = df[zone_id_col].unique()
            
            for zone_id in unique_zones:
                try:
                    # Para otra info:
                    row = df[df[zone_id_col] == zone_id].iloc[0]
                    
                    zone_payload = {
                        "id": int(zone_id),
                        "borough": str(row.get(borough_col, f"Borough_{zone_id}")),
                        "zone_name": str(row.get(zone_name_col, f"Zone_{zone_id}")),
                        "service_zone": str(row.get(service_zone_col, f"Service_{zone_id}")),
                        "active": True
                    }
                    
                    # Agregar zona via API
                    response = requests.post(
                        f"{API_URL}/zones",
                        json=zone_payload
                    )
                    
                    if response.status_code == 201:
                        created_count += 1
                        results.append({
                            "zone_id": zone_id,
                            "status": "created",
                            "zone_name": zone_payload["zone_name"]
                        })
                    elif response.status_code == 400 and "ya existe" in response.text:
                        # skip
                        results.append({
                            "zone_id": zone_id,
                            "status": "exists",
                            "zone_name": zone_payload["zone_name"]
                        })
                    else:
                        error_count += 1
                        results.append({
                            "zone_id": zone_id,
                            "status": "error",
                            "error": response.text
                        })
                        
                except Exception as e:
                    error_count += 1
                    results.append({
                        "zone_id": zone_id,
                        "status": "error",
                        "error": str(e)
                    })
            
            # Resultados
            st.success(f"Procesamiento completado: {created_count} creadas, {error_count} errores")
            
            if results:
                st.subheader("Detalles del procesamiento")
                results_df = pd.DataFrame(results)
                st.dataframe(results_df)
            
            summary = {
                "total_unique_zones": len(unique_zones),
                "created": created_count,
                "errors": error_count,
                "processed_file": uploaded_file.name
            }
            
            st.subheader("Resumen del procesamiento")
            st.json(summary)

        except Exception as e:
            st.error(f"No se pudo procesar el archivo: {e}")