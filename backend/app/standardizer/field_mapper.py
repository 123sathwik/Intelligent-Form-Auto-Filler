import re

# Thesaurus mapping incoming keys to target schema dot-paths (Legacy fallback)
FIELD_MAPPING = {
    # Personal Info
    "name": "personal_information.name",
    "candidate name": "personal_information.name",
    "applicant name": "personal_information.name",
    "student name": "personal_information.name",
    "full name": "personal_information.name",
    "person name": "personal_information.name",
    
    "father name": "personal_information.father_name",
    "father": "personal_information.father_name",
    "father s name": "personal_information.father_name",
    "fathers name": "personal_information.father_name",
    "father's name": "personal_information.father_name",
    
    "mother name": "personal_information.mother_name",
    "mother": "personal_information.mother_name",
    "mother s name": "personal_information.mother_name",
    "mothers name": "personal_information.mother_name",
    "mother's name": "personal_information.mother_name",
    
    "gender": "personal_information.gender",
    "sex": "personal_information.gender",
    
    "dob": "personal_information.dob",
    "date of birth": "personal_information.dob",
    "birth date": "personal_information.dob",
    "d o b": "personal_information.dob",
    
    "age": "personal_information.age",
    
    "nationality": "personal_information.nationality",
    "citizenship": "personal_information.nationality",
    
    # Contact Info
    "email": "contact_information.email",
    "email id": "contact_information.email",
    "mail": "contact_information.email",
    "mail address": "contact_information.email",
    "email address": "contact_information.email",
    
    "phone": "contact_information.phone",
    "phone number": "contact_information.phone",
    "mobile": "contact_information.phone",
    "mobile number": "contact_information.phone",
    "contact number": "contact_information.phone",
    "tel": "contact_information.phone",
    "telephone": "contact_information.phone",
    
    "address": "contact_information.address",
    "permanent address": "contact_information.address",
    "residential address": "contact_information.address",
    "location": "contact_information.address",
    
    "city": "contact_information.city",
    "town": "contact_information.city",
    
    "state": "contact_information.state",
    "province": "contact_information.state",
    
    "country": "contact_information.country",
    "nation": "contact_information.country",
    
    "pincode": "contact_information.pincode",
    "pin code": "contact_information.pincode",
    "zip": "contact_information.pincode",
    "zipcode": "contact_information.pincode",
    "zip code": "contact_information.pincode",
    "postal code": "contact_information.pincode",
    
    # Education
    "college": "education.college",
    "college name": "education.college",
    "institute": "education.college",
    "school": "education.college",
    
    "university": "education.university",
    "university name": "education.university",
    "board": "education.university",
    
    "degree": "education.degree",
    "degree name": "education.degree",
    "qualification": "education.degree",
    
    "branch": "education.branch",
    "branch name": "education.branch",
    "specialization": "education.branch",
    "stream": "education.branch",
    "major": "education.branch",
    
    "cgpa": "education.cgpa",
    "gpa": "education.cgpa",
    "grade point": "education.cgpa",
    
    "percentage": "education.percentage",
    "percent": "education.percentage",
    "marks percentage": "education.percentage",
    "aggregate marks": "education.percentage",
    
    # Professional
    "company": "professional.company",
    "company name": "professional.company",
    "organization": "professional.company",
    "employer": "professional.company",
    
    "experience": "professional.experience",
    "work experience": "professional.experience",
    "experience years": "professional.experience",
    
    "skills": "professional.skills",
    "skill list": "professional.skills",
    "technologies": "professional.skills",
    "key skills": "professional.skills",
    
    "projects": "professional.projects",
    "project list": "professional.projects",
    "key projects": "professional.projects",
    
    "certificates": "professional.certificates",
    "certifications": "professional.certificates",
    "credentials": "professional.certificates",
    
    # Identification
    "passport number": "identification.passport_number",
    "passport": "identification.passport_number",
    "passport no": "identification.passport_number",
    
    "visa number": "identification.visa_number",
    "visa": "identification.visa_number",
    "visa no": "identification.visa_number",
    
    "pan number": "identification.pan_number",
    "pan": "identification.pan_number",
    "pan card": "identification.pan_number",
    "pan card number": "identification.pan_number",
    "pan no": "identification.pan_number",
    
    "aadhaar number": "identification.aadhaar_number",
    "aadhaar": "identification.aadhaar_number",
    "aadhaar card": "identification.aadhaar_number",
    "aadhaar card number": "identification.aadhaar_number",
    "aadhaar no": "identification.aadhaar_number",
    "adhar": "identification.aadhaar_number",
    "adhar card": "identification.aadhaar_number",
    "adhar number": "identification.aadhaar_number",
    
    "driving license": "identification.driving_license",
    "driving license number": "identification.driving_license",
    "dl number": "identification.driving_license",
    "dl": "identification.driving_license",
    "dl no": "identification.driving_license",
}

