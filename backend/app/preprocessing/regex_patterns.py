import re

# Email with optional horizontal spaces around @ and . (does not match newlines)
# Matches: ABC @ Gmail . Com, abc@gmail.com, support @ company.co.uk
EMAIL_WITH_SPACES = re.compile(
    r'\b([a-zA-Z0-9_.+-]+(?:[ \t]+[a-zA-Z0-9_.+-]+)*)[ \t]*@[ \t]*([a-zA-Z0-9-]+(?:[ \t]+[a-zA-Z0-9-]+)*)[ \t]*\.[ \t]*([a-zA-Z0-9-.]+(?:[ \t]+[a-zA-Z0-9-.]+)*)\b'
)

# Phone number pattern supporting standard format and 5-and-5 layout (+91-98765 43210)
PHONE_PATTERN = re.compile(
    r'(?<!\d)(\+?\d{1,3}[-.\s]?)?(?:\d{5}[-.\s]?\d{5}|\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4})\b'
)

# Date patterns
# 1. Digits: DD/MM/YYYY or DD-MM-YYYY (e.g. 12/08/2002)
DATE_DIGITS = re.compile(
    r'\b(0?[1-9]|[12]\d|3[01])[-/](0?[1-9]|1[0-2])[-/](\d{4})\b'
)

# 2. Words: DD Aug 2002, DD August 2002, DD-Aug-2002
DATE_WORDS = re.compile(
    r'\b(0?[1-9]|[12]\d|3[01])[-/\s]+(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*[-/\s]+(\d{4})\b',
    re.IGNORECASE
)

MONTHS_MAP = {
    "jan": "01", "feb": "02", "mar": "03", "apr": "04", "may": "05", "jun": "06",
    "jul": "07", "aug": "08", "sep": "09", "oct": "10", "nov": "11", "dec": "12"
}

# OCR symbols to remove: |, ~, _, \
ARTIFACTS_PATTERN = re.compile(r'[|~_\\]')

# Repeating dots/hyphens to clean: .., ..., ----
REPEATING_CHARS = re.compile(r'\.{2,}|-{2,}')
