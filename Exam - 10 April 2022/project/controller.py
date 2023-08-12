from project.player import Player
from project.supply.drink import Drink
from project.supply.food import Food
from project.supply.supply import Supply


class Controller:
    SUSTENANCE_TYPES = {"Food": Food, "Drink": Drink}

    def __init__(self):
        self.players = []
        self.supplies = []

    def find_player_by_name(self, name):
        return [p for p in self.players if p.name == name]

    def find_supply_by_type(self, s_type):
        return [s for s in self.supplies if type(s).__name__ == s_type]

    def add_player(self, *args: Player):
        added_players = []

        for player_obj in args:
            if not self.find_player_by_name(player_obj.name):
                self.players.append(player_obj)
                added_players.append(player_obj.name)

        return f"Successfully added: {', '.join(added_players)}"

    def add_supply(self, *args: Supply):
        for supply_obj in args:
            self.supplies.append(supply_obj)

    def sustain(self, player_name, sustenance_type):
        player = self.find_player_by_name(player_name)

        if player and sustenance_type in self.SUSTENANCE_TYPES.keys():
            current_player = player[0]

            if current_player.stamina == 100:
                return f"{player_name} have enough stamina."

            if sustenance_type == "Food":
                if not self.find_supply_by_type(sustenance_type):
                    raise Exception(f"There are no food supplies left!")

            if sustenance_type == "Drink":
                if not self.find_supply_by_type(sustenance_type):
                    raise Exception(f"There are no drink supplies left!")

            last_supply = self.find_supply_by_type(sustenance_type)[-1]

            if current_player.stamina + last_supply.energy > 100:
                current_player.stamina = 100
            else:
                current_player.stamina += last_supply.energy

            supply_name = last_supply.name

            for i in range(len(self.supplies)-1, 0, -1):
                if self.supplies[i] == last_supply:
                    self.supplies.pop(i)
                    break

            return f"{player_name} sustained successfully with {supply_name}."

    def duel(self, first_player_name, second_player_name):
        first_pl = self.find_player_by_name(first_player_name)[0]
        second_pl = self.find_player_by_name(second_player_name)[0]

        if first_pl.stamina > 0 and second_pl.stamina > 0:
            attackers = sorted([first_pl, second_pl], key=lambda x: x.stamina)
            first_attacker, second_attacker = attackers[0], attackers[1]

            if second_attacker.stamina - (first_attacker.stamina / 2) <= 0:
                second_attacker.stamina = 0
                return f"Winner: {first_attacker.name}"
            else:
                second_attacker.stamina -= (first_attacker.stamina / 2)

            if first_attacker.stamina - (second_attacker.stamina / 2) <= 0:
                first_attacker.stamina = 0
                return f"Winner: {second_attacker.name}"
            else:
                first_attacker.stamina -= (second_attacker.stamina / 2)

            winner = sorted([first_attacker, second_attacker], key=lambda x: x.stamina)[-1]
            return f"Winner: {winner.name}"

        else:
            result = []
            for player in [first_pl, second_pl]:
                if player.stamina == 0:
                    result.append(f"Player {player.name} does not have enough stamina.")

            return '\n'.join(result)

    def next_day(self):
        for player in self.players:
            if player.stamina - (player.age * 2) < 0:
                player.stamina = 0
            else:
                player.stamina -= (player.age * 2)

        for player in self.players:
            self.sustain(player.name, "Food")
            self.sustain(player.name, "Drink")

    def __str__(self):
        result = []
        for player in self.players:
            result.append(str(player))

        for supply in self.supplies:
            result.append(supply.details())

        return '\n'.join(result)




















