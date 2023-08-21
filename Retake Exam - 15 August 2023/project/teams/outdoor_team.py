from project.teams.base_team import BaseTeam


class OutdoorTeam(BaseTeam):
    INCREASED_POINTS = 115

    def __init__(self, name, country, advantage):
        super().__init__(name, country, advantage, budget=1000.0)

    def win(self):
        self.wins += 1
        self.advantage += OutdoorTeam.INCREASED_POINTS