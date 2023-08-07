from project.band_members.musician import Musician


class Drummer(Musician):
    NEEDED_SKILLS = {"Rock": "play the drums with drumsticks",
                     "Metal": "play the drums with drumsticks",
                     "Jazz": "play the drums with drum brushes"}

    RECOMMENDED_SKILLS = ["play the drums with drumsticks",
                          "play the drums with drum brushes",
                          "read sheet music"]

    def learn_new_skill(self, new_skill):
        if new_skill not in self.RECOMMENDED_SKILLS:
            raise ValueError(f"{new_skill} is not a needed skill!")

        if new_skill in self.skills:
            raise Exception(f"{new_skill} is already learned!")

        self.skills.append(new_skill)
        return f"{self.name} learned to {new_skill}."

    def check_needed_skills(self, concert_type):
        if self.NEEDED_SKILLS[concert_type] not in self.skills:
            return False

        return True


