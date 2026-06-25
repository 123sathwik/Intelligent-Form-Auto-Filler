import re

class TextCleaner:
    @staticmethod
    def clean(text: str) -> str:
        """
        Cleans and normalizes text:
        - Removes extra spaces/tabs
        - Removes duplicate lines (preserving first occurrence)
        - Removes blank lines
        - Normalizes emails (lowercases them)
        - Normalizes phone numbers to (XXX) XXX-XXXX or +1 (XXX) XXX-XXXX
        - Normalizes dates to YYYY-MM-DD
        """
        if not text:
            return ""

        # 1. Split into lines
        lines = text.splitlines()
        
        # 2. Clean spaces, remove blank and duplicate lines
        seen_lines = set()
        cleaned_lines = []
        
        for line in lines:
            # Replace multiple spaces/tabs with a single space, and strip edges
            trimmed = re.sub(r'[ \t]+', ' ', line).strip()
            if trimmed:
                if trimmed not in seen_lines:
                    seen_lines.add(trimmed)
                    cleaned_lines.append(trimmed)

        cleaned_text = "\n".join(cleaned_lines)

        # 3. Normalize emails (find matches and lowercase them)
        email_regex = r'\b([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)\b'
        cleaned_text = re.sub(email_regex, lambda m: m.group(1).lower().strip(), cleaned_text)

        # 4. Normalize phone numbers
        # Matches: 123-456-7890, (123) 456-7890, +1 123 456 7890, 123.456.7890, etc.
        phone_regex = r'(?<!\d)(\+?1?[-.\s]?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4})\b'
        def normalize_phone(match):
            digits = "".join(filter(str.isdigit, match.group(1)))
            if len(digits) == 10:
                return f"({digits[:3]}) {digits[3:6]}-{digits[6:]}"
            elif len(digits) == 11 and digits[0] == '1':
                return f"+1 ({digits[1:4]}) {digits[4:7]}-{digits[7:]}"
            return match.group(1)
            
        cleaned_text = re.sub(phone_regex, normalize_phone, cleaned_text)

        # 5. Normalize dates
        # MM/DD/YYYY or MM-DD-YYYY to YYYY-MM-DD (e.g. 06/25/2026 -> 2026-06-25)
        date_us_regex = r'\b(0?[1-9]|1[0-2])[-/](0?[1-9]|[12]\d|3[01])[-/](\d{4})\b'
        cleaned_text = re.sub(
            date_us_regex, 
            lambda m: f"{m.group(3)}-{int(m.group(1)):02d}-{int(m.group(2)):02d}", 
            cleaned_text
        )

        # YYYY/MM/DD or YYYY-MM-DD to YYYY-MM-DD (already standard format, handles slashes to dashes conversion)
        date_iso_regex = r'\b(\d{4})[-/](0?[1-9]|1[0-2])[-/](0?[1-9]|[12]\d|3[01])\b'
        cleaned_text = re.sub(
            date_iso_regex, 
            lambda m: f"{m.group(1)}-{int(m.group(2)):02d}-{int(m.group(3)):02d}", 
            cleaned_text
        )

        return cleaned_text
