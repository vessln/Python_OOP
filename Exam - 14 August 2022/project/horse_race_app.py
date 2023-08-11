from project.horse_race import HorseRace
from project.horse_specification.appaloosa import Appaloosa
from project.horse_specification.thoroughbred import Thoroughbred
from project.jockey import Jockey


class HorseRaceApp:
    VALID_HORSE_BREEDS = {"Appaloosa": Appaloosa,
                          "Thoroughbred": Thoroughbred}

    def __init__(self):
        self.horses = []
        self.jockeys = []
        self.horse_races = []

    @staticmethod
    def find_object_by_name(name, list_objects):
        return [ob for ob in list_objects if ob.name == name]

    def find_race_by_type(self, r_type):
        return [r for r in self.horse_races if r.race_type == r_type]

    def find_horse_by_type(self, h_type):
        return [h for h in self.horses if type(h).__name__ == h_type]

    def add_horse(self, horse_type, horse_name, horse_speed):
        if self.find_object_by_name(horse_name, self.horses):
            raise Exception(f"Horse {horse_name} has been already added!")

        if horse_type in self.VALID_HORSE_BREEDS.keys():
            new_horse = self.VALID_HORSE_BREEDS[horse_type](horse_name, horse_speed)
            self.horses.append(new_horse)
            return f"{horse_type} horse {horse_name} is added."

    def add_jockey(self, jockey_name, age):
        if self.find_object_by_name(jockey_name, self.jockeys):
            raise Exception(f"Jockey {jockey_name} has been already added!")

        new_jockey = Jockey(jockey_name, age)
        self.jockeys.append(new_jockey)
        return f"Jockey {jockey_name} is added."

    def create_horse_race(self, race_type):
        if self.find_race_by_type(race_type):
            raise Exception(f"Race {race_type} has been already created!")

        new_race = HorseRace(race_type)
        self.horse_races.append(new_race)
        return f"Race {race_type} is created."

    def add_horse_to_jockey(self, jockey_name, horse_type):
        given_jockey = self.find_object_by_name(jockey_name, self.jockeys)
        if not given_jockey:
            raise Exception(f"Jockey {jockey_name} could not be found!")

        given_horse = [h for h in self.horses if type(h).__name__ == horse_type and not h.is_taken]

        if not given_horse:
            raise Exception(f"Horse breed {horse_type} could not be found!")

        current_jockey = given_jockey[0]
        current_horse = given_horse[-1]

        if current_jockey.horse:
            return f"Jockey {jockey_name} already has a horse."

        current_horse.is_taken = True
        current_jockey.horse = current_horse
        return f"Jockey {jockey_name} will ride the horse {current_horse.name}."

    def add_jockey_to_horse_race(self, race_type, jockey_name):
        current_race = self.find_race_by_type(race_type)
        if not current_race:
            raise Exception(f"Race {race_type} could not be found!")

        current_jockey = self.find_object_by_name(jockey_name, self.jockeys)
        if not current_jockey:
            raise Exception(f"Jockey {jockey_name} could not be found!")

        race = current_race[0]
        jockey = current_jockey[0]

        if not jockey.horse:
            raise Exception(f"Jockey {jockey_name} cannot race without a horse!")

        if jockey in race.jockeys:
            return f"Jockey {jockey_name} has been already added to the {race_type} race."

        race.jockeys.append(jockey)
        return f"Jockey {jockey_name} added to the {race_type} race."

    def start_horse_race(self, race_type):
        current_race = self.find_race_by_type(race_type)

        if not current_race:
            raise Exception(f"Race {race_type} could not be found!")

        race = current_race[0]

        if len(race.jockeys) < 2:
            raise Exception(f"Horse race {race_type} needs at least two participants!")

        winner = sorted(race.jockeys, key=lambda x: -x.horse.speed)[0]
        highest_speed = winner.horse.speed
        horse_name = winner.horse.name

        return f"The winner of the {race_type} race, with a speed of " \
               f"{highest_speed}km/h is {winner.name}! Winner's horse: {horse_name}."






