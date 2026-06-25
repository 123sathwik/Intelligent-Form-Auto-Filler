import re

class RegexExtractor:
    @staticmethod
    def extract(text: str) -> dict:
        """
        Extracts pattern-based entities from raw/cleaned text using regex.
        Returns a dict of extracted values.
        """
        entities = {}

        # 1. Email Address
        email_match = re.search(r'\b[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+\b', text)
        entities["email"] = email_match.group(0) if email_match else ""

        # 2. Phone Number
        phone_match = re.search(
            r'\b(\+?\d{1,3}[-.\s]?)?(?:\d{5}[-.\s]?\d{5}|\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4})\b', 
            text
        )
        if phone_match:
            digits = "".join(filter(str.isdigit, phone_match.group(0)))
            entities["phone_number"] = digits[-10:] if len(digits) >= 10 else digits
        else:
            entities["phone_number"] = ""

        # 3. LinkedIn URL
        linkedin_match = re.search(
            r'(?:https?://)?(?:www\.)?linkedin\.com/in/[a-zA-Z0-9_-]+/?', 
            text, 
            re.IGNORECASE
        )
        entities["linkedin"] = linkedin_match.group(0).strip() if linkedin_match else ""

        # 4. GitHub URL
        github_match = re.search(
            r'(?:https?://)?(?:www\.)?github\.com/[a-zA-Z0-9_-]+/?', 
            text, 
            re.IGNORECASE
        )
        entities["github"] = github_match.group(0).strip() if github_match else ""

        # 5. General Website
        # Use negative lookbehind (?<!@) to avoid matching email domains (e.g. gmail.com in abc@gmail.com)
        website_matches = re.finditer(
            r'(?<!@)\b(?:https?://)?(?:www\.)?[a-zA-Z0-9-]+\.[a-z]{2,6}(?:/[a-zA-Z0-9_.-]*)*\b', 
            text, 
            re.IGNORECASE
        )
        website_url = ""
        for match in website_matches:
            url = match.group(0).strip()
            if "linkedin.com" not in url.lower() and "github.com" not in url.lower():
                website_url = url
                break
        entities["website"] = website_url

        # 6. Aadhaar Number (12 digits, often formatted as 4-4-4)
        aadhaar_match = re.search(r'\b\d{4}\s\d{4}\s\d{4}\b|\b\d{12}\b', text)
        entities["aadhaar_number"] = aadhaar_match.group(0).strip() if aadhaar_match else ""

        # 7. PAN Number (5 letters, 4 digits, 1 letter)
        pan_match = re.search(r'\b[A-Z]{5}\d{4}[A-Z]\b', text)
        entities["pan_number"] = pan_match.group(0).strip() if pan_match else ""

        # 8. Passport Number (Indian: 1 letter + 7 digits, or generic)
        passport_match = re.search(
            r'\b[A-Z]\d{7}\b|\b[A-PR-WY-Z][1-9]\d\s?\d{4}[1-9]\b', 
            text, 
            re.IGNORECASE
        )
        entities["passport_number"] = passport_match.group(0).upper().strip() if passport_match else ""

        # 9. Pincode (6 digits for India, avoiding hyphenated registration numbers like REG-998822)
        pincode_match = re.search(r'(?<![A-Za-z-])\b\d{6}\b', text)
        entities["pincode"] = pincode_match.group(0).strip() if pincode_match else ""

        # Helper for label-based extractions (IDs/numbers)
        def search_labeled_pattern(patterns, source_text):
            for pat in patterns:
                match = re.search(pat, source_text, re.IGNORECASE)
                if match and len(match.groups()) > 0:
                    return match.group(1).strip()
            return ""

        # 10. Visa Number
        entities["visa_number"] = search_labeled_pattern(
            [r'\bvisa\s*(?:no\.?|num(?:ber)?)?\s*:\s*([a-z0-9-]+)\b', r'\bvisa\s+([a-z0-9-]+)\b'],
            text
        )

        # 11. Driving License Number
        dl_match = re.search(r'\b[A-Z]{2}\d{13}\b', text, re.IGNORECASE)
        entities["driving_license_number"] = dl_match.group(0).upper().strip() if dl_match else search_labeled_pattern(
            [r'\bdl\s*(?:no\.?|num(?:ber)?)?\s*:\s*([a-z0-9-]+)\b', r'\bdriving\s+licen[sc]e\s*(?:no\.?|num(?:ber)?)?\s*:\s*([a-z0-9-]+)\b'],
            text
        )

        # 12. Invoice Number
        entities["invoice_number"] = search_labeled_pattern(
            [
                r'\binvoice\s*(?:no\.?|num(?:ber)?)?\s*:\s*([a-z0-9-]+)\b',
                r'\binv-[a-z0-9-]+\b', # Match INV-XXXX formats
                r'\bbill\s*(?:no\.?|num(?:ber)?)?\s*:\s*([a-z0-9-]+)\b'
            ],
            text
        )

        # 13. Employee ID
        entities["employee_id"] = search_labeled_pattern(
            [
                r'\bemp(?:loyee)?\s*(?:id|code)?\s*:\s*([a-z0-9-]+)\b',
                r'\bstaff\s*(?:id|code)?\s*:\s*([a-z0-9-]+)\b'
            ],
            text
        )

        # 14. Roll Number
        entities["roll_number"] = search_labeled_pattern(
            [
                r'\broll\s*(?:no\.?|num(?:ber)?)?\s*:\s*([a-z0-9-]+)\b',
                r'\brollno\s*:\s*([a-z0-9-]+)\b'
            ],
            text
        )

        # 15. Registration Number
        entities["registration_number"] = search_labeled_pattern(
            [
                r'\breg(?:istration)?\s*(?:no\.?|num(?:ber)?)?\s*:\s*([a-z0-9-]+)\b',
                r'\bregno\s*:\s*([a-z0-9-]+)\b'
            ],
            text
        )

        return entities
