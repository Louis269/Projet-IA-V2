class Memory:
    def __init__(self):
        self.experiences = []

    def add_experience(self, message, impact):
        self.experiences.append((message, impact))

        # Limite mémoire à 100 souvenirs
        if len(self.experiences) > 100:
            self.experiences.pop(0)

    def get_recent_impact(self):
        if not self.experiences:
            return 0

        recent = self.experiences[-5:]
        return sum(impact for _, impact in recent) / len(recent)