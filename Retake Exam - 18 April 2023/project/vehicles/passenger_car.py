from project.vehicles.base_vehicle import BaseVehicle


class PassengerCar(BaseVehicle):
    MAX_MILEAGE = 450.00

    def __init__(self, brand, model, license_plate_number):
        super().__init__(brand, model, license_plate_number, max_mileage=PassengerCar.MAX_MILEAGE)

    def drive(self, mileage):
        part = mileage / PassengerCar.MAX_MILEAGE
        self.battery_level -= round(part * 100)

