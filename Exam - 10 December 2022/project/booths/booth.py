from abc import ABC, abstractmethod


class Booth(ABC):
    def __init__(self, booth_number, capacity):
        self.booth_number = booth_number
        self.capacity = capacity
        self.delicacy_orders = []
        self.price_for_reservation = 0
        self.is_reserved = False

    @property
    @abstractmethod
    def price_per_person(self):
        pass

    @property
    def capacity(self):
        return self.__capacity

    @capacity.setter
    def capacity(self, value):
        if value < 0:
            raise ValueError("Capacity cannot be a negative number!")
        self.__capacity = value

    def reserve(self, number_of_people):
        price = self.price_per_person * number_of_people
        self.price_for_reservation = price
        self.is_reserved = True

    def calculate_bill(self):
        bill = 0
        for delicacy_ord in self.delicacy_orders:
            bill += delicacy_ord.price

        bill += self.price_for_reservation

        return bill







