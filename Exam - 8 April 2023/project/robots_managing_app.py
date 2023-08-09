from project.robots.female_robot import FemaleRobot
from project.robots.male_robot import MaleRobot
from project.services.main_service import MainService
from project.services.secondary_service import SecondaryService


class RobotsManagingApp:
    VALID_SERVICES = {"MainService": MainService,
                      "SecondaryService": SecondaryService}

    VALID_ROBOTS = {"MaleRobot": MaleRobot,
                    "FemaleRobot": FemaleRobot}

    def __init__(self):
        self.robots = []
        self.services = []

    def add_service(self, service_type, name):
        if service_type not in RobotsManagingApp.VALID_SERVICES:
            raise Exception("Invalid service type!")

        new_service = self.create_service(service_type, name)
        self.services.append(new_service)
        return f"{service_type} is successfully added."

    def create_service(self, s_type, name):
        return RobotsManagingApp.VALID_SERVICES[s_type](name)

    def add_robot(self, robot_type, name, kind, price):
        if robot_type not in RobotsManagingApp.VALID_ROBOTS:
            raise Exception("Invalid robot type!")

        new_robot = self.create_robot(robot_type, name, kind, price)
        self.robots.append(new_robot)
        return f"{robot_type} is successfully added."

    def create_robot(self, r_type, name, kind, price):
        return RobotsManagingApp.VALID_ROBOTS[r_type](name, kind, price)

    def add_robot_to_service(self, robot_name: str, service_name: str):
        robot_obj = [r for r in self.robots if r.name == robot_name][0]
        service_obj = [s for s in self.services if s.name == service_name][0]

        service_class_name = service_obj.__class__.__name__
        if robot_obj.POSSIBLE_SERVICE != service_class_name:
            return "Unsuitable service."

        if len(service_obj.robots) >= service_obj.capacity:
            raise Exception("Not enough capacity for this robot!")

        self.robots.remove(robot_obj)
        service_obj.robots.append(robot_obj)
        return f"Successfully added {robot_name} to {service_name}."

    def remove_robot_from_service(self, robot_name: str, service_name: str):
        service_obj = [s for s in self.services if s.name == service_name][0]
        robot_obj = [r for r in service_obj.robots if r.name == robot_name]

        if not robot_obj:
            raise Exception("No such robot in this service!")

        robot = robot_obj[0]
        service_obj.robots.remove(robot)
        self.robots.append(robot)
        return f"Successfully removed {robot_name} from {service_name}."

    def feed_all_robots_from_service(self, service_name: str):
        service_obj = [s for s in self.services if s.name == service_name][0]
        for el_robot in service_obj.robots:
            el_robot.eating()

        return f"Robots fed: {len(service_obj.robots)}."

    def service_price(self, service_name: str):
        service_obj = [s for s in self.services if s.name == service_name][0]
        total_price = 0
        for el_robot in service_obj.robots:
            total_price += el_robot.price

        return f"The value of service {service_name} is {total_price:.2f}."

    def __str__(self):
        result = ""
        for el in self.services:
            result += f"{el.details()}\n"
        return result.strip()


