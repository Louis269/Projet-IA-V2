import random
import json
import os
from dictionnaire import reponses

# ================================================
# Mini génératif Markov (pour phrases approximatives)
# ================================================
class MiniGeneratif:
    """
    Cette classe apprend des phrases et peut générer
    des phrases basées sur les mots précédents (Markov).
    """

    def __init__(self):
        self.bigrammes = {}  # Dictionnaire mot -> liste de mots suivants

    def apprendre(self, phrases):
        """
        Apprend des phrases pour alimenter le générateur.
        """
        for phrase in phrases:
            mots = phrase.lower().split()
            for i in range(len(mots)-1):
                if mots[i] not in self.bigrammes:
                    self.bigrammes[mots[i]] = []
                self.bigrammes[mots[i]].append(mots[i+1])

    def generer(self, debut):
        """
        Génère une phrase à partir d'un mot ou d'une phrase initiale.
        """
        mots = debut.lower().split()
        if not mots:
            mots = [random.choice(list(self.bigrammes.keys()))] if self.bigrammes else ["hum..."]

        resultat = mots[:]
        for _ in range(10):  # maximum 10 mots générés
            mot_courant = resultat[-1]
            suivant = self.bigrammes.get(mot_courant)
            if suivant:
                resultat.append(random.choice(suivant))
            else:
                break
        return " ".join(resultat).capitalize() + "."


# ================================================
# Classe principale IA
# ================================================
class IA:
    """
    Classe IA représentant le chatbot.
    - Contient l'humeur de l'IA
    - Contient le dictionnaire de réponses
    - Contient la mémoire persistante
    - Peut générer des phrases approximatives
    """

    def __init__(self):
        self.humeur = 50  # humeur de base (0-100)
        self.reponses = reponses  # dictionnaire des réponses
        self.fichier_memoire = "memoire.json"  # fichier pour sauvegarder l'apprentissage
        self.generateur = MiniGeneratif()  # générateur Markov
        self.charger_memoire()

        # On apprend les phrases existantes du dictionnaire
        for cat in self.reponses.values():
            self.generateur.apprendre(cat["reponses"])

    # -------------------------
    # Gestion mémoire
    # -------------------------
    def charger_memoire(self):
        """Charge la mémoire sauvegardée si elle existe"""
        if os.path.exists(self.fichier_memoire):
            with open(self.fichier_memoire, "r", encoding="utf-8") as f:
                nouvelles_donnees = json.load(f)
                self.reponses.update(nouvelles_donnees)
                # Apprentissage des phrases mémorisées
                for cat in nouvelles_donnees.values():
                    self.generateur.apprendre(cat["reponses"])

    def sauvegarder(self):
        """Sauvegarde le dictionnaire et nouvelles réponses dans le fichier mémoire"""
        with open(self.fichier_memoire, "w", encoding="utf-8") as f:
            json.dump(self.reponses, f, indent=4, ensure_ascii=False)

    # -------------------------
    # Gestion humeur
    # -------------------------
    def ajuster_humeur(self, message):
        """Augmente ou diminue l'humeur selon les mots du message"""
        mots_positifs = ["super", "génial", "cool", "heureux", "merci"]
        mots_negatifs = ["nul", "triste", "déteste", "mauvais"]

        for mot in mots_positifs:
            if mot in message.lower():
                self.humeur += 5
        for mot in mots_negatifs:
            if mot in message.lower():
                self.humeur -= 5

        # On garde l'humeur entre 0 et 100
        self.humeur = max(0, min(100, self.humeur))

    def ton_selon_humeur(self, reponse):
        """Ajoute un emoji selon l'humeur pour rendre le ton plus humain"""
        if self.humeur > 70:
            return reponse + " 😄🔥"
        elif self.humeur < 30:
            return reponse + " 😒"
        else:
            return reponse

    # -------------------------
    # Réponse principale
    # -------------------------
    def repondre(self, message):
        """
        Retourne une réponse à partir du message de l'utilisateur
        - Vérifie le dictionnaire
        - Sinon génère une phrase approximative
        """
        message = message.lower()
        self.ajuster_humeur(message)

        # Cherche une réponse connue
        for categorie in self.reponses.values():
            for mot in categorie["mots"]:
                if mot in message:
                    base = random.choice(categorie["reponses"])
                    return self.ton_selon_humeur(base)

        # Sinon génération Markov
        reponse_gen = self.generateur.generer(message)
        return self.ton_selon_humeur(reponse_gen)


# ================================================
# Programme principal
# ================================================
if __name__ == "__main__":

    ia = IA()
    print("Bienvenue ! Parle avec l'IA générative (tape 'quit' pour arrêter)")

    while True:
        user_input = input("Toi : ")

        if user_input.lower() == "quit":
            print("IA : À bientôt !")
            break

        response = ia.repondre(user_input)
        print("IA :", response)