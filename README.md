# API Gestor de Gastos Compartidos

API REST para gestionar gastos compartidos entre amigos (tipo Splitwise Lite).

## Instalación

```bash
pip install -r requirements.txt
```

## Ejecutar

```bash
python run.py
```

O directamente con uvicorn:

```bash
uvicorn app.main:app --reload
```

La API estará disponible en: http://localhost:8000

Documentación interactiva: http://localhost:8000/docs

## Endpoints

- `POST /gastos` - Crear un nuevo gasto
- `GET /gastos` - Obtener todos los gastos y el cálculo de deudas
- `GET /gastos/{id}` - Obtener un gasto específico
- `PUT /gastos/{id}` - Actualizar un gasto
- `DELETE /gastos/{id}` - Eliminar un gasto
- `GET /resumen` - Obtener resumen de quién debe a quién
