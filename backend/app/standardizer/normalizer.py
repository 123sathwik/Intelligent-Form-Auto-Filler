import re
from datetime import datetime
from typing import List, Any

class Normalizer:
    @staticmethod
    def normalize_name(value: Any) -> str:
        """Title cases names."""
        if not value:
            return ""
        return str(value).strip().title()

    @staticmethod
    def normalize_gender(value: Any) -> str:
        """Standardizes gender to Male, Female, or Other."""
        if not value:
            return ""
        val = str(value).strip().lower()
        if val.startswith("m"):
            return "Male"
        if val.startswith("f"):
            return "Female"
        if val.startswith("o"):
            return "Other"
        return val.capitalize()

    @staticmethod
    def normalize_date(value: Any) -> str:
        """Translates dates into standard YYYY-MM-DD ISO format."""
        if not value:
            return ""
        val_clean = str(value).strip()
        
        # If it matches ISO format, return it
        if re.match(r'^\d{4}-\d{2}-\d{2}$', val_clean):
            return val_clean
            
        formats = [
            ("%d/%m/%Y", "%Y-%m-%d"),
            ("%d-%m-%Y", "%Y-%m-%d"),
            ("%m/%d/%Y", "%Y-%m-%d"),
            ("%Y/%m/%d", "%Y-%m-%d"),
            ("%d %b %Y", "%Y-%m-%d"),
            ("%d %B %Y", "%Y-%m-%d"),
        ]
        
        for fmt_in, fmt_out in formats:
            try:
                dt = datetime.strptime(val_clean, fmt_in)
                return dt.strftime(fmt_out)
            except ValueError:
                continue
                
        return val_clean

    @staticmethod
    def normalize_age(value: Any) -> str:
        """Extracts the numeric age from text (e.g. '25 years' -> '25')."""
        if not value:
            return ""
        digits = "".join(filter(str.isdigit, str(value)))
        return digits[:2] if digits else str(value).strip()

    @staticmethod
    def normalize_cgpa(value: Any) -> str:
        """Extracts floating point CGPA (e.g., '9.4 GPA' -> '9.4')."""
        if not value:
            return ""
        val_str = str(value).strip()
        # Find values like 9.4, 8.5, 10, 10.0
        match = re.search(r'\b([1-9]\.\d{1,2}|10(?:\.0)?)\b', val_str)
        if match:
            return match.group(1)
        return val_str

    @staticmethod
    def normalize_percentage(value: Any) -> str:
        """Extracts numeric percentage (e.g., '94%' -> '94')."""
        if not value:
            return ""
        val_str = str(value).strip()
        match = re.search(r'\b(\d{1,2}(?:\.\d{1,2})?)\b', val_str)
        if match:
            return match.group(1)
        return val_str

    @staticmethod
    def normalize_list(value: Any) -> List[str]:
        """Converts strings, arrays, or text entries into clean string arrays."""
        if not value:
            return []
        if isinstance(value, list):
            return [str(item).strip() for item in value if str(item).strip()]
        if isinstance(value, str):
            if "\n" in value:
                items = value.split("\n")
            elif "," in value:
                items = value.split(",")
            elif ";" in value:
                items = value.split(";")
            else:
                items = [value]
            return [item.strip() for item in items if item.strip()]
        return [str(value).strip()]

    @staticmethod
    def normalize_experience(value: Any) -> str:
        """Stringifies experiences lists if they arrive as arrays."""
        if not value:
            return ""
        if isinstance(value, list):
            # Filter headers and empty items
            cleaned = []
            for item in value:
                item_str = str(item).strip()
                if item_str and item_str.upper() not in ["EXPERIENCE", "WORK EXPERIENCE"]:
                    cleaned.append(item_str)
            return "; ".join(cleaned)
        return str(value).strip()
