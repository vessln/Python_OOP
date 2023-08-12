from project.car.car import Car


class MuscleCar(Car):
    MIN_SPEED = 250
    MAX_SPEED = 450

    @property
    def speed_limit(self):
        return self.__speed_limit

    @speed_limit.setter
    def speed_limit(self, value):
        if value < MuscleCar.MIN_SPEED or value > MuscleCar.MAX_SPEED:
            raise ValueError(f"Invalid speed limit! Must be between 250 and 450!")
        self.__speed_limit = value
