from project.equipment.base_equipment import BaseEquipment


class KneePad(BaseEquipment):
    def __init__(self):
        super().__init__(120, 15.0)

    def increase_price(self):
        price = self.price * 0.2
        self.price += price
