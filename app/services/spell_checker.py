from spellchecker import SpellChecker

class SpellCorrector:
    def __init__(self):
        self.spell = SpellChecker()
        # Add custom words if needed
        self.spell.word_frequency.load_words(['wifi', 'login', 'portal', 'chatbot', 'faq', 'admin'])

    def correct_text(self, text: str) -> str:
        words = text.split()
        corrected_words = []
        for word in words:
            # Get the one `most likely` answer
            corrected = self.spell.correction(word)
            # If correction is None (word is correct or unknown), use original
            corrected_words.append(corrected if corrected else word)
        return " ".join(corrected_words)

spell_corrector = SpellCorrector()
