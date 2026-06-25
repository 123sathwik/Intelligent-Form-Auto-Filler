import logging
from app.nlp.regex_extractor import RegexExtractor
from app.nlp.custom_rules import CustomRulesExtractor
from app.nlp.entity_extractor import EntityExtractor

logger = logging.getLogger("autofiller-backend")

class EntityService:
    @staticmethod
    async def extract_entities_from_text(text: str) -> dict:
        """
        Coordinates NLP, Regex, and Heuristics to extract structured information from cleaned text.
        Returns a structured dictionary matching the 38 requested fields.
        """
        logger.info("Starting Entity Extraction pipeline...")
        
        # 1. Execute individual extractors
        regex_data = RegexExtractor.extract(text)
        rules_data = CustomRulesExtractor.extract(text)
        nlp_data = EntityExtractor.extract(text)

        # 2. Merge and prioritize extractions
        
        # Name: prioritize spaCy NER
        name = nlp_data.get("person_name") or rules_data.get("person_name") or ""
        
        # Email: prioritize Regex
        email = regex_data.get("email") or ""
        
        # Phone: prioritize Regex
        phone = regex_data.get("phone_number") or ""
        
        # DOB: prioritize Regex or Custom Rules
        dob = regex_data.get("dob") or rules_data.get("dob") or ""
        
        # Degree & Branch: prioritize Custom Rules
        degree = rules_data.get("degree") or ""
        branch = rules_data.get("branch") or ""
        
        # CGPA & Percentage: prioritize Custom Rules
        cgpa = rules_data.get("cgpa") or ""
        percentage = rules_data.get("percentage") or ""
        
        # Address, City, State, Country: prioritize spaCy GPE
        address = nlp_data.get("address") or ""
        city = nlp_data.get("city") or ""
        state = nlp_data.get("state") or ""
        country = nlp_data.get("country") or ""
        pincode = regex_data.get("pincode") or ""

        # Institutions: prioritize spaCy ORG
        organization = nlp_data.get("organization") or ""
        company = nlp_data.get("company") or ""
        college = nlp_data.get("college") or ""
        university = nlp_data.get("university") or ""

        # Demographics: prioritize Custom Rules
        father_name = rules_data.get("father_name") or ""
        mother_name = rules_data.get("mother_name") or ""
        age = rules_data.get("age") or ""
        gender = rules_data.get("gender") or ""
        nationality = rules_data.get("nationality") or ""

        # Lists: prioritize Custom Rules
        skills = rules_data.get("skills") or []
        experience = rules_data.get("experience") or []
        projects = rules_data.get("projects") or []
        certificates = rules_data.get("certificates") or []

        # URLs: prioritize Regex
        linkedin = regex_data.get("linkedin") or ""
        github = regex_data.get("github") or ""
        website = regex_data.get("website") or ""

        # Document Identifiers: prioritize Regex
        passport_number = regex_data.get("passport_number") or ""
        visa_number = regex_data.get("visa_number") or ""
        pan_number = regex_data.get("pan_number") or ""
        aadhaar_number = regex_data.get("aadhaar_number") or ""
        driving_license_number = regex_data.get("driving_license_number") or ""
        invoice_number = regex_data.get("invoice_number") or ""
        employee_id = regex_data.get("employee_id") or ""
        roll_number = regex_data.get("roll_number") or ""
        registration_number = regex_data.get("registration_number") or ""

        # 3. Construct structured output mapping all 38 fields plus alias keys
        entities_map = {
            # Aliases & Standard keys
            "name": name,
            "person_name": name,
            "father_name": father_name,
            "mother_name": mother_name,
            "email": email,
            "phone": phone,
            "phone_number": phone,
            "dob": dob,
            "date_of_birth": dob,
            "age": age,
            "gender": gender,
            "nationality": nationality,
            
            # Location
            "address": address,
            "city": city,
            "state": state,
            "country": country,
            "pincode": pincode,
            
            # Education / Professional
            "organization": organization,
            "company": company,
            "college": college,
            "university": university,
            "degree": degree,
            "branch": branch,
            "cgpa": cgpa,
            "percentage": percentage,
            
            # Lists
            "skills": skills,
            "experience": experience,
            "projects": projects,
            "certificates": certificates,
            
            # Socials & Web
            "linkedin": linkedin,
            "github": github,
            "website": website,
            
            # Document IDs
            "passport_number": passport_number,
            "visa_number": visa_number,
            "pan_number": pan_number,
            "aadhaar_number": aadhaar_number,
            "driving_license_number": driving_license_number,
            "invoice_number": invoice_number,
            "employee_id": employee_id,
            "roll_number": roll_number,
            "registration_number": registration_number
        }

        logger.info("Extraction complete. Returning entities map.")
        return {
            "success": True,
            "entities": entities_map
        }
