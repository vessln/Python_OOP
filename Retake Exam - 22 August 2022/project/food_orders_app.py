from project.client import Client
from project.meals.dessert import Dessert
from project.meals.main_dish import MainDish
from project.meals.meal import Meal
from project.meals.starter import Starter


class FoodOrdersApp:
    VALID_MEALS = {"Starter": Starter,
                   "MainDish": MainDish,
                   "Dessert": Dessert}

    def __init__(self):
        self.menu = []
        self.clients_list = []
        self.paid_bills = 0

    def find_meal_by_name(self, meal_name):
        return [m for m in self.menu if m.name == meal_name]

    def find_client_by_number(self, number):
        return [c for c in self.clients_list if c.phone_number == number]

    def register_client(self, client_phone_number):
        if self.find_client_by_number(client_phone_number):
            raise Exception("The client has already been registered!")

        new_client = Client(client_phone_number)
        self.clients_list.append(new_client)
        return f"Client {client_phone_number} registered successfully."

    def add_meals_to_menu(self, *meals: Meal):
        for el in meals:
            if isinstance(el, Starter) or isinstance(el, MainDish) or isinstance(el, Dessert):
                self.menu.append(el)

    def show_menu(self):
        if len(self.menu) < 5:
            raise Exception("The menu is not ready!")

        return '\n'.join([meal.details() for meal in self.menu])

    def add_meals_to_shopping_cart(self, client_phone_number, **meal_names_and_quantities):
        if len(self.menu) < 5:
            raise Exception("The menu is not ready!")

        client_obj = self.find_client_by_number(client_phone_number)

        if not client_obj:
            client_obj = Client(client_phone_number)
            self.clients_list.append(client_obj)

        client = client_obj[0]
        current_bill = 0
        current_ordered_meals = []

        for meal_name, qnt in meal_names_and_quantities.items():
            meal = self.find_meal_by_name(meal_name)
            if not meal:
                raise Exception(f"{meal_name} is not on the menu!")

            meal_obj = meal[0]
            if meal_obj.quantity < qnt:
                raise Exception(f"Not enough quantity of {meal_obj.__class__.__name__}: {meal_name}!")

        for meal_name, qnt in meal_names_and_quantities.items():
            meal = self.find_meal_by_name(meal_name)[0]
            current_ordered_meals.append(meal)
            current_bill += meal.price * qnt
            meal.quantity -= qnt

            if meal_name not in client.ordered_meals_qnt:
                client.ordered_meals_qnt[meal_name] = 0
            client.ordered_meals_qnt[meal_name] += qnt

        client.bill += current_bill
        client.shopping_cart.extend(current_ordered_meals)

        return f"Client {client_phone_number} successfully ordered " \
               f"{', '.join([m.name for m in client.shopping_cart])} for {client.bill:.2f}lv."

    def cancel_order(self, client_phone_number):
        client = self.find_client_by_number(client_phone_number)[0]
        if not client.shopping_cart:
            raise Exception("There are no ordered meals!")

        for meal_name, qnt in client.ordered_meals_qnt:
            for meal in self.menu:
                if meal.name == meal_name:
                    meal.quantity += qnt

        client.bill = 0
        client.shopping_cart = []
        client.ordered_meals_qnt = {}

        return f"Client {client_phone_number} successfully canceled his order."

    def finish_order(self, client_phone_number):
        client = self.find_client_by_number(client_phone_number)[0]
        if not client.shopping_cart:
            raise Exception("There are no ordered meals!")

        paid_money = client.bill
        client.bill = 0
        client.shopping_cart = []
        client.ordered_meals_qnt = {}
        self.paid_bills += 1
        return f"Receipt #{self.paid_bills} with total amount of {paid_money:.2f}" \
               f" was successfully paid for {client_phone_number}."

    def __str__(self):
        return f"Food Orders App has {len(self.menu)} meals " \
               f"on the menu and {len(self.clients_list)} clients."



