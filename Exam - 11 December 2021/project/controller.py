from project.car.muscle_car import MuscleCar
from project.car.sports_car import SportsCar
from project.driver import Driver
from project.race import Race


class Controller:
    VALID_CAR_TYPES = {"MuscleCar": MuscleCar,
                       "SportsCar": SportsCar}

    def __init__(self):
        self.cars = []
        self.drivers = []
        self.races = []

    @staticmethod
    def find_object_by_name(name, list_with_objects):
        return [ob for ob in list_with_objects if ob.name == name]

    def find_car_by_model(self, model):
        return [c for c in self.cars if c.model == model]

    def find_car_by_type(self, c_type):
        return [c for c in self.cars if type(c).__name__ == c_type]

    def create_car(self, car_type, model, speed_limit):
        if car_type in Controller.VALID_CAR_TYPES.keys():
            car = self.find_car_by_model(model)

            if car:
                raise Exception(f"Car {model} is already created!")
            else:
                new_car = Controller.VALID_CAR_TYPES[car_type](model, speed_limit)
                self.cars.append(new_car)
                return f"{car_type} {model} is created."

    def create_driver(self, driver_name):
        driver = Controller.find_object_by_name(driver_name, self.drivers)

        if driver:
            raise Exception(f"Driver {driver_name} is already created!")
        else:
            new_driver = Driver(driver_name)
            self.drivers.append(new_driver)
            return f"Driver {driver_name} is created."

    def create_race(self, race_name):
        race = Controller.find_object_by_name(race_name, self.races)

        if race:
            raise Exception(f"Race {race_name} is already created!")
        else:
            new_race = Race(race_name)
            self.races.append(new_race)
            return f"Race {race_name} is created."

    def add_car_to_driver(self, driver_name, car_type):
        driver = Controller.find_object_by_name(driver_name, self.drivers)
        cars = self.find_car_by_type(car_type)

        if not driver:
            raise Exception(f"Driver {driver_name} could not be found!")

        current_driver = driver[0]

        if not cars:
            raise Exception(f"Car {car_type} could not be found!")

        available_cars = [c for c in cars if not c.is_taken]
        if not available_cars:
            raise Exception(f"Car {car_type} could not be found!")

        new_car = available_cars[-1]

        if current_driver.car:
            old_car_model = current_driver.car.model
            current_driver.car.is_taken = False

            current_driver.car = new_car
            new_car.is_taken = True

            return f"Driver {driver_name} changed his car from {old_car_model} to {new_car.model}."

        if not current_driver.car:
            current_driver.car = new_car
            new_car.is_taken = True

            return f"Driver {current_driver.name} chose the car {new_car.model}."

    def add_driver_to_race(self, race_name, driver_name):
        race = Controller.find_object_by_name(race_name, self.races)
        driver = Controller.find_object_by_name(driver_name, self.drivers)

        if not race:
            raise Exception(f"Race {race_name} could not be found!")
        current_race = race[0]

        if not driver:
            raise Exception(f"Driver {driver_name} could not be found!")
        current_driver = driver[0]

        if not current_driver.car:
            raise Exception(f"Driver {driver_name} could not participate in the race!")

        if current_driver in current_race.drivers:
            return f"Driver {driver_name} is already added in {race_name} race."

        current_race.drivers.append(current_driver)
        return f"Driver {driver_name} added in {race_name} race."

    def start_race(self, race_name):
        race = Controller.find_object_by_name(race_name, self.races)

        if not race:
            raise Exception(f"Race {race_name} could not be found!")
        current_race = race[0]

        if len(current_race.drivers) < 3:
            raise Exception(f"Race {race_name} cannot start with less than 3 participants!")

        result = []
        all_drivers = current_race.drivers

        sorted_fastest_dr = sorted(all_drivers, key=lambda x: -x.car.speed_limit)

        for driver in sorted_fastest_dr[0:3]:
            driver.number_of_wins += 1
            result.append(f"Driver {driver.name} wins the {race_name} race with a speed of {driver.car.speed_limit}.")

        return '\n'.join(result)




