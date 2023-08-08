from unittest import TestCase, main

from robot import Robot


class RobotTest(TestCase):
    def test_correct_initializing(self):
        robot = Robot("a1", "Military", 5, 1000)
        self.assertEqual("a1", robot.robot_id)
        self.assertEqual("Military", robot.category)
        self.assertEqual(5, robot.available_capacity)
        self.assertEqual(1000, robot.price)
        self.assertEqual([], robot.hardware_upgrades)
        self.assertEqual([], robot.software_updates)

    def test_category_not_in_allowed_categories_error(self):
        robot = Robot("a1", "Education", 5, 1000)
        categories = ['Military', 'Education', 'Entertainment', 'Humanoids']
        with self.assertRaises(ValueError) as ex:
            robot.category = "Clean"
        self.assertEqual(f"Category should be one of '{categories}'", str(ex.exception))

    def test_price_negative_value_error(self):
        robot = Robot("a2", "Education", 10, 1)
        with self.assertRaises(ValueError) as ex:
            robot.price = -1
        self.assertEqual("Price cannot be negative!", str(ex.exception))

    def test_not_upgrade_hardware_part_robot(self):
        robot = Robot("a2", "Education", 10, 1500)
        robot.hardware_upgrades = ["a2f57 part"]
        result = robot.upgrade("a2f57 part", 55.5)
        self.assertEqual("Robot a2 was not upgraded.", result)

    def test_upgrade_hardware_robot_upgrades_and_price(self):
        robot = Robot("a2", "Education", 10, 1500)
        robot.hardware_upgrades = []
        result = robot.upgrade("part_4", 10.2)

        self.assertEqual(["part_4"], robot.hardware_upgrades)
        self.assertEqual(1515.3, robot.price)
        self.assertEqual("Robot a2 was upgraded with part_4.", result)

        res = robot.upgrade("part_88", 15)
        self.assertEqual(["part_4", "part_88"], robot.hardware_upgrades)
        self.assertEqual(1537.8, robot.price)
        self.assertEqual("Robot a2 was upgraded with part_88.", res)

    def test_not_update_robot_version_exist_enough_capacity(self):
        robot = Robot("a2", "Education", 10, 1500)
        robot.software_updates = [12.0, 12.1]
        result = robot.update(12.1, 3)
        self.assertEqual(f"Robot a2 was not updated.", result)

        robot.software_updates = [12.0, 12.1, 12.2]
        result = robot.update(12.1, 3)
        self.assertEqual(f"Robot a2 was not updated.", result)

    def test_not_upgrade_robot_lower_version_not_enough_capacity(self):
        robot = Robot("a2", "Education", 10, 1500)
        robot.software_updates = [1.0, 1.1]
        result = robot.update(1.2, 15)
        self.assertEqual(f"Robot a2 was not updated.", result)

    def test_update_robot_version_decrease_capacity(self):
        robot = Robot("a2", "Education", 10, 1500)
        robot.software_updates = [1.0, 1.1]
        result = robot.update(1.2, 4)

        self.assertEqual([1.0, 1.1, 1.2], robot.software_updates)
        self.assertEqual(6, robot.available_capacity)
        self.assertEqual('Robot a2 was updated to version 1.2.', result)

    def test_gt_my_robots_price_is_more_expensive_than_others_robot_price(self):
        robot_ed = Robot("a2", "Education", 25, 2500)
        robot_hum = Robot("y66", "Humanoids", 10, 1000)
        result = robot_ed.__gt__(robot_hum)
        self.assertEqual("Robot with ID a2 is more expensive than Robot with ID y66.", result)

    def test_gt_prices_of_two_robots_are_equal(self):
        robot_ed = Robot("a2", "Education", 25, 2500)
        robot_hum = Robot("y66", "Humanoids", 10, 2500)
        result = robot_ed.__gt__(robot_hum)
        self.assertEqual("Robot with ID a2 costs equal to Robot with ID y66.", result)

    def test_gt_my_robots_price_is_cheaper_than_others_robot_price(self):
        robot_ed = Robot("a2", "Education", 25, 1000)
        robot_hum = Robot("y66", "Humanoids", 10, 1400)
        result = robot_ed.__gt__(robot_hum)
        self.assertEqual("Robot with ID a2 is cheaper than Robot with ID y66.", result)


if __name__ == "__main__":
    main()




