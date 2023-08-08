from project.booths.open_booth import OpenBooth
from project.booths.private_booth import PrivateBooth
from project.delicacies.gingerbread import Gingerbread
from project.delicacies.stolen import Stolen


class ChristmasPastryShopApp:
    DELICACIES_TYPES = {"Gingerbread": Gingerbread,
                        "Stolen": Stolen}

    BOOTHS_TYPES = {"Open Booth": OpenBooth,
                    "Private Booth": PrivateBooth}

    def __init__(self):
        self.booths = []
        self.delicacies = []
        self.income = 0.0

    def find_delicacy_by_name(self, name):
        return [d for d in self.delicacies if d.name == name]

    def find_booth_by_number(self, number):
        return [b for b in self.booths if b.booth_number == number]

    def add_delicacy(self, type_delicacy, name, price):
        if self.find_delicacy_by_name(name):
            raise Exception(f"{name} already exists!")

        if type_delicacy not in self.DELICACIES_TYPES:
            raise Exception(f"{type_delicacy} is not on our delicacy menu!")

        new_delicacy = self.DELICACIES_TYPES[type_delicacy](name, price)
        self.delicacies.append(new_delicacy)
        return f"Added delicacy {name} - {type_delicacy} to the pastry shop."

    def add_booth(self, type_booth, booth_number, capacity):
        if self.find_booth_by_number(booth_number):
            raise Exception(f"Booth number {booth_number} already exists!")

        if type_booth not in self.BOOTHS_TYPES:
            raise Exception(f"{type_booth} is not a valid booth!")

        new_booth = self.BOOTHS_TYPES[type_booth](booth_number, capacity)
        self.booths.append(new_booth)
        return f"Added booth number {booth_number} in the pastry shop."

    def reserve_booth(self, number_of_people):
        for booth_obj in self.booths:
            if not booth_obj.is_reserved and booth_obj.capacity >= number_of_people:
                booth_obj.reserve(number_of_people)
                return f"Booth {booth_obj.booth_number} has been reserved for {number_of_people} people."

        raise Exception(f"No available booth for {number_of_people} people!")

    def order_delicacy(self, booth_number, delicacy_name):
        booth = self.find_booth_by_number(booth_number)
        delicacy = self.find_delicacy_by_name(delicacy_name)

        if not booth:
            raise Exception(f"Could not find booth {booth_number}!")

        if not delicacy:
            raise Exception(f"No {delicacy_name} in the pastry shop!")

        current_booth = booth[0]
        current_delicacy = delicacy[0]
        current_booth.delicacy_orders.append(current_delicacy)
        return f"Booth {booth_number} ordered {delicacy_name}."

    def leave_booth(self, booth_number):
        booth = self.find_booth_by_number(booth_number)[0]
        bill = booth.calculate_bill()
        self.income += bill

        booth.delicacy_orders = []
        booth.is_reserved = False
        booth.price_for_reservation = 0
        return f"Booth {booth_number}:\nBill: {bill:.2f}lv."

    def get_income(self):
        return f"Income: {self.income:.2f}lv."



