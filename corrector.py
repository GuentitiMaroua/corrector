from langdetect import detect
from spellchecker import SpellChecker
from autocorrect import Speller
import language_tool_python

# Language tools
tool_en = language_tool_python.LanguageTool('en-US')
tool_fr = language_tool_python.LanguageTool('fr-FR')

# Spell checkers
spell_en = SpellChecker(language='en')
spell_fr = Speller(lang='fr')

def correct_text(text):
    if not text.strip():
        return ""

    lang = detect(text)
    print(f"Detected language: {lang}")

    if lang == 'fr':
        # Step 1: spelling correction
        corrected = spell_fr(text)
        # Step 2: grammar correction
        matches = tool_fr.check(corrected)
        corrected = language_tool_python.utils.correct(corrected, matches)
    else:
        # Step 1: spelling correction
        words = text.split()
        corrected_words = [spell_en.correction(w) or w for w in words]
        corrected = " ".join(corrected_words)
        # Step 2: grammar correction
        matches = tool_en.check(corrected)
        corrected = language_tool_python.utils.correct(corrected, matches)

    return corrected
