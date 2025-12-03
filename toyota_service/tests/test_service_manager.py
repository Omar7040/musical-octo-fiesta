"""Tests for the ServiceManager."""

import unittest
from toyota_service.services.service_manager import ServiceManager
from toyota_service.models.vehicle import ServiceType


class TestServiceManager(unittest.TestCase):
    """Test cases for ServiceManager."""

    def setUp(self):
        """Set up test fixtures."""
        self.manager = ServiceManager()

    def test_register_vehicle(self):
        """Test registering a new vehicle."""
        vehicle = self.manager.register_vehicle(
            model="Camry",
            year=2023,
            license_plate="XYZ-789",
            owner_name="Maria Garcia"
        )
        self.assertEqual(vehicle.model, "Camry")
        self.assertEqual(vehicle.year, 2023)
        self.assertEqual(vehicle.license_plate, "XYZ-789")
        self.assertEqual(vehicle.owner_name, "Maria Garcia")

    def test_get_vehicle(self):
        """Test getting a vehicle by ID."""
        vehicle = self.manager.register_vehicle(
            model="RAV4",
            year=2021,
            license_plate="DEF-456"
        )
        retrieved = self.manager.get_vehicle(vehicle.vehicle_id)
        self.assertEqual(retrieved, vehicle)

    def test_get_vehicle_not_found(self):
        """Test getting a non-existent vehicle."""
        result = self.manager.get_vehicle("non-existent-id")
        self.assertIsNone(result)

    def test_get_vehicle_by_plate(self):
        """Test getting a vehicle by license plate."""
        vehicle = self.manager.register_vehicle(
            model="Highlander",
            year=2020,
            license_plate="GHI-101"
        )
        retrieved = self.manager.get_vehicle_by_plate("GHI-101")
        self.assertEqual(retrieved, vehicle)

    def test_get_all_vehicles(self):
        """Test getting all vehicles."""
        self.manager.register_vehicle(
            model="Corolla", year=2022, license_plate="AAA-111"
        )
        self.manager.register_vehicle(
            model="Camry", year=2023, license_plate="BBB-222"
        )
        vehicles = self.manager.get_all_vehicles()
        self.assertEqual(len(vehicles), 2)

    def test_remove_vehicle(self):
        """Test removing a vehicle."""
        vehicle = self.manager.register_vehicle(
            model="Prius", year=2021, license_plate="CCC-333"
        )
        result = self.manager.remove_vehicle(vehicle.vehicle_id)
        self.assertTrue(result)
        self.assertIsNone(self.manager.get_vehicle(vehicle.vehicle_id))

    def test_remove_vehicle_not_found(self):
        """Test removing a non-existent vehicle."""
        result = self.manager.remove_vehicle("non-existent-id")
        self.assertFalse(result)

    def test_schedule_service(self):
        """Test scheduling a service."""
        vehicle = self.manager.register_vehicle(
            model="4Runner", year=2022, license_plate="DDD-444"
        )
        service = self.manager.schedule_service(
            vehicle_id=vehicle.vehicle_id,
            service_type=ServiceType.OIL_CHANGE,
            description="5000km service",
            cost=55.00,
            technician="Pedro"
        )
        self.assertIsNotNone(service)
        self.assertEqual(service.service_type, ServiceType.OIL_CHANGE)
        self.assertEqual(service.cost, 55.00)

    def test_schedule_service_invalid_vehicle(self):
        """Test scheduling a service for non-existent vehicle."""
        service = self.manager.schedule_service(
            vehicle_id="invalid-id",
            service_type=ServiceType.OIL_CHANGE,
            description="Test",
            cost=10.00
        )
        self.assertIsNone(service)

    def test_complete_service(self):
        """Test completing a service."""
        vehicle = self.manager.register_vehicle(
            model="Tacoma", year=2023, license_plate="EEE-555"
        )
        service = self.manager.schedule_service(
            vehicle_id=vehicle.vehicle_id,
            service_type=ServiceType.TIRE_ROTATION,
            description="Tire rotation",
            cost=30.00
        )
        result = self.manager.complete_service(
            vehicle.vehicle_id, service.service_id
        )
        self.assertTrue(result)
        self.assertTrue(service.completed)

    def test_get_pending_services(self):
        """Test getting pending services for a vehicle."""
        vehicle = self.manager.register_vehicle(
            model="Sienna", year=2022, license_plate="FFF-666"
        )
        self.manager.schedule_service(
            vehicle_id=vehicle.vehicle_id,
            service_type=ServiceType.BRAKE_INSPECTION,
            description="Brake check",
            cost=25.00
        )
        pending = self.manager.get_pending_services(vehicle.vehicle_id)
        self.assertEqual(len(pending), 1)

    def test_search_vehicles(self):
        """Test searching vehicles."""
        self.manager.register_vehicle(
            model="Corolla", year=2022, license_plate="AAA-111",
            owner_name="Juan Perez"
        )
        self.manager.register_vehicle(
            model="Camry", year=2023, license_plate="BBB-222",
            owner_name="Ana Lopez"
        )

        # Search by model
        results = self.manager.search_vehicles("Corolla")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].model, "Corolla")

        # Search by owner
        results = self.manager.search_vehicles("Ana")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].owner_name, "Ana Lopez")

    def test_search_vehicles_with_empty_owner(self):
        """Test searching vehicles when owner_name is empty."""
        self.manager.register_vehicle(
            model="Tacoma", year=2022, license_plate="CCC-333"
            # owner_name is empty by default
        )
        # Should not raise an error when searching
        results = self.manager.search_vehicles("Tacoma")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].model, "Tacoma")

    def test_get_statistics(self):
        """Test getting service statistics."""
        vehicle = self.manager.register_vehicle(
            model="Land Cruiser", year=2021, license_plate="GGG-777"
        )
        self.manager.schedule_service(
            vehicle_id=vehicle.vehicle_id,
            service_type=ServiceType.GENERAL_INSPECTION,
            description="Full inspection",
            cost=100.00
        )

        stats = self.manager.get_statistics()
        self.assertEqual(stats["total_vehicles"], 1)
        self.assertEqual(stats["total_services"], 1)
        self.assertEqual(stats["pending_services"], 1)
        self.assertEqual(stats["total_revenue"], 100.00)


if __name__ == "__main__":
    unittest.main()
