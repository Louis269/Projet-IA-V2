class Personality:
    def __init__(self):
        self.kindness = 0.5
        self.aggressiveness = 0.5
        self.curiosity = 0.5
        self.trust = 0.5

    def update(self, impact):
        # IA influençable (évolution assez rapide)
        self.kindness = min(1.0, max(0.0, self.kindness + 0.3 * impact))
        self.aggressiveness = min(1.0, max(0.0, self.aggressiveness - 0.2 * impact))
        self.curiosity = min(1.0, max(0.0, self.curiosity + 0.2 * impact))
        self.trust = min(1.0, max(0.0, self.trust + 0.2 * impact))