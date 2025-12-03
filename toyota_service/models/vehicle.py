"""Vehicle and Service Record models for Toyota Car Service."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional
from enum import Enum
import uuid


class ServiceType(Enum):
    """Types of services available for Toyota vehicles."""
    OIL_CHANGE = "Cambio de aceite"
    TIRE_ROTATION = "Rotación de llantas"
    BRAKE_INSPECTION = "Inspección de frenos"
    ENGINE_TUNE_UP = "Afinación de motor"
    TRANSMISSION_SERVICE = "Servicio de transmisión"
    BATTERY_CHECK = "Revisión de batería"
    AIR_FILTER_REPLACEMENT = "Reemplazo de filtro de aire"
    GENERAL_INSPECTION = "Inspección general"
    SCHEDULED_MAINTENANCE = "Mantenimiento programado"


@dataclass
class ServiceRecord:
    """Represents a service record for a Toyota vehicle."""
    service_type: ServiceType
    description: str
    cost: float
    date: datetime = field(default_factory=datetime.now)
    service_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    technician: str = ""
    notes: str = ""
    completed: bool = False

    def mark_completed(self) -> None:
        """Mark this service as completed."""
        self.completed = True

    def to_dict(self) -> dict:
        """Convert service record to dictionary."""
        return {
            "service_id": self.service_id,
            "service_type": self.service_type.value,
            "description": self.description,
            "cost": self.cost,
            "date": self.date.isoformat(),
            "technician": self.technician,
            "notes": self.notes,
            "completed": self.completed
        }


@dataclass
class Vehicle:
    """Represents a Toyota vehicle in the service system."""
    model: str
    year: int
    license_plate: str
    vin: str = ""
    owner_name: str = ""
    owner_phone: str = ""
    owner_email: str = ""
    mileage: int = 0
    vehicle_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    service_history: List[ServiceRecord] = field(default_factory=list)
    registration_date: datetime = field(default_factory=datetime.now)

    def add_service(self, service: ServiceRecord) -> None:
        """Add a service record to the vehicle's history."""
        self.service_history.append(service)

    def get_pending_services(self) -> List[ServiceRecord]:
        """Get all pending (incomplete) services."""
        return [s for s in self.service_history if not s.completed]

    def get_completed_services(self) -> List[ServiceRecord]:
        """Get all completed services."""
        return [s for s in self.service_history if s.completed]

    def get_total_service_cost(self) -> float:
        """Calculate total cost of all services."""
        return sum(s.cost for s in self.service_history)

    def update_mileage(self, new_mileage: int) -> None:
        """Update the vehicle's mileage."""
        if new_mileage >= self.mileage:
            self.mileage = new_mileage
        else:
            raise ValueError("El nuevo kilometraje no puede ser menor al actual")

    def to_dict(self) -> dict:
        """Convert vehicle to dictionary."""
        return {
            "vehicle_id": self.vehicle_id,
            "model": self.model,
            "year": self.year,
            "license_plate": self.license_plate,
            "vin": self.vin,
            "owner_name": self.owner_name,
            "owner_phone": self.owner_phone,
            "owner_email": self.owner_email,
            "mileage": self.mileage,
            "registration_date": self.registration_date.isoformat(),
            "service_history": [s.to_dict() for s in self.service_history]
        }


# Popular Toyota models available for service
TOYOTA_MODELS = [
    "Corolla",
    "Camry",
    "RAV4",
    "Highlander",
    "Tacoma",
    "Tundra",
    "4Runner",
    "Prius",
    "Yaris",
    "Supra",
    "Land Cruiser",
    "Sienna",
    "Avalon",
    "C-HR",
    "Venza"
]
