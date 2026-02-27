from memory import Memory
from personality import Personality
from utils import analyze_input
import random

class Brain:
    def __init__(self):
        self.users = {}

    def ensure_user(self, user_id):
        if user_id not in self.users:
            self.users[user_id] = {
                "memory": Memory(),
                "personality": Personality()
            }

    def receive_message(self, user_id, message):
        self.ensure_user(user_id)

        impact = analyze_input(message)

        self.users[user_id]["memory"].add_experience(message, impact)
        self.users[user_id]["personality"].update(impact)

        return self.generate_response(user_id)

    def generate_response(self, user_id):
        p = self.users[user_id]["personality"]

        # CONTENU (influencé par personnalité)
        if p.curiosity > 0.6:
            base = "Ta remarque m'intrigue."
        elif p.aggressiveness > 0.6:
            base = "Je ne suis pas entièrement convaincu."
        elif p.kindness > 0.6:
            base = "Je trouve cela intéressant, merci de le partager."
        else:
            base = "Je vois ce que tu veux dire."

        # STYLE / NUANCE LITTÉRAIRE
        nuances = []

        if p.trust > 0.7:
            nuances.append("Je me sens assez confiant dans cette réflexion.")
        elif p.trust < 0.3:
            nuances.append("Je reste toutefois prudent dans mon jugement.")

        if p.curiosity > 0.7:
            nuances.append("Il y a quelque chose qui mérite d'être exploré davantage.")

        if p.kindness > 0.7:
            nuances.append("Ta manière de l'exprimer est appréciable.")

        if nuances:
            base += " " + random.choice(nuances)

        return base