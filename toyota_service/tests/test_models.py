"""Tests for the Vehicle and ServiceRecord models."""

import unittest
from datetime import datetime
from toyota_service.models.vehicle import Vehicle, ServiceRecord, ServiceType


class TestServiceRecord(unittest.TestCase):
    """Test cases for ServiceRecord model."""

    def test_create_service_record(self):
        """Test creating a service record."""
        service = ServiceRecord(
            service_type=ServiceType.OIL_CHANGE,
            description="Oil change for 5000km service",
            cost=50.00
        )
        self.assertEqual(service.service_type, ServiceType.OIL_CHANGE)
        self.assertEqual(service.description, "Oil change for 5000km service")
        self.assertEqual(service.cost, 50.00)
        self.assertFalse(service.completed)
        self.assertIsNotNone(service.service_id)

    def test_mark_completed(self):
        """Test marking a service as completed."""
        service = ServiceRecord(
            service_type=ServiceType.BRAKE_INSPECTION,
            description="Brake pad inspection",
            cost=30.00
        )
        self.assertFalse(service.completed)
        service.mark_completed()
        self.assertTrue(service.completed)

    def test_to_dict(self):
        """Test converting service record to dictionary."""
        service = ServiceRecord(
            service_type=ServiceType.TIRE_ROTATION,
            description="Tire rotation",
            cost=25.00,
            technician="Juan"
        )
        result = service.to_dict()
        self.assertIn("service_id", result)
        self.assertEqual(result["service_type"], "Rotación de llantas")
        self.assertEqual(result["description"], "Tire rotation")
        self.assertEqual(result["cost"], 25.00)
        self.assertEqual(result["technician"], "Juan")


class TestVehicle(unittest.TestCase):
    """Test cases for Vehicle model."""

    def setUp(self):
        """Set up test fixtures."""
        self.vehicle = Vehicle(
            model="Corolla",
            year=2022,
            license_plate="ABC-123",
            owner_name="Carlos Rodriguez"
        )

    def test_create_vehicle(self):
        """Test creating a vehicle."""
        self.assertEqual(self.vehicle.model, "Corolla")
        self.assertEqual(self.vehicle.year, 2022)
        self.assertEqual(self.vehicle.license_plate, "ABC-123")
        self.assertEqual(self.vehicle.owner_name, "Carlos Rodriguez")
        self.assertIsNotNone(self.vehicle.vehicle_id)

    def test_add_service(self):
        """Test adding a service to a vehicle."""
        service = ServiceRecord(
            service_type=ServiceType.OIL_CHANGE,
            description="Regular oil change",
            cost=45.00
        )
        self.vehicle.add_service(service)
        self.assertEqual(len(self.vehicle.service_history), 1)
        self.assertEqual(self.vehicle.service_history[0], service)

    def test_get_pending_services(self):
        """Test getting pending services."""
        service1 = ServiceRecord(
            service_type=ServiceType.OIL_CHANGE,
            description="Oil change",
            cost=45.00
        )
        service2 = ServiceRecord(
            service_type=ServiceType.BRAKE_INSPECTION,
            description="Brake check",
            cost=30.00
        )
        service2.mark_completed()

        self.vehicle.add_service(service1)
        self.vehicle.add_service(service2)

        pending = self.vehicle.get_pending_services()
        self.assertEqual(len(pending), 1)
        self.assertEqual(pending[0], service1)

    def test_get_completed_services(self):
        """Test getting completed services."""
        service1 = ServiceRecord(
            service_type=ServiceType.OIL_CHANGE,
            description="Oil change",
            cost=45.00
        )
        service2 = ServiceRecord(
            service_type=ServiceType.BRAKE_INSPECTION,
            description="Brake check",
            cost=30.00
        )
        service2.mark_completed()

        self.vehicle.add_service(service1)
        self.vehicle.add_service(service2)

        completed = self.vehicle.get_completed_services()
        self.assertEqual(len(completed), 1)
        self.assertEqual(completed[0], service2)

    def test_get_total_service_cost(self):
        """Test calculating total service cost."""
        service1 = ServiceRecord(
            service_type=ServiceType.OIL_CHANGE,
            description="Oil change",
            cost=45.00
        )
        service2 = ServiceRecord(
            service_type=ServiceType.BRAKE_INSPECTION,
            description="Brake check",
            cost=30.00
        )

        self.vehicle.add_service(service1)
        self.vehicle.add_service(service2)

        total = self.vehicle.get_total_service_cost()
        self.assertEqual(total, 75.00)

    def test_update_mileage(self):
        """Test updating vehicle mileage."""
        self.vehicle.update_mileage(10000)
        self.assertEqual(self.vehicle.mileage, 10000)

        self.vehicle.update_mileage(15000)
        self.assertEqual(self.vehicle.mileage, 15000)

    def test_update_mileage_invalid(self):
        """Test updating mileage with lower value raises error."""
        self.vehicle.update_mileage(10000)
        with self.assertRaises(ValueError):
            self.vehicle.update_mileage(5000)

    def test_to_dict(self):
        """Test converting vehicle to dictionary."""
        result = self.vehicle.to_dict()
        self.assertIn("vehicle_id", result)
        self.assertEqual(result["model"], "Corolla")
        self.assertEqual(result["year"], 2022)
        self.assertEqual(result["license_plate"], "ABC-123")
        self.assertEqual(result["owner_name"], "Carlos Rodriguez")
        self.assertIsInstance(result["service_history"], list)


if __name__ == "__main__":
    unittest.main()
