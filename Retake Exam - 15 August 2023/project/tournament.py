from project.equipment.elbow_pad import ElbowPad
from project.equipment.knee_pad import KneePad
from project.teams.indoor_team import IndoorTeam
from project.teams.outdoor_team import OutdoorTeam


class Tournament:
    VALID_EQUIPMENTS = {"KneePad": KneePad, "ElbowPad": ElbowPad}
    VALID_TEAMS = {"OutdoorTeam": OutdoorTeam, "IndoorTeam": IndoorTeam}

    def __init__(self, name, capacity):
        self.name = name
        self.capacity = capacity
        self.equipment = []
        self.teams = []

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        if not value.isalnum():
            raise ValueError("Tournament name should contain letters and digits only!")
        self.__name = value

    def find_team_by_name(self, team_name):
        return [t for t in self.teams if t.name == team_name]

    def find_team_by_type(self, team_type):
        return [t for t in self.teams if type(t).__name__ == team_type]

    def find_equip_by_type(self, eq_type):
        return [e for e in self.equipment if type(e).__name__ == eq_type]

    def add_equipment(self, equipment_type):
        if equipment_type not in self.VALID_EQUIPMENTS.keys():
            raise Exception("Invalid equipment type!")

        new_equipment = self.VALID_EQUIPMENTS[equipment_type]()
        self.equipment.append(new_equipment)
        return f"{equipment_type} was successfully added."

    def add_team(self, team_type, team_name, country, advantage):
        if team_type not in self.VALID_TEAMS.keys():
            raise Exception("Invalid team type!")

        if self.capacity <= len(self.teams):
            return f"Not enough tournament capacity."

        new_team = self.VALID_TEAMS[team_type](team_name, country, advantage)
        self.teams.append(new_team)
        return f"{team_type} was successfully added."

    def sell_equipment(self, equipment_type, team_name):
        team = self.find_team_by_name(team_name)[0]
        equip = self.find_equip_by_type(equipment_type)[-1]

        if team.budget < equip.price:
            raise Exception("Budget is not enough!")

        self.equipment.remove(equip)
        team.equipment.append(equip)
        team.budget -= equip.price
        return f"Successfully sold {equipment_type} to {team_name}."

    def remove_team(self, team_name):
        team = self.find_team_by_name(team_name)

        if not team:
            raise Exception("No such team!")

        current_team = team[0]

        if current_team.wins > 0:
            raise Exception(f"The team has {current_team.wins} wins! Removal is impossible!")
        else:
            self.teams.remove(current_team)
            return f"Successfully removed {team_name}."

    def increase_equipment_price(self, equipment_type):
        needed_equipments = self.find_equip_by_type(equipment_type)

        for eq in needed_equipments:
            eq.increase_price()

        return f"Successfully changed {len(needed_equipments)}pcs of equipment."

    def play(self, team_name1, team_name2):
        team_1 = self.find_team_by_name(team_name1)[0]
        team_2 = self.find_team_by_name(team_name2)[0]

        if type(team_1).__name__ != type(team_2).__name__:
            raise Exception("Game cannot start! Team types mismatch!")

        points_team_1 = team_1.get_total_points()
        points_team_2 = team_2.get_total_points()

        if points_team_1 == points_team_2:
            return "No winner in this game."

        winner = team_1 if points_team_1 > points_team_2 else team_2
        winner.win()
        return f"The winner is {winner.name}."

    def get_statistics(self):
        result = [f"Tournament: {self.name}"]
        result.append(f"Number of Teams: {len(self.teams)}")
        result.append("Teams:")

        for team in sorted(self.teams, key=lambda x: -x.wins):
            result.append(team.get_statistics())

        return '\n'.join(result)

