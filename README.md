# Demand Prediction Service – PSet #1
Desarrollado por Eduardo Cedeño, Jorge Marcillo, Pablo Galarza, Emilio Puga

## Descripción
Este proyecto implementa una arquitectura básica de servicios para el PSet #1 del curso de Diseño de Sistemas de la Universidad San Francisco de Quito.  
Permite realizar operaciones de creación, modificación y eliminación de zonas y rutas mediante una interfaz de usuario, así como importar bases de datos a través de archivos Parquet.   
Incluye:
- Backend en FastAPI
- Frontend en Streamlit
- Contenerización con Docker
- Orquestación con Docker Compose

## Arquitectura
- `backend/`: API REST con FastAPI
- `frontend/`: Interfaz de usuario con Streamlit
- `docker-compose.yml`: orquesta los servicios
- `docs/`: documentación del proyecto

## Cómo correr el proyecto (Docker)
Requisitos:
- Docker Desktop
- Docker Compose

Desde la raíz del proyecto:

```bash
docker compose up --build
```

## Servicios disponibles:
Backend: http://localhost:8000
Health check: http://localhost:8000/health
Frontend: http://localhost:8501

## Para detener la ejecución:

```bash
Ctrl + C   # (2 veces)
```