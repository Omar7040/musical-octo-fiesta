"""Service Manager for Toyota Car Service operations."""

from typing import Dict, List, Optional
from datetime import datetime
from ..models.vehicle import Vehicle, ServiceRecord, ServiceType


class ServiceManager:
    """Manages Toyota vehicle service operations."""

    def __init__(self):
        """Initialize the service manager."""
        self._vehicles: Dict[str, Vehicle] = {}

    def register_vehicle(
        self,
        model: str,
        year: int,
        license_plate: str,
        vin: str = "",
        owner_name: str = "",
        owner_phone: str = "",
        owner_email: str = "",
        mileage: int = 0
    ) -> Vehicle:
        """Register a new Toyota vehicle in the system."""
        vehicle = Vehicle(
            model=model,
            year=year,
            license_plate=license_plate,
            vin=vin,
            owner_name=owner_name,
            owner_phone=owner_phone,
            owner_email=owner_email,
            mileage=mileage
        )
        self._vehicles[vehicle.vehicle_id] = vehicle
        return vehicle

    def get_vehicle(self, vehicle_id: str) -> Optional[Vehicle]:
        """Get a vehicle by its ID."""
        return self._vehicles.get(vehicle_id)

    def get_vehicle_by_plate(self, license_plate: str) -> Optional[Vehicle]:
        """Get a vehicle by its license plate."""
        for vehicle in self._vehicles.values():
            if vehicle.license_plate == license_plate:
                return vehicle
        return None

    def get_all_vehicles(self) -> List[Vehicle]:
        """Get all registered vehicles."""
        return list(self._vehicles.values())

    def remove_vehicle(self, vehicle_id: str) -> bool:
        """Remove a vehicle from the system."""
        if vehicle_id in self._vehicles:
            del self._vehicles[vehicle_id]
            return True
        return False

    def schedule_service(
        self,
        vehicle_id: str,
        service_type: ServiceType,
        description: str,
        cost: float,
        technician: str = "",
        notes: str = "",
        scheduled_date: Optional[datetime] = None
    ) -> Optional[ServiceRecord]:
        """Schedule a new service for a vehicle."""
        vehicle = self.get_vehicle(vehicle_id)
        if not vehicle:
            return None

        service = ServiceRecord(
            service_type=service_type,
            description=description,
            cost=cost,
            date=scheduled_date or datetime.now(),
            technician=technician,
            notes=notes
        )
        vehicle.add_service(service)
        return service

    def complete_service(
        self,
        vehicle_id: str,
        service_id: str
    ) -> bool:
        """Mark a service as completed."""
        vehicle = self.get_vehicle(vehicle_id)
        if not vehicle:
            return False

        for service in vehicle.service_history:
            if service.service_id == service_id:
                service.mark_completed()
                return True
        return False

    def get_pending_services(self, vehicle_id: str) -> List[ServiceRecord]:
        """Get all pending services for a vehicle."""
        vehicle = self.get_vehicle(vehicle_id)
        if not vehicle:
            return []
        return vehicle.get_pending_services()

    def get_all_pending_services(self) -> List[tuple]:
        """Get all pending services across all vehicles."""
        pending = []
        for vehicle in self._vehicles.values():
            for service in vehicle.get_pending_services():
                pending.append((vehicle, service))
        return pending

    def get_service_history(self, vehicle_id: str) -> List[ServiceRecord]:
        """Get complete service history for a vehicle."""
        vehicle = self.get_vehicle(vehicle_id)
        if not vehicle:
            return []
        return vehicle.service_history.copy()

    def search_vehicles(self, query: str) -> List[Vehicle]:
        """Search vehicles by model, owner name, or license plate."""
        query_lower = query.lower()
        results = []
        for vehicle in self._vehicles.values():
            if (query_lower in vehicle.model.lower() or
                query_lower in vehicle.owner_name.lower() or
                query_lower in vehicle.license_plate.lower()):
                results.append(vehicle)
        return results

    def get_statistics(self) -> dict:
        """Get service statistics."""
        total_vehicles = len(self._vehicles)
        total_services = sum(
            len(v.service_history) for v in self._vehicles.values()
        )
        pending_services = len(self.get_all_pending_services())
        total_revenue = sum(
            v.get_total_service_cost() for v in self._vehicles.values()
        )

        return {
            "total_vehicles": total_vehicles,
            "total_services": total_services,
            "pending_services": pending_services,
            "completed_services": total_services - pending_services,
            "total_revenue": total_revenue
        }
