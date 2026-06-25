import json
import urllib.request
import urllib.error

API_URL = "http://localhost:8000/extract-entities"

# Define mock document texts representing different scenarios
MOCK_DOCUMENTS = {
    "resume": """
    Vamsi Krishna
    Software Engineer
    Email: vamsi.krishna@example.com
    Phone: +91-9876543210
    LinkedIn: https://www.linkedin.com/in/vamsikrishna
    GitHub: https://github.com/vamsikrishna
    Website: https://vamsikrishna.dev

    OBJECTIVE
    Detail-oriented Software Engineer seeking a challenging role.

    EDUCATION
    Stanford University
    Degree: B.Tech
    Branch: Computer Science
    CGPA: 9.4
    Percentage: 94%

    EXPERIENCE
    Software Engineer at Google Ltd (June 2024 - Present)
    Developed high-performance microservices in Python.
    Worked as Associate Developer at Tech Solutions (May 2023 - May 2024)

    PROJECTS
    Developed a real-time face recognition system using OpenCV.
    Built a scalable analytics dashboard in React and Go.

    CERTIFICATIONS
    AWS Certified Solutions Architect
    Docker Certified Associate

    SKILLS
    Python, TypeScript, React, Docker, FastAPI, SQL, Git

    PERSONAL DETAILS
    Father Name: Mr. Ramakrishna Prasad
    Mother Name: Mrs. Sita Lakshmi
    Date of Birth: 15/08/2000
    Age: 25
    Gender: Male
    Nationality: Indian
    Permanent Address: 104, Sunrise Apartments, Road No 3, Banjara Hills, Hyderabad, Telangana, 500034, India
    """,

    "government_ids": """
    GOVERNMENT OF INDIA
    AADHAAR CARD
    Aadhaar Number: 1234 5678 9012
    PAN CARD
    PAN Number: ABCDE1234F
    PASSPORT
    Passport Number: Z1234567
    VISA
    Visa Number: VI123456789
    DRIVING LICENSE
    DL No: DL1420110068991
    """,

    "invoice_and_employee": """
    INVOICE
    Invoice Number: INV-2026-9988
    Bill to: Acme Corp
    Date: 2026-06-25

    EMPLOYEE DETAIL
    Employee ID: EMP-998822
    College: Hyderabad Engineering College
    Roll Number: 1601-20-733-045
    Registration Number: REG-2026-887766
    """
}

def run_extraction_test(text):
    data = json.dumps({"text": text}).encode("utf-8")
    req = urllib.request.Request(
        API_URL, 
        data=data, 
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    try:
        with urllib.request.urlopen(req) as response:
            res_body = response.read().decode("utf-8")
            return json.loads(res_body)
    except urllib.error.HTTPError as e:
        print(f"HTTP Error: {e.code} - {e.reason}")
        print(e.read().decode("utf-8"))
        return None
    except Exception as e:
        print(f"Error connecting to API: {str(e)}")
        return None

def test_all():
    print("==================================================")
    print("Testing NLP / Entity Extraction API Endpoint")
    print("==================================================")

    # Test 1: Resume Document
    print("\n--- Test Case 1: Resume Extraction ---")
    res1 = run_extraction_test(MOCK_DOCUMENTS["resume"])
    if not res1 or not res1.get("success"):
        print("FAIL: Resume extraction failed.")
        return False
    
    entities = res1["entities"]
    
    # Assertions
    assertions = {
        "name": "Vamsi Krishna",
        "email": "vamsi.krishna@example.com",
        "phone_number": "9876543210",
        "dob": "15/08/2000",
        "age": "25",
        "gender": "Male",
        "nationality": "Indian",
        "degree": "B.Tech",
        "branch": "Computer Science",
        "cgpa": "9.4",
        "percentage": "94",
        "university": "Stanford University",
        "company": "Google Ltd",
        "linkedin": "https://www.linkedin.com/in/vamsikrishna",
        "github": "https://github.com/vamsikrishna",
        "website": "https://vamsikrishna.dev",
        "father_name": "Ramakrishna Prasad",
        "mother_name": "Sita Lakshmi",
        "state": "Telangana",
        "country": "India",
        "pincode": "500034"
    }

    passed = True
    for key, expected in assertions.items():
        val = entities.get(key)
        if val != expected:
            print(f"  [Mismatch] Key '{key}': Expected '{expected}', Got '{val}'")
            passed = False
        else:
            print(f"  [OK] Key '{key}': '{val}'")

    # Verify lists are present and correct
    for lst_key, expected_subset in [
        ("skills", ["Python", "TypeScript", "React", "Docker", "FastAPI", "SQL", "Git"]),
        ("experience", ["Software Engineer at Google Ltd (June 2024 - Present)", "Worked as Associate Developer at Tech Solutions (May 2023 - May 2024)"]),
        ("projects", ["Developed a real-time face recognition system using OpenCV.", "Built a scalable analytics dashboard in React and Go."]),
        ("certificates", ["AWS Certified Solutions Architect", "Docker Certified Associate"])
    ]:
        val_list = entities.get(lst_key, [])
        mismatch = [item for item in expected_subset if item not in val_list]
        if mismatch:
            print(f"  [Mismatch] Key '{lst_key}': Missing {mismatch} in {val_list}")
            passed = False
        else:
            print(f"  [OK] Key '{lst_key}': Extracted {len(val_list)} items.")

    # Test 2: Government IDs
    print("\n--- Test Case 2: Government IDs Extraction ---")
    res2 = run_extraction_test(MOCK_DOCUMENTS["government_ids"])
    if not res2 or not res2.get("success"):
        print("FAIL: Government IDs extraction failed.")
        return False
    
    entities2 = res2["entities"]
    id_assertions = {
        "aadhaar_number": "1234 5678 9012",
        "pan_number": "ABCDE1234F",
        "passport_number": "Z1234567",
        "visa_number": "VI123456789",
        "driving_license_number": "DL1420110068991"
    }

    for key, expected in id_assertions.items():
        val = entities2.get(key)
        if val != expected:
            print(f"  [Mismatch] Key '{key}': Expected '{expected}', Got '{val}'")
            passed = False
        else:
            print(f"  [OK] Key '{key}': '{val}'")

    # Test 3: Invoice and Employee Details
    print("\n--- Test Case 3: Invoice & Employee Extraction ---")
    res3 = run_extraction_test(MOCK_DOCUMENTS["invoice_and_employee"])
    if not res3 or not res3.get("success"):
        print("FAIL: Invoice & Employee extraction failed.")
        return False
    
    entities3 = res3["entities"]
    invoice_assertions = {
        "invoice_number": "INV-2026-9988",
        "employee_id": "EMP-998822",
        "roll_number": "1601-20-733-045",
        "registration_number": "REG-2026-887766",
        "college": "Hyderabad Engineering College"
    }

    for key, expected in invoice_assertions.items():
        val = entities3.get(key)
        if val != expected:
            print(f"  [Mismatch] Key '{key}': Expected '{expected}', Got '{val}'")
            passed = False
        else:
            print(f"  [OK] Key '{key}': '{val}'")

    print("\n==================================================")
    if passed:
        print("SUCCESS: All tests passed!")
    else:
        print("FAIL: Some assertions failed.")
    print("==================================================")
    return passed

if __name__ == "__main__":
    test_all()
