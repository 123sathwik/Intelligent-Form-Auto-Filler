import re
import spacy
import logging
from pathlib import Path
from app.nlp.custom_rules import COMMON_SKILLS

logger = logging.getLogger("autofiller-backend")

_nlp = None

def get_spacy_nlp():
    global _nlp
    if _nlp is None:
        logger.info("Loading spaCy model 'en_core_web_sm'...")
        try:
            _nlp = spacy.load("en_core_web_sm")
        except Exception as e:
            logger.error(f"Failed to load spaCy model: {str(e)}")
            # Fallback if download was not processed
            raise RuntimeError(f"spaCy model 'en_core_web_sm' not loaded: {str(e)}")
    return _nlp

class EntityExtractor:
    @staticmethod
    def extract(text: str) -> dict:
        """
        Extracts NLP-based entities (Name, Organization, Company, College, University, GPE locations)
        using spaCy NER, supplemented by robust lexicons and layout heuristics.
        """
        entities = {
            "person_name": "",
            "organization": "",
            "company": "",
            "college": "",
            "university": "",
            "address": "",
            "city": "",
            "state": "",
            "country": ""
        }
        
        if not text:
            return entities

        nlp = get_spacy_nlp()
        doc = nlp(text)

        # 1. Extract Person Name
        person_entities = [ent.text.strip() for ent in doc.ents if ent.label_ == "PERSON"]
        
        # Candidate name heuristic check for the top 3 non-empty lines:
        first_line_name = ""
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        for line in lines[:3]:
            cleaned_line = re.sub(r'[:;,]+$', '', line).strip()
            words = cleaned_line.split()
            if 2 <= len(words) <= 4:
                # No numbers, no symbols
                if re.match(r'^[A-Za-z. \t]+$', cleaned_line):
                    cleaned_lower = cleaned_line.lower()
                    keywords = {
                        "resume", "cv", "curriculum", "vitae", "summary", "profile", "contact", 
                        "email", "phone", "address", "page", "developer", "engineer", "designer", 
                        "manager", "architect", "analyst", "student", "candidate", "about", "me",
                        "experience", "education", "skills", "projects", "certifications", "objective",
                        "card", "passport", "visa", "invoice", "receipt", "bill", "license", "aadhaar", 
                        "pan", "driving", "employee", "id", "form", "certify", "certificate", "certification", 
                        "university", "college", "school", "institute", "application", "details", "government", 
                        "india", "state", "dept", "department", "ministry", "board", "national", "union", 
                        "republic", "office", "authority", "division"
                    }
                    if not any(k in cleaned_lower for k in keywords):
                        first_line_name = cleaned_line.title()
                        break

        if first_line_name:
            entities["person_name"] = first_line_name
        elif person_entities:
            valid_names = [name for name in person_entities if len(name.split()) >= 2 and "\n" not in name]
            if valid_names:
                entities["person_name"] = valid_names[0]
            else:
                entities["person_name"] = person_entities[0]

        # 2. Extract ORG entities (Organization, Company, College, University)
        orgs = [
            clean_org for clean_org in [
                ent.text.strip().split("\n")[0].strip() for ent in doc.ents if ent.label_ == "ORG"
            ] if clean_org
        ]
        
        universities = []
        colleges = []
        companies = []
        general_orgs = []

        # Exclude generic words and common skills from ORG entities
        generic_org_words = {
            "software", "engineer", "developer", "designer", "manager", "architect", "analyst", 
            "project", "program", "team", "computer", "science", "information", "technology", 
            "engineering", "skills", "experience", "education", "projects", "certifications", 
            "objective", "resume", "cv", "profile", "summary", "personal", "details", "contact",
            "certifications", "certified", "pan", "aadhaar", "passport", "visa", "invoice", "dl", "id", "card"
        }
        for skill in COMMON_SKILLS:
            generic_org_words.add(skill.lower())

        for org in orgs:
            org_lower = org.lower().strip()
            # Skip if it is too short or is a generic role/section header
            if len(org_lower) <= 2 or org_lower in generic_org_words:
                continue
            if "university" in org_lower or "univ" in org_lower:
                universities.append(org)
            elif any(k in org_lower for k in ["college", "institute", "school", "academy", "iit", "nit", "bits"]):
                colleges.append(org)
            elif any(k in org_lower for k in ["ltd", "inc", "corp", "company", "limited", "technologies", "solutions", "services", "labs"]):
                companies.append(org)
            else:
                general_orgs.append(org)

        entities["university"] = universities[0] if universities else ""
        entities["college"] = colleges[0] if colleges else ""
        entities["company"] = companies[0] if companies else ""
        entities["organization"] = general_orgs[0] if general_orgs else (entities["company"] or entities["university"] or "")

        # 3. Extract Locations (GPE, LOC) with Lexicon lookups
        gpes = [
            clean_gpe for clean_gpe in [
                ent.text.strip().split("\n")[0].strip() for ent in doc.ents if ent.label_ in ["GPE", "LOC"]
            ] if clean_gpe
        ]
        
        country_lexicon = {
            "india": "India", "usa": "USA", "united states": "USA", "united states of america": "USA",
            "uk": "UK", "united kingdom": "UK", "canada": "Canada", "australia": "Australia",
            "germany": "Germany", "france": "France", "japan": "Japan"
        }
        
        state_lexicon = {
            "california": "California", "ca": "California",
            "texas": "Texas", "tx": "Texas",
            "new york": "New York", "ny": "New York",
            "florida": "Florida", "fl": "Florida",
            "washington": "Washington", "wa": "Washington",
            "illinois": "Illinois", "il": "Illinois",
            "massachusetts": "Massachusetts", "ma": "Massachusetts",
            "andhra pradesh": "Andhra Pradesh", "ap": "Andhra Pradesh",
            "telangana": "Telangana", "ts": "Telangana", "tg": "Telangana",
            "karnataka": "Karnataka", "ka": "Karnataka",
            "maharashtra": "Maharashtra", "mh": "Maharashtra",
            "tamil nadu": "Tamil Nadu", "tn": "Tamil Nadu",
            "delhi": "Delhi", "dl": "Delhi",
            "haryana": "Haryana", "hr": "Haryana",
            "uttar pradesh": "Uttar Pradesh", "up": "Uttar Pradesh",
            "west bengal": "West Bengal", "wb": "West Bengal",
            "gujarat": "Gujarat", "gj": "Gujarat",
            "rajasthan": "Rajasthan", "rj": "Rajasthan",
            "punjab": "Punjab", "pb": "Punjab"
        }

        found_country = ""
        found_state = ""

        # Disambiguate entities tagged as GPE by spaCy
        for gpe in gpes:
            gpe_lower = gpe.lower()
            if gpe_lower in country_lexicon:
                found_country = country_lexicon[gpe_lower]
            elif gpe_lower in state_lexicon:
                found_state = state_lexicon[gpe_lower]

        # Scan text if country not resolved
        if not found_country:
            for country_key, country_val in country_lexicon.items():
                if len(country_key) > 3:
                    if re.search(r'\b' + re.escape(country_key) + r'\b', text, re.IGNORECASE):
                        found_country = country_val
                        break
            if not found_country:
                abbrev_match = re.search(r'\b(USA|UK|IND|CAN|AUS)\b', text)
                if abbrev_match:
                    abbrev = abbrev_match.group(1)
                    if abbrev == "IND":
                        found_country = "India"
                    else:
                        found_country = country_lexicon.get(abbrev.lower(), abbrev)

        # Scan text if state not resolved
        if not found_state:
            for state_key, state_val in state_lexicon.items():
                if len(state_key) > 2:
                    if re.search(r'\b' + re.escape(state_key) + r'\b', text, re.IGNORECASE):
                        found_state = state_val
                        break
            if not found_state:
                state_abbrev_match = re.search(
                    r'\b(CA|NY|TX|FL|WA|IL|MA|AP|TS|TG|KA|MH|TN|DL|HR|UP|WB|GJ|RJ|PB)\b', 
                    text
                )
                if state_abbrev_match:
                    found_state = state_lexicon[state_abbrev_match.group(1).lower()]

        # Determine City (excluding common programming skills)
        cities = []
        for gpe in gpes:
            gpe_lower = gpe.lower()
            if gpe_lower not in country_lexicon and gpe_lower not in state_lexicon:
                if gpe_lower not in [s.lower() for s in COMMON_SKILLS]:
                    cities.append(gpe)

        entities["country"] = found_country
        entities["state"] = found_state
        entities["city"] = cities[0] if cities else ""

        # 4. Synthesize Address
        address_line = ""
        for i, line in enumerate(lines):
            trimmed = line.strip()
            addr_match = re.match(
                r'^(?:permanent\s+|correspondence\s+|present\s+)?(?:address|location|residence)\s*[:\-]\s*(.*)', 
                trimmed, 
                re.IGNORECASE
            )
            if addr_match:
                address_line = addr_match.group(1).strip()
                if i + 1 < len(lines):
                    next_line = lines[i+1].strip()
                    # Append next line if it doesn't look like a new label field
                    if next_line and not re.search(r'\b[a-zA-Z\s]+:', next_line) and any(
                        k in next_line.lower() for k in ["road", "street", "st.", "rd.", "lane", "nagar", "colony", "apartment", "floor", "h.no", "sector", "phase", "zip", "pin", "pincode"]
                    ):
                        address_line += ", " + next_line
                break

        if not address_line:
            for line in lines:
                trimmed = line.strip()
                if any(k in trimmed.lower() for k in ["road", "street", "st.", "rd.", "lane", "nagar", "colony", "apartment", "floor", "h.no", "sector", "phase", "flat", "building", "plot", "house"]):
                    address_line = trimmed
                    break

        if not address_line and gpes:
            address_line = ", ".join(dict.fromkeys(gpes))

        entities["address"] = address_line

        return entities