# Document type specific thesaurus mappings
DOCUMENT_MAPPINGS = {
    "Resume": {
        "name": "personal_information.name",
        "candidate name": "personal_information.name",
        "applicant name": "personal_information.name",
        "student name": "personal_information.name",
        "full name": "personal_information.name",
        "person name": "personal_information.name",
        "father name": "personal_information.father_name",
        "mother name": "personal_information.mother_name",
        "gender": "personal_information.gender",
        "sex": "personal_information.gender",
        "dob": "personal_information.dob",
        "date of birth": "personal_information.dob",
        "age": "personal_information.age",
        "nationality": "personal_information.nationality",
        "email": "contact_information.email",
        "email id": "contact_information.email",
        "mail": "contact_information.email",
        "phone": "contact_information.phone",
        "phone number": "contact_information.phone",
        "mobile": "contact_information.phone",
        "address": "contact_information.address",
        "college": "education.college",
        "institute": "education.college",
        "school": "education.college",
        "university": "education.university",
        "degree": "education.degree",
        "branch": "education.branch",
        "specialization": "education.branch",
        "cgpa": "education.cgpa",
        "gpa": "education.cgpa",
        "percentage": "education.percentage",
        "company": "professional.company",
        "experience": "professional.experience",
        "skills": "professional.skills",
        "projects": "professional.projects",
        "certificates": "professional.certificates"
    },
    "Passport": {
        "passport number": "passport_details.passport_number",
        "passport no": "passport_details.passport_number",
        "passport": "passport_details.passport_number",
        "country code": "passport_details.country_code",
        "surname": "passport_details.surname",
        "given names": "passport_details.given_names",
        "nationality": "passport_details.nationality",
        "dob": "passport_details.dob",
        "date of birth": "passport_details.dob",
        "gender": "passport_details.gender",
        "sex": "passport_details.gender",
        "place of birth": "passport_details.place_of_birth",
        "place of issue": "passport_details.place_of_issue",
        "authority": "passport_details.place_of_issue",
        "date of issue": "passport_details.date_of_issue",
        "date of expiry": "passport_details.date_of_expiry",
        "expiry date": "passport_details.date_of_expiry",
    },
    "Aadhaar": {
        "aadhaar number": "aadhaar_details.aadhaar_number",
        "aadhaar": "aadhaar_details.aadhaar_number",
        "aadhaar card": "aadhaar_details.aadhaar_number",
        "adhar": "aadhaar_details.aadhaar_number",
        "name": "aadhaar_details.name",
        "full name": "aadhaar_details.name",
        "dob": "aadhaar_details.dob",
        "date of birth": "aadhaar_details.dob",
        "gender": "aadhaar_details.gender",
        "sex": "aadhaar_details.gender",
        "address": "aadhaar_details.address",
        "father name": "aadhaar_details.father_or_spouse_name",
        "husband name": "aadhaar_details.father_or_spouse_name",
        "father or spouse": "aadhaar_details.father_or_spouse_name"
    },
    "PAN Card": {
        "pan number": "pan_details.pan_number",
        "pan": "pan_details.pan_number",
        "pan card": "pan_details.pan_number",
        "name": "pan_details.name",
        "father name": "pan_details.father_name",
        "dob": "pan_details.dob",
        "date of birth": "pan_details.dob",
        "card type": "pan_details.card_type",
        "category": "pan_details.card_type"
    },
    "Driving License": {
        "driving license": "license_details.driving_license_number",
        "driving license number": "license_details.driving_license_number",
        "license number": "license_details.driving_license_number",
        "dl number": "license_details.driving_license_number",
        "dl": "license_details.driving_license_number",
        "name": "license_details.name",
        "father name": "license_details.father_or_spouse_name",
        "father or spouse": "license_details.father_or_spouse_name",
        "dob": "license_details.dob",
        "date of birth": "license_details.dob",
        "address": "license_details.address",
        "license class": "license_details.license_class",
        "class": "license_details.license_class",
        "date of issue": "license_details.date_of_issue",
        "issue date": "license_details.date_of_issue",
        "date of expiry": "license_details.date_of_expiry",
        "expiry date": "license_details.date_of_expiry"
    },
    "Invoice": {
        "invoice number": "invoice_details.invoice_number",
        "invoice no": "invoice_details.invoice_number",
        "invoice": "invoice_details.invoice_number",
        "invoice date": "invoice_details.invoice_date",
        "date": "invoice_details.invoice_date",
        "due date": "invoice_details.due_date",
        "po number": "invoice_details.po_number",
        "po": "invoice_details.po_number",
        "vendor name": "vendor_details.vendor_name",
        "vendor": "vendor_details.vendor_name",
        "vendor address": "vendor_details.vendor_address",
        "vendor email": "vendor_details.vendor_email",
        "vendor phone": "vendor_details.vendor_phone",
        "tax id": "vendor_details.tax_id",
        "customer name": "customer_details.customer_name",
        "customer": "customer_details.customer_name",
        "bill to": "customer_details.customer_name",
        "customer address": "customer_details.customer_address",
        "customer email": "customer_details.customer_email",
        "customer phone": "customer_details.customer_phone",
        "subtotal": "payment_details.subtotal",
        "tax amount": "payment_details.tax_amount",
        "tax": "payment_details.tax_amount",
        "total amount": "payment_details.total_amount",
        "total": "payment_details.total_amount",
        "payment status": "payment_details.payment_status",
        "status": "payment_details.payment_status"
    },
    "Bank Statement": {
        "bank name": "bank_details.bank_name",
        "bank": "bank_details.bank_name",
        "account number": "bank_details.account_number",
        "account no": "bank_details.account_number",
        "account holder": "bank_details.account_holder",
        "name": "bank_details.account_holder",
        "statement period": "bank_details.statement_period",
        "period": "bank_details.statement_period",
        "opening balance": "bank_details.opening_balance",
        "closing balance": "bank_details.closing_balance",
        "balance": "bank_details.closing_balance"
    },
    "Medical Report": {
        "patient name": "patient_details.patient_name",
        "patient": "patient_details.patient_name",
        "age": "patient_details.age",
        "gender": "patient_details.gender",
        "sex": "patient_details.gender",
        "dob": "patient_details.dob",
        "date of birth": "patient_details.dob",
        "patient id": "patient_details.patient_id",
        "report date": "clinical_details.report_date",
        "date": "clinical_details.report_date",
        "doctor name": "clinical_details.doctor_name",
        "doctor": "clinical_details.doctor_name",
        "diagnosis": "clinical_details.diagnosis",
        "symptoms": "clinical_details.symptoms",
        "recommendations": "clinical_details.recommendations",
        "treatment": "clinical_details.recommendations",
        "tests performed": "clinical_details.tests_performed",
        "tests": "clinical_details.tests_performed"
    },
    "Research Paper": {
        "title": "paper_details.title",
        "authors": "paper_details.authors",
        "author": "paper_details.authors",
        "abstract": "paper_details.abstract",
        "publication date": "paper_details.publication_date",
        "date": "paper_details.publication_date",
        "journal": "paper_details.journal_or_conference",
        "conference": "paper_details.journal_or_conference",
        "journal or conference": "paper_details.journal_or_conference",
        "keywords": "paper_details.keywords",
        "doi": "paper_details.doi"
    },
    "Egg AI Report": {
        "batch number": "egg_details.batch_number",
        "batch": "egg_details.batch_number",
        "inspection date": "egg_details.inspection_date",
        "date": "egg_details.inspection_date",
        "total eggs": "egg_details.total_eggs",
        "grade a count": "egg_details.grade_a_count",
        "grade a": "egg_details.grade_a_count",
        "grade b count": "egg_details.grade_b_count",
        "grade b": "egg_details.grade_b_count",
        "reject count": "egg_details.reject_count",
        "rejects": "egg_details.reject_count",
        "temperature": "egg_details.temperature",
        "temp": "egg_details.temperature",
        "humidity": "egg_details.humidity",
        "inspector name": "egg_details.inspector_name",
        "inspector": "egg_details.inspector_name"
    },
    "Certificate": {
        "title": "certificate_details.title",
        "recipient name": "certificate_details.recipient_name",
        "recipient": "certificate_details.recipient_name",
        "name": "certificate_details.recipient_name",
        "awarded to": "certificate_details.recipient_name",
        "issuing organization": "certificate_details.issuing_organization",
        "issuer": "certificate_details.issuing_organization",
        "issue date": "certificate_details.issue_date",
        "date": "certificate_details.issue_date",
        "credential id": "certificate_details.credential_id",
        "credential": "certificate_details.credential_id",
        "course": "certificate_details.course_or_achievement",
        "achievement": "certificate_details.course_or_achievement",
        "course or achievement": "certificate_details.course_or_achievement"
    },
    "Generic Document": {
        "title": "document_details.title",
        "date": "document_details.date",
        "author": "document_details.author",
        "description": "document_details.description",
        "content summary": "document_details.content_summary",
        "summary": "document_details.content_summary"
    }
}

class FieldMapper:
    @staticmethod
    def clean_key(key: str) -> str:
        """
        Cleans and normalizes key names to lowercase words separated by single spaces.
        E.g., 'Candidate_Name' -> 'candidate name'
              'Email-ID!'      -> 'email id'
        """
        # Remove any non-alphanumeric/spaces/underscores/hyphens
        cleaned = re.sub(r'[^a-zA-Z0-9\s_-]', ' ', key)
        # Convert underscores and hyphens to spaces
        cleaned = cleaned.replace('_', ' ').replace('-', ' ')
        # Collapse multiple spaces and trim
        return " ".join(cleaned.split()).lower()

    @staticmethod
    def map_key_to_schema_path(key: str, document_type: str = "Generic Document") -> str:
        """
        Maps standard and non-standard field keys to schema dot-notation paths
        for a specific document type, falling back to general field mapping.
        Returns empty string if not matched.
        """
        cleaned = FieldMapper.clean_key(key)
        
        # 1. Check document type specific mapping first
        if document_type in DOCUMENT_MAPPINGS:
            path = DOCUMENT_MAPPINGS[document_type].get(cleaned)
            if path:
                return path

        # 2. Fall back to generic mapping
        return FIELD_MAPPING.get(cleaned, "")
