"""Demo module for Toyota Car Service Application.

Módulo de demostración para la aplicación de servicio de autos Toyota.
"""

from toyota_service.models.vehicle import ServiceType
from toyota_service.services.service_manager import ServiceManager
from toyota_service.ui.display import (
    print_header,
    print_statistics,
    print_pending_services,
    print_vehicle_details,
    print_footer,
    print_vehicle_registered,
    print_service_scheduled,
    print_service_completed
)


def run_demo():
    """Run a demonstration of the Toyota Car Service system.
    
    Ejecuta una demostración del sistema de servicio de autos Toyota.
    """
    print_header()
    
    # Create service manager
    manager = ServiceManager()
    
    # Register vehicles
    print("Registrando vehículos de demostración...")
    
    vehicle1 = manager.register_vehicle(
        model="Corolla",
        year=2022,
        license_plate="ABC-123",
        owner_name="Carlos Rodriguez",
        owner_phone="555-1234",
        mileage=15000
    )
    print_vehicle_registered(vehicle1)
    
    vehicle2 = manager.register_vehicle(
        model="RAV4",
        year=2021,
        license_plate="XYZ-789",
        owner_name="Maria Garcia",
        owner_phone="555-5678",
        mileage=25000
    )
    print_vehicle_registered(vehicle2)
    
    vehicle3 = manager.register_vehicle(
        model="Camry",
        year=2023,
        license_plate="DEF-456",
        owner_name="Juan Perez",
        owner_phone="555-9012",
        mileage=8000
    )
    print_vehicle_registered(vehicle3)
    
    # Schedule services
    print("\nProgramando servicios...")
    
    service1 = manager.schedule_service(
        vehicle_id=vehicle1.vehicle_id,
        service_type=ServiceType.OIL_CHANGE,
        description="Cambio de aceite sintético 5W-30",
        cost=75.00,
        technician="Pedro Martinez"
    )
    print_service_scheduled(service1, vehicle1)
    
    service2 = manager.schedule_service(
        vehicle_id=vehicle1.vehicle_id,
        service_type=ServiceType.TIRE_ROTATION,
        description="Rotación de llantas y balanceo",
        cost=45.00,
        technician="Pedro Martinez"
    )
    print_service_scheduled(service2, vehicle1)
    
    service3 = manager.schedule_service(
        vehicle_id=vehicle2.vehicle_id,
        service_type=ServiceType.BRAKE_INSPECTION,
        description="Inspección de pastillas y discos de freno",
        cost=35.00,
        technician="Ana Lopez"
    )
    print_service_scheduled(service3, vehicle2)
    
    service4 = manager.schedule_service(
        vehicle_id=vehicle3.vehicle_id,
        service_type=ServiceType.SCHEDULED_MAINTENANCE,
        description="Mantenimiento de los 10,000 km",
        cost=150.00,
        technician="Roberto Sanchez"
    )
    print_service_scheduled(service4, vehicle3)
    
    # Complete some services
    print("\nCompletando servicios...")
    manager.complete_service(vehicle1.vehicle_id, service1.service_id)
    print_service_completed(service1, vehicle1)
    
    manager.complete_service(vehicle2.vehicle_id, service3.service_id)
    print_service_completed(service3, vehicle2)
    
    # Print statistics
    print_statistics(manager.get_statistics())
    
    # Print pending services
    print_pending_services(manager.get_all_pending_services())
    
    # Print vehicle details
    print_vehicle_details(manager.get_all_vehicles())
    
    # Print footer
    print_footer()
