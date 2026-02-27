from brain import Brain
import pyttsx3

ai = Brain()

print("Bienvenue ! Tape 'quit' pour arrêter.")
user_id = input("Quel est ton nom ? ")

# Choix voix
voice_choice = input("Veux-tu que l'IA parle à voix haute ? (oui/non) : ").lower()
use_voice = voice_choice == "oui"

if use_voice:
    engine = pyttsx3.init()

    voices = engine.getProperty('voices')

    # Afficher les voix disponibles
    print("\nVoix disponibles :")
    for index, voice in enumerate(voices):
        print(index, "-", voice.name)

    choice = int(input("Choisis l'index de la voix : "))
    engine.setProperty('voice', voices[choice].id)

    engine.setProperty('rate', 150)    # vitesse
    engine.setProperty('volume', 1.0)  # volume

while True:
    user_input = input(f"{user_id} : ")

    if user_input.lower() == "quit":
        print("IA : À bientôt !")
        if use_voice:
            engine.say("À bientôt !")
            engine.runAndWait()
        break

    response = ai.receive_message(user_id, user_input)

    print("IA :", response)

    if use_voice:
        engine.say(response)
        engine.runAndWait()