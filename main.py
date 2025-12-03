#!/usr/bin/env python3
"""
Toyota Car Service Application - Main Entry Point

Sistema de gestión de servicios para autos Toyota.
Este aplicación permite registrar vehículos, programar servicios,
y administrar el historial de mantenimiento de autos Toyota.
"""

from toyota_service.models.vehicle import Vehicle, ServiceRecord, ServiceType, TOYOTA_MODELS
from toyota_service.services.service_manager import ServiceManager


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


def demo():
    """Run a demonstration of the Toyota Car Service system."""
    print_header()
    
    # Create service manager
    manager = ServiceManager()
    
    # Register some vehicles
    print("Registrando vehículos de demostración...")
    
    vehicle1 = manager.register_vehicle(
        model="Corolla",
        year=2022,
        license_plate="ABC-123",
        owner_name="Carlos Rodriguez",
        owner_phone="555-1234",
        mileage=15000
    )
    print(f"  ✓ Registrado: {vehicle1.model} {vehicle1.year} - {vehicle1.license_plate}")
    
    vehicle2 = manager.register_vehicle(
        model="RAV4",
        year=2021,
        license_plate="XYZ-789",
        owner_name="Maria Garcia",
        owner_phone="555-5678",
        mileage=25000
    )
    print(f"  ✓ Registrado: {vehicle2.model} {vehicle2.year} - {vehicle2.license_plate}")
    
    vehicle3 = manager.register_vehicle(
        model="Camry",
        year=2023,
        license_plate="DEF-456",
        owner_name="Juan Perez",
        owner_phone="555-9012",
        mileage=8000
    )
    print(f"  ✓ Registrado: {vehicle3.model} {vehicle3.year} - {vehicle3.license_plate}")
    
    # Schedule some services
    print("\nProgramando servicios...")
    
    service1 = manager.schedule_service(
        vehicle_id=vehicle1.vehicle_id,
        service_type=ServiceType.OIL_CHANGE,
        description="Cambio de aceite sintético 5W-30",
        cost=75.00,
        technician="Pedro Martinez"
    )
    print(f"  ✓ Servicio programado: {service1.service_type.value} para {vehicle1.model}")
    
    service2 = manager.schedule_service(
        vehicle_id=vehicle1.vehicle_id,
        service_type=ServiceType.TIRE_ROTATION,
        description="Rotación de llantas y balanceo",
        cost=45.00,
        technician="Pedro Martinez"
    )
    print(f"  ✓ Servicio programado: {service2.service_type.value} para {vehicle1.model}")
    
    service3 = manager.schedule_service(
        vehicle_id=vehicle2.vehicle_id,
        service_type=ServiceType.BRAKE_INSPECTION,
        description="Inspección de pastillas y discos de freno",
        cost=35.00,
        technician="Ana Lopez"
    )
    print(f"  ✓ Servicio programado: {service3.service_type.value} para {vehicle2.model}")
    
    service4 = manager.schedule_service(
        vehicle_id=vehicle3.vehicle_id,
        service_type=ServiceType.SCHEDULED_MAINTENANCE,
        description="Mantenimiento de los 10,000 km",
        cost=150.00,
        technician="Roberto Sanchez"
    )
    print(f"  ✓ Servicio programado: {service4.service_type.value} para {vehicle3.model}")
    
    # Complete some services
    print("\nCompletando servicios...")
    manager.complete_service(vehicle1.vehicle_id, service1.service_id)
    print(f"  ✓ Completado: {service1.service_type.value} para {vehicle1.model}")
    
    manager.complete_service(vehicle2.vehicle_id, service3.service_id)
    print(f"  ✓ Completado: {service3.service_type.value} para {vehicle2.model}")
    
    # Print statistics
    print("\n" + "=" * 60)
    print("                    ESTADÍSTICAS")
    print("=" * 60)
    stats = manager.get_statistics()
    print(f"  Total de vehículos registrados: {stats['total_vehicles']}")
    print(f"  Total de servicios: {stats['total_services']}")
    print(f"  Servicios pendientes: {stats['pending_services']}")
    print(f"  Servicios completados: {stats['completed_services']}")
    print(f"  Ingresos totales: ${stats['total_revenue']:.2f}")
    
    # Print pending services
    print("\n" + "=" * 60)
    print("                 SERVICIOS PENDIENTES")
    print("=" * 60)
    all_pending = manager.get_all_pending_services()
    for vehicle, service in all_pending:
        print(f"  • {vehicle.model} ({vehicle.license_plate})")
        print(f"    - {service.service_type.value}: {service.description}")
        print(f"    - Costo: ${service.cost:.2f}")
        print()
    
    # Print vehicle details
    print("=" * 60)
    print("              DETALLE DE VEHÍCULOS")
    print("=" * 60)
    for vehicle in manager.get_all_vehicles():
        print(f"\n  {vehicle.model} {vehicle.year}")
        print(f"  Placa: {vehicle.license_plate}")
        print(f"  Propietario: {vehicle.owner_name}")
        print(f"  Kilometraje: {vehicle.mileage:,} km")
        print(f"  Total servicios: {len(vehicle.service_history)}")
        print(f"  Costo total: ${vehicle.get_total_service_cost():.2f}")
    
    print("\n" + "=" * 60)
    print("     ¡Gracias por usar Toyota Car Service!")
    print("=" * 60)


if __name__ == "__main__":
    demo()
