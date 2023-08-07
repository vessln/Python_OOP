from project.band import Band
from project.band_members.drummer import Drummer
from project.band_members.guitarist import Guitarist
from project.band_members.singer import Singer
from project.concert import Concert


class ConcertTrackerApp:
    VALID_MUSICIANS = {"Guitarist": Guitarist,
                       "Drummer": Drummer,
                       "Singer": Singer}

    def __init__(self):
        self.bands = []
        self.musicians = []
        self.concerts = []

    @staticmethod
    def find_object_by_name(name, list_objects):
        return [ob for ob in list_objects if ob.name == name]

    def find_concert_by_place(self, place):
        return [c for c in self.concerts if c.place == place]

    def create_musician(self, musician_type, name, age):
        if musician_type not in self.VALID_MUSICIANS.keys():
            raise ValueError("Invalid musician type!")

        musician = ConcertTrackerApp.find_object_by_name(name, self.musicians)
        if musician:
            current_musician = musician[0]
            raise Exception(f"{current_musician.name} is already a musician!")

        new_musician = self.VALID_MUSICIANS[musician_type](name, age)
        self.musicians.append(new_musician)
        return f"{new_musician.name} is now a {musician_type}."

    def create_band(self, name):
        if ConcertTrackerApp.find_object_by_name(name, self.bands):
            raise Exception(f"{name} band is already created!")

        new_band = Band(name)
        self.bands.append(new_band)
        return f"{name} was created."

    def create_concert(self, genre, audience, ticket_price, expenses, place):
        concert = self.find_concert_by_place(place)
        if concert:
            current_concert = concert[0]
            raise Exception(f"{current_concert.place} is already registered for {current_concert.genre} concert!")

        new_concert = Concert(genre, audience, ticket_price, expenses, place)
        self.concerts.append(new_concert)
        return f"{genre} concert in {place} was added."

    def add_musician_to_band(self, musician_name, band_name):
        musician = ConcertTrackerApp.find_object_by_name(musician_name, self.musicians)
        if not musician:
            raise Exception(f"{musician_name} isn't a musician!")

        band = ConcertTrackerApp.find_object_by_name(band_name, self.bands)
        if not band:
            raise Exception(f"{band_name} isn't a band!")

        current_musician = musician[0]
        current_band = band[0]
        current_band.members.append(current_musician)
        return f"{current_musician.name} was added to {current_band.name}."

    def remove_musician_from_band(self, musician_name, band_name):
        band = ConcertTrackerApp.find_object_by_name(band_name, self.bands)
        if not band:
            raise Exception(f"{band_name} isn't a band!")

        current_band = band[0]

        musician = [m for m in current_band.members if m.name == musician_name]
        if not musician:
            raise Exception(f"{musician_name} isn't a member of {current_band.name}!")

        current_musician = musician[0]
        if current_musician not in current_band.members:
            raise Exception(f"{musician_name} isn't a musician!")

        current_band.members.remove(current_musician)
        return f"{musician_name} was removed from {band_name}."

    def start_concert(self, concert_place, band_name):
        concert = self.find_concert_by_place(concert_place)[0]
        band = ConcertTrackerApp.find_object_by_name(band_name, self.bands)[0]
        members_in_band_by_type = [type(m).__name__ for m in band.members]

        if "Singer" not in members_in_band_by_type or \
            "Drummer" not in members_in_band_by_type or \
                "Guitarist" not in members_in_band_by_type:
            raise Exception(f"{band.name} can't start the concert because it doesn't have enough members!")

        for member in band.members:
            if not member.check_needed_skills(concert.genre):
                raise Exception(f"The {band.name} band is not ready to play at the concert!")

        profit = (concert.audience * concert.ticket_price) - concert.expenses
        return f"{band.name} gained {profit:.2f}$ from the {concert.genre} concert in {concert.place}."


