from unittest import TestCase, main
from project.toy_store import ToyStore


class ToyStoreTest(TestCase):
    def test_correct_initialising(self):
        store = ToyStore()
        self.assertIsNone(store.toy_shelf["A"])
        self.assertIsNone(store.toy_shelf["B"])
        self.assertIsNone(store.toy_shelf["C"])
        self.assertIsNone(store.toy_shelf["D"])
        self.assertIsNone(store.toy_shelf["E"])
        self.assertIsNone(store.toy_shelf["F"])
        self.assertIsNone(store.toy_shelf["G"])

    def test_add_toy_in_non_existing_shelf_exception(self):
        store = ToyStore()
        with self.assertRaises(Exception) as ex:
            store.add_toy("V", "doll")
        self.assertEqual("Shelf doesn't exist!", str(ex.exception))

    def test_add_already_existing_toy_in_current_shelf_exception(self):
        store = ToyStore()
        store.add_toy("D", "doll")
        with self.assertRaises(Exception) as ex:
            store.add_toy("D", "doll")
        self.assertEqual("Toy is already in shelf!", str(ex.exception))

    def test_add_toy_in_taken_shelf_exception(self):
        store = ToyStore()
        store.add_toy("D", "doll")

        with self.assertRaises(Exception) as ex:
            store.add_toy("D", "dragon")
        self.assertEqual("Shelf is already taken!", str(ex.exception))

    def test_add_toy_in_free_shelf_correctly(self):
        store = ToyStore()
        result = store.add_toy("B", "baby")
        self.assertEqual("Toy:baby placed successfully!", result)
        self.assertEqual("baby", store.toy_shelf["B"])

        result = store.add_toy("E", "elephant")
        self.assertEqual("Toy:elephant placed successfully!", result)
        self.assertEqual("elephant", store.toy_shelf["E"])

    def test_remove_toy_from_non_existing_shelf_exception(self):
        store = ToyStore()
        with self.assertRaises(Exception) as ex:
            store.remove_toy("W", "godzilla")
        self.assertEqual("Shelf doesn't exist!", str(ex.exception))

    def test_remove_non_existing_toy_exception(self):
        store = ToyStore()
        store.add_toy("B", "baby")
        with self.assertRaises(Exception) as ex:
            store.remove_toy("B", "godzilla")
        self.assertEqual("Toy in that shelf doesn't exists!", str(ex.exception))

    def test_remove_toy_from_shelf_correctly(self):
        store = ToyStore()
        store.add_toy("A", "animal")
        store.add_toy("G", "godzilla")
        store.add_toy("C", "car")

        result = store.remove_toy("G", "godzilla")
        self.assertEqual(None, store.toy_shelf["G"])
        self.assertEqual("Remove toy:godzilla successfully!", result)

        result = store.remove_toy("C", "car")
        self.assertEqual(None, store.toy_shelf["C"])
        self.assertEqual("Remove toy:car successfully!", result)


if __name__ == "__main__":
    main()





