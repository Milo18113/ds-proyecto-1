# Demand Prediction Service – PSet #1

## Descripción
Este proyecto implementa una arquitectura básica de servicios para el PSet #1 del curso de Diseño de Sistemas de la Universidad San Francisco de Quito.
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