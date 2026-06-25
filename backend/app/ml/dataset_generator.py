import random

# Thesaurus containing representative synonyms for the 30 target classes
SYNONYMS = {
    "name": [
        "Name", "Full Name", "Candidate Name", "Applicant Name", "Student Name", "Person Name",
        "First Name", "Last Name", "User's Name", "Profile Name", "Customer Name", "Member Name",
        "Employee Name", "Staff Name", "Client Name", "Guest Name", "Account Name", "Holder Name"
    ],
    "father_name": [
        "Father Name", "Father's Name", "Dad's Name", "Parent Name", "Father", "Name of Father",
        "Father's Full Name", "Paternal Parent Name", "Guardian Name", "Father's First Name"
    ],
    "mother_name": [
        "Mother Name", "Mother's Name", "Mom's Name", "Mother", "Name of Mother", "Mother's Full Name",
        "Maternal Parent Name", "Mother's First Name"
    ],
    "gender": [
        "Gender", "Sex", "Gender Identity", "Male/Female/Other", "Sexuality", "Sex Category", "Gender Category"
    ],
    "dob": [
        "DOB", "Date of Birth", "Birth Date", "Birth Date and Year", "Birthday", "D.O.B", "Born On"
    ],
    "age": [
        "Age", "Age in Years", "Year of Age", "Current Age", "User Age", "How old"
    ],
    "nationality": [
        "Nationality", "Citizenship", "Country of Citizenship", "Nation of Origin", "Ethnic Origin", "Country of Nationality"
    ],
    "email": [
        "Email", "Mail", "Email Address", "Mail ID", "Email ID", "Mailing Address", "Electronic Mail", "Inbox Address"
    ],
    "phone": [
        "Phone", "Mobile", "Contact Number", "Cell Number", "Telephone", "Mobile Number", "Phone No",
        "Cell No", "Contact Phone", "Telephone Number", "Tel"
    ],
    "address": [
        "Address", "Permanent Address", "Residential Address", "Correspondence Address", "Home Address",
        "Street Address", "Location", "Residence", "House Address", "Mailing Address"
    ],
    "city": [
        "City", "Town", "Municipality", "City Name", "Town Name", "City of Residence"
    ],
    "state": [
        "State", "Province", "Territory", "State Name", "Region", "Province Name", "State/Province"
    ],
    "country": [
        "Country", "Nation", "Country Name", "Nation Name", "Country of Residence"
    ],
    "pincode": [
        "Pincode", "Pin Code", "Zip", "Zip Code", "Zipcode", "Postal Code", "Postal"
    ],
    "college": [
        "College", "College Name", "Institute", "School", "Institute Name", "School Name", "College Attended"
    ],
    "university": [
        "University", "University Name", "Board", "University Attended", "Board of Education"
    ],
    "degree": [
        "Degree", "Degree Name", "Qualification", "Educational Qualification", "Highest Degree", "Major Qualification",
        "Academic Degree", "Academic Qualification", "Course of Study", "Graduation Degree"
    ],
    "branch": [
        "Branch", "Branch Name", "Specialization", "Stream", "Major", "Subject", "Department"
    ],
    "cgpa": [
        "CGPA", "GPA", "Grade Point", "Grade Point Average", "Cumulative GPA", "Scores"
    ],
    "percentage": [
        "Percentage", "Percent", "Marks Percentage", "Aggregate Marks", "Score Percentage", "Overall Percentage"
    ],
    "company": [
        "Company", "Company Name", "Organization", "Employer", "Workplace", "Firm Name",
        "Corporate Name", "Organization Name"
    ],
    "experience": [
        "Experience", "Work Experience", "Professional Experience", "Years of Experience",
        "Past Experience", "Employment History", "Experience Years"
    ],
    "skills": [
        "Skills", "Key Skills", "Technologies", "Technical Skills", "Core Skills", "Skillset", "List of Skills"
    ],
    "projects": [
        "Projects", "Project List", "Key Projects", "Academic Projects", "Major Projects", "Work Projects", "Project Descriptions"
    ],
    "certificates": [
        "Certificates", "Certifications", "Credentials", "Certified In", "Professional Certifications", "Courses"
    ],
    "passport_number": [
        "Passport Number", "Passport", "Passport No", "Passport ID", "Travel Document Number", "Passport Code"
    ],
    "visa_number": [
        "Visa Number", "Visa", "Visa No", "Visa ID", "Permit Number", "Visa Code"
    ],
    "pan_number": [
        "PAN Number", "PAN", "PAN Card", "PAN Card Number", "PAN No", "Permanent Account Number"
    ],
    "aadhaar_number": [
        "Aadhaar Number", "Aadhaar", "Aadhaar Card", "Aadhaar Card Number", "Aadhaar No", "UIDAI Number"
    ],
    "driving_license": [
        "Driving License", "Driving License Number", "DL Number", "DL", "DL No", "License Number", "Driving Permit Number"
    ]
}

# String templates to multiply the synonym examples for a robust semantic range
TEMPLATES = [
    "{synonym}",
    "Enter {synonym}",
    "Please provide your {synonym}",
    "Your {synonym}",
    "{synonym} is required",
    "{synonym}:",
    "Field for {synonym}",
    "Input {synonym}",
    "Type of {synonym}",
    "{synonym} value",
    "Provide {synonym}"
]

class DatasetGenerator:
    @staticmethod
    def generate() -> tuple:
        """
        Generates lists of (label, target_class) pairs.
        Returns a tuple of (texts, labels).
        """
        texts = []
        labels = []
        
        # Apply templates to synonyms to generate thousands of examples
        for target_class, syn_list in SYNONYMS.items():
            for synonym in syn_list:
                for template in TEMPLATES:
                    # Apply template casing variations
                    sentence = template.format(synonym=synonym)
                    
                    texts.append(sentence)
                    labels.append(target_class)
                    
                    # Add lowercase and uppercase variants to double the training diversity
                    texts.append(sentence.lower())
                    labels.append(target_class)
                    
                    texts.append(sentence.upper())
                    labels.append(target_class)

        # Shuffle the generated dataset deterministically
        combined = list(zip(texts, labels))
        random.seed(42)
        random.shuffle(combined)
        
        # Split back
        texts_shuffled, labels_shuffled = zip(*combined)
        return list(texts_shuffled), list(labels_shuffled)
