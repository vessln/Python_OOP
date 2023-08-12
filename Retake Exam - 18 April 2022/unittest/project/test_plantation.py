from unittest import TestCase, main
from project.plantation import Plantation


class TestPlantation(TestCase):
    def setUp(self):
        self.plantation = Plantation(20)

    def test_correct_initializing(self):
        self.assertEqual(20, self.plantation.size)
        self.assertEqual({}, self.plantation.plants)
        self.assertEqual([], self.plantation.workers)

    def test_value_size_less_than_zero_error(self):
        with self.assertRaises(ValueError) as ve:
            self.plantation.size = -1
        self.assertEqual("Size must be positive number!", str(ve.exception))

    def test_already_hired_worker_error(self):
        self.plantation.workers = ["Vesi"]

        with self.assertRaises(ValueError) as ve:
            self.plantation.hire_worker("Vesi")
        self.assertEqual("Worker already hired!", str(ve.exception))

        self.plantation.workers = ["Vesi", "Sara"]
        with self.assertRaises(ValueError) as ve:
            self.plantation.hire_worker("Sara")
        self.assertEqual("Worker already hired!", str(ve.exception))

    def test_hire_new_worker_correctly(self):
        self.assertEqual([], self.plantation.workers)

        result = self.plantation.hire_worker("Vesi")
        self.assertEqual(["Vesi"], self.plantation.workers)
        self.assertEqual("Vesi successfully hired.", result)

        result = self.plantation.hire_worker("Lilly")
        self.assertEqual(["Vesi", "Lilly"], self.plantation.workers)
        self.assertEqual("Lilly successfully hired.", result)

    def test_len_count_of_total_planted_plants(self):
        self.plantation.workers = ["Vesi"]
        self.assertEqual({}, self.plantation.plants)
        self.assertEqual(0, len(self.plantation))

        self.plantation.plants = {"Vesi": ["Rose"]}
        self.assertEqual(1, len(self.plantation))

        self.plantation.workers = ["Vesi"]
        self.plantation.plants = {"Vesi": ["Begonia", "Calendula", "Rose"],
                                  "Ivaylo": [], "Sara": ["Mint", "Hyacinth"]}
        self.assertEqual(5, len(self.plantation))

    def test_planting_not_correct_worker_error(self):
        self.plantation.workers = []
        with self.assertRaises(ValueError) as ve:
            self.plantation.planting("Vesi", "Rose")
        self.assertEqual("Worker with name Vesi is not hired!", str(ve.exception))

        self.plantation.workers = ["Vesi", "Mike"]
        with self.assertRaises(ValueError) as ve:
            self.plantation.planting("Sara", "Lavender")
        self.assertEqual("Worker with name Sara is not hired!", str(ve.exception))

    def test_planting_if_plantation_is_full_error(self):
        self.plantation.size = 3
        self.plantation.workers = ["Vesi", "Sara"]
        self.plantation.plants = {"Vesi": ["Begonia", "Calendula"],
                                  "Sara": ["Mint"]}

        with self.assertRaises(ValueError) as ve:
            self.plantation.planting("Sara", "Tulip")
        self.assertEqual("The plantation is full!", str(ve.exception))

        self.plantation.plants = {"Vesi": ["Begonia", "Calendula"],
                                  "Sara": ["Mint", "Plant", "Lavender"]}

        with self.assertRaises(ValueError) as ve:
            self.plantation.planting("Sara", "Tulip")
        self.assertEqual("The plantation is full!", str(ve.exception))

    def test_existing_worker_plant_new_plant(self):
        self.plantation.workers = ["Vesi"]
        self.plantation.plants = {"Vesi": ["Rose"]}

        result = self.plantation.planting("Vesi", "Begonia")
        self.assertEqual({"Vesi": ["Rose", "Begonia"]}, self.plantation.plants)
        self.assertEqual("Vesi planted Begonia.", result)

        self.plantation.workers = ["Sara", "Vesi"]
        self.plantation.plants = {"Vesi": ["Rose", "Begonia"],
                                  "Sara": ["Calendula"]}

        result = self.plantation.planting("Sara", "Dahlia")
        self.assertEqual({"Vesi": ["Rose", "Begonia"],
                          "Sara": ["Calendula", "Dahlia"]}, self.plantation.plants)
        self.assertEqual("Sara planted Dahlia.", result)

    def test_worker_plant_for_first_time(self):
        self.plantation.workers = []
        self.plantation.plants = {}

        self.plantation.hire_worker("Vesi")
        result = self.plantation.planting("Vesi", "Rose")
        self.assertEqual({"Vesi": ["Rose"]}, self.plantation.plants)
        self.assertEqual("Vesi planted it's first Rose.", result)

        self.plantation.hire_worker("Sara")
        result = self.plantation.planting("Sara", "Tulip")
        self.assertEqual({"Vesi": ["Rose"], "Sara": ["Tulip"]}, self.plantation.plants)
        self.assertEqual("Sara planted it's first Tulip.", result)

    def test_str_method(self):
        expected = f"Plantation size: 20\n"
        self.assertEqual(expected, str(self.plantation))

        expected = f"Plantation size: 20\nSara"
        self.plantation.workers = ["Sara"]
        self.assertEqual(expected, str(self.plantation))

        expected = f"Plantation size: 20\nSara, Vesi"
        self.plantation.workers = ["Sara", "Vesi"]
        self.assertEqual(expected, str(self.plantation))

        expected = f"Plantation size: 20\nSara, Vesi\nVesi planted: Rose, Begonia"
        self.plantation.workers = ["Sara", "Vesi"]
        self.plantation.plants = {"Vesi": ["Rose", "Begonia"]}
        self.assertEqual(expected, str(self.plantation))

        expected = f"Plantation size: 20\nSara, Vesi\nVesi planted: Rose, Begonia\nSara planted: Mint, Tulip"
        self.plantation.workers = ["Sara", "Vesi"]
        self.plantation.plants = {"Vesi": ["Rose", "Begonia"], "Sara": ["Mint", "Tulip"]}
        self.assertEqual(expected, str(self.plantation))

    def test_repr_method(self):
        expected = f"Size: {20}\nWorkers: "
        self.assertEqual(expected, repr(self.plantation))

        self.plantation.workers = ["Vesi"]
        expected = f"Size: {20}\nWorkers: Vesi"
        self.assertEqual(expected, repr(self.plantation))

        self.plantation.workers = ["Vesi", "Sara", "Ivaylo"]
        expected = f"Size: {20}\nWorkers: Vesi, Sara, Ivaylo"
        self.assertEqual(expected, repr(self.plantation))


if __name__ == "__main__":
    main()

