import re

class TextCleaner:
    @staticmethod
    def clean_structure(text: str) -> str:
        """
        Cleans structural layout of text:
        - Removes extra duplicate whitespaces
        - Removes empty lines
        - Removes duplicate lines (preserving document order)
        """
        if not text:
            return ""

        lines = text.splitlines()
        seen = set()
        cleaned_lines = []

        for line in lines:
            # Replace multiple whitespaces/tabs with a single space and strip edges
            cleaned_line = re.sub(r'\s+', ' ', line).strip()
            if cleaned_line:  # Remove empty lines
                if cleaned_line not in seen:  # Remove duplicate lines
                    seen.add(cleaned_line)
                    cleaned_lines.append(cleaned_line)

        return "\n".join(cleaned_lines)
