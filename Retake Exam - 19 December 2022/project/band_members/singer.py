from project.band_members.musician import Musician


class Singer(Musician):
    RECOMMENDED_SKILLS = {"Rock": "sing high pitch notes",
                          "Metal": "sing low pitch notes"}

    def learn_new_skill(self, new_skill):
        if new_skill not in self.RECOMMENDED_SKILLS.values():
            raise ValueError(f"{new_skill} is not a needed skill!")

        if new_skill in self.skills:
            raise Exception(f"{new_skill} is already learned!")

        self.skills.append(new_skill)
        return f"{self.name} learned to {new_skill}."

    def check_needed_skills(self, concert_type):
        if concert_type == "Jazz":
            if "sing low pitch notes" not in self.skills or "sing high pitch notes" not in self.skills:
                return False
            return True

        else:
            if self.RECOMMENDED_SKILLS[concert_type] not in self.skills:
                return False
            return True

