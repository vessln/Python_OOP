from project.route import Route
from project.user import User
from project.vehicles.cargo_van import CargoVan
from project.vehicles.passenger_car import PassengerCar


class ManagingApp:
    VEHICLE_TYPES = {"PassengerCar": PassengerCar, "CargoVan": CargoVan}

    def __init__(self):
        self.users = []
        self.vehicles = []
        self.routes = []

    @staticmethod
    def create_new_user(f_name, l_name, driving_license_num):
        return User(f_name, l_name, driving_license_num)

    def find_user_by_driving_license_number(self, dr_lic_num):
        return [u for u in self.users if u.driving_license_number == dr_lic_num]

    def find_vehicle_by_license_pl_number(self, lic_pl_num):
        return [v for v in self.vehicles if v.license_plate_number == lic_pl_num]

    def get_first_count_of_damaged_vehicles(self, n):
        damaged_vehicles = [v for v in self.vehicles if v.is_damaged is True]
        sort_vehicles = sorted(damaged_vehicles, key=lambda v: (v.brand, v.model))
        return sort_vehicles[:n]

    def register_user(self, first_name, last_name, driving_license_number):
        if self.find_user_by_driving_license_number(driving_license_number):
            return f"{driving_license_number} has already been registered to our platform."

        new_user = self.create_new_user(first_name, last_name, driving_license_number)
        self.users.append(new_user)
        return f"{first_name} {last_name} was successfully registered under DLN-{driving_license_number}"

    def upload_vehicle(self, vehicle_type, brand, model, license_plate_number):
        if vehicle_type not in ManagingApp.VEHICLE_TYPES.keys():
            return f"Vehicle type {vehicle_type} is inaccessible."

        if self.find_vehicle_by_license_pl_number(license_plate_number):
            return f"{license_plate_number} belongs to another vehicle."

        new_vehicle = ManagingApp.VEHICLE_TYPES[vehicle_type](brand, model, license_plate_number)
        self.vehicles.append(new_vehicle)
        return f"{brand} {model} was successfully uploaded with LPN-{license_plate_number}."

    def allow_route(self, start_point, end_point, length):
        for route_ob in self.routes:
            if route_ob.start_point == start_point and route_ob.end_point == end_point and route_ob.length == length:
                return f"{start_point}/{end_point} - {length} km had already been added to our platform."

            if route_ob.start_point == start_point and route_ob.end_point == end_point and route_ob.length < length:
                return f"{start_point}/{end_point} shorter route had already been added to our platform."

            if route_ob.start_point == start_point and route_ob.end_point == end_point and route_ob.length > length:
                route_ob.is_locked = True

        id_new_route = len(self.routes) + 1
        new_route = Route(start_point, end_point, length, id_new_route)
        self.routes.append(new_route)
        return f"{start_point}/{end_point} - {length} km is unlocked and available to use."

    def make_trip(self, driving_license_number, license_plate_number, route_id, is_accident_happened):
        current_user = self.find_user_by_driving_license_number(driving_license_number)[0]
        current_vehicle = self.find_vehicle_by_license_pl_number(license_plate_number)[0]
        current_route = [r for r in self.routes if r.route_id == route_id][0]

        if current_user.is_blocked:
            return f"User {driving_license_number} is blocked in the platform! This trip is not allowed."

        if current_vehicle.is_damaged:
            return f"Vehicle {license_plate_number} is damaged! This trip is not allowed."

        if current_route.is_locked:
            return f"Route {route_id} is locked! This trip is not allowed."

        mileage_km = current_route.length
        current_vehicle.drive(mileage_km)

        if is_accident_happened:
            current_vehicle.is_damaged = True
            current_user.decrease_rating()
        else:
            current_user.increase_rating()

        return current_vehicle.__str__()

    def repair_vehicles(self, count):
        vehicles_for_repair = self.get_first_count_of_damaged_vehicles(count)
        for vehicle_obj in vehicles_for_repair:
            vehicle_obj.is_damaged = False
            vehicle_obj.battery_level = 100

        return f"{len(vehicles_for_repair)} vehicles were successfully repaired!"

    def users_report(self):
        arranged_users = sorted(self.users, key=lambda u: -u.rating)
        result = "*** E-Drive-Rent ***"
        for el in arranged_users:
            result += f"\n{el.__str__()}"

        return result



