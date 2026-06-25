import logging
from app.preprocessing.text_normalizer import TextNormalizer
from app.preprocessing.text_cleaner import TextCleaner
from app.preprocessing.regex_patterns import (
    EMAIL_WITH_SPACES,
    PHONE_PATTERN,
    DATE_DIGITS,
    DATE_WORDS,
    MONTHS_MAP,
    ARTIFACTS_PATTERN,
    REPEATING_CHARS
)

logger = logging.getLogger("autofiller-backend")

class CleaningService:
    @staticmethod
    def clean_text(text: str) -> str:
        """
        Runs the full text cleaning pipeline:
        1. Unicode normalization (NFKC)
        2. Removes OCR artifacts (| , ~ , _ , \ )
        3. Removes repeating characters like multiple dots or hyphens
        4. Normalizes emails (lowercasing, joining spaces)
        5. Normalizes phone numbers to a clean 10-digit format
        6. Normalizes dates (DD/MM/YYYY or DD Aug YYYY) to YYYY-MM-DD
        7. Cleans spacing, empty lines, and duplicate lines
        """
        if not text:
            return ""

        # 1. Unicode normalization
        text = TextNormalizer.normalize_unicode(text)

        # 2. Remove OCR artifacts (replace |, ~, _, \ with a space)
        text = ARTIFACTS_PATTERN.sub(" ", text)

        # Remove repeating characters like .., ..., ---- with a single space
        text = REPEATING_CHARS.sub(" ", text)

        # 3. Normalize emails (handles spaces like ABC @ Gmail . Com)
        def replace_email(match):
            user = match.group(1).replace(" ", "")
            domain = match.group(2).replace(" ", "")
            tld = match.group(3).replace(" ", "")
            return f"{user}@{domain}.{tld}".lower()
            
        text = EMAIL_WITH_SPACES.sub(replace_email, text)

        # 4. Normalize phone numbers (e.g. +91-98765 43210 -> 9876543210)
        def replace_phone(match):
            matched_str = match.group(0)
            digits = "".join(filter(str.isdigit, matched_str))
            # Extract last 10 digits as standard local number
            if len(digits) >= 10:
                return digits[-10:]
            return digits

        text = PHONE_PATTERN.sub(replace_phone, text)

        # 5. Normalize dates
        # 5a. Slash/Dash formats (DD/MM/YYYY or DD-MM-YYYY)
        text = DATE_DIGITS.sub(
            lambda m: f"{m.group(3)}-{int(m.group(2)):02d}-{int(m.group(1)):02d}", 
            text
        )
        
        # 5b. Word months (DD Aug 2002)
        def replace_word_date(match):
            day = int(match.group(1))
            mon_name = match.group(2).lower()[:3]
            mon = MONTHS_MAP.get(mon_name, "01")
            year = match.group(3)
            return f"{year}-{mon}-{day:02d}"
            
        text = DATE_WORDS.sub(replace_word_date, text)

        # 6. Formatting layout: spaces, blank lines, duplicates
        text = TextCleaner.clean_structure(text)

        return text
