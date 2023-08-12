from project.car.car import Car


class SportsCar(Car):
    MIN_SPEED = 400
    MAX_SPEED = 600

    @property
    def speed_limit(self):
        return self.__speed_limit

    @speed_limit.setter
    def speed_limit(self, value):
        if value < SportsCar.MIN_SPEED or value > SportsCar.MAX_SPEED:
            raise ValueError(f"Invalid speed limit! Must be between 400 and 600!")
        self.__speed_limit = value
