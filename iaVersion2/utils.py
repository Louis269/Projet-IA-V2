def analyze_input(text):
    positives = ["merci", "bravo", "gentil", "super", "cool"]
    negatives = ["idiot", "nul", "stupide", "mauvais", "bête"]

    score = 0
    lower_text = text.lower()

    for word in positives:
        if word in lower_text:
            score += 0.3

    for word in negatives:
        if word in lower_text:
            score -= 0.3

    return max(-1, min(1, score))