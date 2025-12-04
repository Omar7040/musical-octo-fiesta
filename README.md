# Toyota Car Service Application

Sistema de gestión de servicios para autos Toyota.

## Descripción

Esta aplicación permite administrar el servicio de mantenimiento de vehículos Toyota. Incluye funcionalidades para:

- **Registro de vehículos**: Registra autos Toyota con información del propietario
- **Programación de servicios**: Programa diferentes tipos de mantenimiento
- **Historial de servicios**: Mantiene un registro completo de todos los servicios realizados
- **Estadísticas**: Visualiza estadísticas del taller de servicios

## Estructura del Proyecto

```
toyota_service/
├── __init__.py
├── models/
│   ├── __init__.py
│   └── vehicle.py          # Modelos de Vehicle y ServiceRecord
├── services/
│   ├── __init__.py
│   └── service_manager.py  # Lógica de gestión de servicios
└── tests/
    ├── __init__.py
    ├── test_models.py
    └── test_service_manager.py
main.py                      # Punto de entrada de la aplicación
```

## Tipos de Servicio Disponibles

- Cambio de aceite
- Rotación de llantas
- Inspección de frenos
- Afinación de motor
- Servicio de transmisión
- Revisión de batería
- Reemplazo de filtro de aire
- Inspección general
- Mantenimiento programado

## Modelos Toyota Soportados

Corolla, Camry, RAV4, Highlander, Tacoma, Tundra, 4Runner, Prius, Yaris, Supra, Land Cruiser, Sienna, Avalon, C-HR, Venza

## Instalación

```bash
# Clonar el repositorio
git clone https://github.com/Omar7040/musical-octo-fiesta.git
cd musical-octo-fiesta

# No se requieren dependencias externas
# La aplicación usa solo la biblioteca estándar de Python
```

## Uso

### Ejecutar la demostración

```bash
python main.py
```

### Ejecutar las pruebas

```bash
python -m pytest toyota_service/tests/ -v
# o
python -m unittest discover -s toyota_service/tests -v
```

### Uso como biblioteca

```python
from toyota_service.services import ServiceManager
from toyota_service.models import ServiceType

# Crear un administrador de servicios
manager = ServiceManager()

# Registrar un vehículo
vehicle = manager.register_vehicle(
    model="Corolla",
    year=2022,
    license_plate="ABC-123",
    owner_name="Juan Perez",
    mileage=15000
)

# Programar un servicio
service = manager.schedule_service(
    vehicle_id=vehicle.vehicle_id,
    service_type=ServiceType.OIL_CHANGE,
    description="Cambio de aceite sintético",
    cost=75.00,
    technician="Pedro Martinez"
)

# Completar el servicio
manager.complete_service(vehicle.vehicle_id, service.service_id)

# Ver estadísticas
stats = manager.get_statistics()
print(f"Total de vehículos: {stats['total_vehicles']}")
```

## Requisitos

- Python 3.7 o superior

## Licencia

MIT License