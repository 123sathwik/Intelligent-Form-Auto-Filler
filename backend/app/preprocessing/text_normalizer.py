import unicodedata

class TextNormalizer:
    @staticmethod
    def normalize_unicode(text: str) -> str:
        """
        Normalizes Unicode characters to standard NFKC normalization form.
        """
        if not text:
            return ""
        return unicodedata.normalize("NFKC", text)
