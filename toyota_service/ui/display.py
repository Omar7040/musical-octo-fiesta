"""Display functions for Toyota Car Service Application.

Funciones de visualización para la aplicación de servicio de autos Toyota.
"""

from typing import List, Tuple
from toyota_service.models.vehicle import Vehicle, ServiceRecord, ServiceType, TOYOTA_MODELS


def print_header():
    """Print the application header."""
    print("=" * 60)
    print("       TOYOTA CAR SERVICE - Sistema de Servicios")
    print("=" * 60)
    print()


def print_menu():
    """Print the main menu options."""
    print("\n--- MENÚ PRINCIPAL ---")
    print("1. Registrar nuevo vehículo")
    print("2. Ver todos los vehículos")
    print("3. Buscar vehículo")
    print("4. Programar servicio")
    print("5. Completar servicio")
    print("6. Ver historial de servicios")
    print("7. Ver estadísticas")
    print("8. Salir")
    print()


def print_service_types():
    """Print available service types."""
    print("\nTipos de servicio disponibles:")
    for i, stype in enumerate(ServiceType, 1):
        print(f"  {i}. {stype.value}")
    print()


def print_toyota_models():
    """Print available Toyota models."""
    print("\nModelos Toyota disponibles:")
    for i, model in enumerate(TOYOTA_MODELS, 1):
        print(f"  {i}. {model}")
    print()


def print_statistics(stats: dict):
    """Print service statistics.
    
    Args:
        stats: Dictionary containing service statistics.
    """
    print("\n" + "=" * 60)
    print("                    ESTADÍSTICAS")
    print("=" * 60)
    print(f"  Total de vehículos registrados: {stats['total_vehicles']}")
    print(f"  Total de servicios: {stats['total_services']}")
    print(f"  Servicios pendientes: {stats['pending_services']}")
    print(f"  Servicios completados: {stats['completed_services']}")
    print(f"  Ingresos totales: ${stats['total_revenue']:.2f}")


def print_pending_services(pending_services: List[Tuple[Vehicle, ServiceRecord]]):
    """Print all pending services.
    
    Args:
        pending_services: List of tuples containing (vehicle, service) pairs.
    """
    print("\n" + "=" * 60)
    print("                 SERVICIOS PENDIENTES")
    print("=" * 60)
    for vehicle, service in pending_services:
        print(f"  • {vehicle.model} ({vehicle.license_plate})")
        print(f"    - {service.service_type.value}: {service.description}")
        print(f"    - Costo: ${service.cost:.2f}")
        print()


def print_vehicle_details(vehicles: List[Vehicle]):
    """Print details for all vehicles.
    
    Args:
        vehicles: List of vehicles to display.
    """
    print("=" * 60)
    print("              DETALLE DE VEHÍCULOS")
    print("=" * 60)
    for vehicle in vehicles:
        print(f"\n  {vehicle.model} {vehicle.year}")
        print(f"  Placa: {vehicle.license_plate}")
        print(f"  Propietario: {vehicle.owner_name}")
        print(f"  Kilometraje: {vehicle.mileage:,} km")
        print(f"  Total servicios: {len(vehicle.service_history)}")
        print(f"  Costo total: ${vehicle.get_total_service_cost():.2f}")


def print_footer():
    """Print the application footer."""
    print("\n" + "=" * 60)
    print("     ¡Gracias por usar Toyota Car Service!")
    print("=" * 60)


def print_vehicle_registered(vehicle: Vehicle):
    """Print confirmation of vehicle registration.
    
    Args:
        vehicle: The registered vehicle.
    """
    print(f"  ✓ Registrado: {vehicle.model} {vehicle.year} - {vehicle.license_plate}")


def print_service_scheduled(service: ServiceRecord, vehicle: Vehicle):
    """Print confirmation of service scheduling.
    
    Args:
        service: The scheduled service.
        vehicle: The vehicle for the service.
    """
    print(f"  ✓ Servicio programado: {service.service_type.value} para {vehicle.model}")


def print_service_completed(service: ServiceRecord, vehicle: Vehicle):
    """Print confirmation of service completion.
    
    Args:
        service: The completed service.
        vehicle: The vehicle for the service.
    """
    print(f"  ✓ Completado: {service.service_type.value} para {vehicle.model}")
