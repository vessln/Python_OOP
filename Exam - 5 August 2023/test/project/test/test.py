from unittest import TestCase, main
from project.second_hand_car import SecondHandCar


class TestSecondHandCar(TestCase):
    def setUp(self):
        self.car = SecondHandCar("Audi", "A3", 550, 1000.5)
        self.assertEqual("Audi", self.car.model)
        self.assertEqual("A3", self.car.car_type)
        self.assertEqual(550, self.car.mileage)
        self.assertEqual(1000.5, self.car.price)
        self.assertEqual([], self.car.repairs)

    def test_too_lower_value_of_price_error(self):
        with self.assertRaises(ValueError) as ve:
            self.car.price = -1.5
        self.assertEqual("Price should be greater than 1.0!", str(ve.exception))

        with self.assertRaises(ValueError) as ve:
            self.car.price = 0
        self.assertEqual("Price should be greater than 1.0!", str(ve.exception))

        with self.assertRaises(ValueError) as ve:
            self.car.price = 1.0
        self.assertEqual("Price should be greater than 1.0!", str(ve.exception))

    def test_too_lower_value_of_mileage_error(self):
        with self.assertRaises(ValueError) as ve:
            self.car.mileage = -5
        self.assertEqual("Please, second-hand cars only! Mileage must be greater than 100!", str(ve.exception))

        with self.assertRaises(ValueError) as ve:
            self.car.mileage = 0
        self.assertEqual("Please, second-hand cars only! Mileage must be greater than 100!", str(ve.exception))

        with self.assertRaises(ValueError) as ve:
            self.car.mileage = 100
        self.assertEqual("Please, second-hand cars only! Mileage must be greater than 100!", str(ve.exception))

    def test_set_promotional_price_incorrect_error(self):
        with self.assertRaises(ValueError) as ve:
            self.car.set_promotional_price(1100)
        self.assertEqual("You are supposed to decrease the price!", str(ve.exception))

        with self.assertRaises(ValueError) as ve:
            self.car.set_promotional_price(1000.5)
        self.assertEqual("You are supposed to decrease the price!", str(ve.exception))

    def test_set_promotional_price_correctly(self):
        self.assertEqual(1000.5, self.car.price)

        result = self.car.set_promotional_price(1000.4)
        self.assertEqual(1000.4, self.car.price)
        self.assertEqual("The promotional price has been successfully set.", result)

        result = self.car.set_promotional_price(750)
        self.assertEqual(750, self.car.price)
        self.assertEqual("The promotional price has been successfully set.", result)

    def test_need_repair_but_service_is_too_expensive(self):
        self.car.price = 1000

        result = self.car.need_repair(501, "change_tires")
        self.assertEqual(result, "Repair is impossible!")

        result = self.car.need_repair(1050.5, "add_coilovers")
        self.assertEqual(result, "Repair is impossible!")

    def test_need_repair_cheap_service(self):
        self.car.price = 1000

        result = self.car.need_repair(300, "transmission")
        self.assertEqual(1300, self.car.price)
        self.assertEqual(["transmission"], self.car.repairs)
        self.assertEqual(result, "Price has been increased due to repair charges.")

        result = self.car.need_repair(500, "ABC system")
        self.assertEqual(1800, self.car.price)
        self.assertEqual(["transmission", "ABC system"], self.car.repairs)
        self.assertEqual(result, "Price has been increased due to repair charges.")

    def test_gt_method_with_different_car_type(self):
        self.assertEqual("A3", self.car.car_type)
        second_car = SecondHandCar("Audi", "TT", 300, 19000)

        result = self.car.__gt__(second_car)
        self.assertEqual(result, "Cars cannot be compared. Type mismatch!")

        result = second_car.__gt__(self.car)
        self.assertEqual(result, "Cars cannot be compared. Type mismatch!")

    def test_gt_method_compare_cars_by_price_correctly(self):
        second_car = SecondHandCar("Audi", "A3", 300, 2500)

        self.car.price = 2500
        result = self.car.__gt__(second_car)
        self.assertEqual(result, False)

        self.car.price = 1500
        result = self.car.__gt__(second_car)
        self.assertEqual(result, False)

        self.car.price = 2501
        result = self.car.__gt__(second_car)
        self.assertEqual(result, True)

        self.car.price = 2500
        result = second_car.__gt__(self.car)
        self.assertEqual(result, False)

        self.car.price = 1500
        result = second_car.__gt__(self.car)
        self.assertEqual(result, True)

        self.car.price = 2501
        result = second_car.__gt__(self.car)
        self.assertEqual(result, False)

    def test_str_method(self):
        expected = "Model Audi | Type A3 | Milage 550km\nCurrent price: 1000.50 | Number of Repairs: 0"
        result = str(self.car)
        self.assertEqual(expected, result)


if __name__ == "__main__":
    main()
