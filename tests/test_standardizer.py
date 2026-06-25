import json
import urllib.request
import urllib.error

API_URL = "http://localhost:8000/api/v1/standardize"

TEST_CASES = {
    "resume": {
        "Candidate Name": "Vamsi Krishna",
        "Father's Name": "Ramakrishna Prasad",
        "Mother's Name": "Sita Lakshmi",
        "Gender": "Male",
        "DOB": "15/08/2000",
        "Age": "25 years old",
        "Nationality": "Indian",
        "Email ID": "vamsi@example.com",
        "Mobile": "+91-9876543210",
        "Address": "104 Sunrise Apartments, Banjara Hills",
        "City": "Hyderabad",
        "State": "Telangana",
        "Country": "India",
        "Pin Code": "500034",
        "College": "Hyderabad Engineering College",
        "University": "Stanford University",
        "Degree": "B.Tech",
        "Branch": "Computer Science",
        "CGPA": "9.4 CGPA",
        "Percentage": "94%",
        "Company": "Google Ltd",
        "Work Experience": [
            "Software Engineer at Google Ltd (June 2024 - Present)",
            "Worked as Associate Developer at Tech Solutions (May 2023 - May 2024)"
        ],
        "Key Skills": "Python, TypeScript, React, Docker, FastAPI",
        "Key Projects": "Real-time face recognition system, Scalable analytics dashboard",
        "Certifications": ["AWS Solutions Architect", "Docker Associate"]
    },
    
    "passport": {
        "Full Name": "John Doe",
        "Birth Date": "05 Dec 1995",
        "Passport Number": "Z1234567",
        "Nationality": "American",
        "Sex": "Male"
    },

    "invoice": {
        "Employer": "Acme Corp",
        "Mobile": "555-666-7777",
        "Pin Code": "95101",
        "DL No": "DL1420110068991",
        "PAN Card": "ABCDE1234F"
    },

    "admission_form": {
        "Student Name": "Alice Smith",
        "Mail": "alice@gmail.com",
        "Grade Point": "8.5 GPA",
        "Percent": "85.0",
        "Qualification": "MCA",
        "Specialization": "Cloud Computing"
    },

    "government_id": {
        "Aadhaar Card": "1234 5678 9012",
        "Full Name": "Charlie Brown",
        "Sex": "M",
        "Age": "30 years"
    }
}

def run_standardizer_test(payload):
    data = json.dumps(payload).encode("utf-8")
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
    print("Testing JSON Standardization Module API Endpoint")
    print("==================================================")

    passed = True

    # 1. Test Resume
    print("\n--- Test Case 1: Resume standardization ---")
    res1 = run_standardizer_test(TEST_CASES["resume"])
    if not res1:
        print("FAIL: Resume standardizer request failed.")
        return False
    
    personal = res1.get("personal_information", {})
    contact = res1.get("contact_information", {})
    education = res1.get("education", {})
    professional = res1.get("professional", {})
    
    resume_assertions = [
        (personal.get("name"), "Vamsi Krishna"),
        (personal.get("father_name"), "Ramakrishna Prasad"),
        (personal.get("mother_name"), "Sita Lakshmi"),
        (personal.get("gender"), "Male"),
        (personal.get("dob"), "2000-08-15"),
        (personal.get("age"), "25"),
        (personal.get("nationality"), "Indian"),
        (contact.get("email"), "vamsi@example.com"),
        (contact.get("phone"), "+91-9876543210"),
        (contact.get("pincode"), "500034"),
        (education.get("degree"), "B.Tech"),
        (education.get("cgpa"), "9.4"),
        (education.get("percentage"), "94"),
        (professional.get("company"), "Google Ltd"),
        (professional.get("experience"), "Software Engineer at Google Ltd (June 2024 - Present); Worked as Associate Developer at Tech Solutions (May 2023 - May 2024)")
    ]
    
    for val, expected in resume_assertions:
        if val != expected:
            print(f"  [Mismatch] Expected '{expected}', Got '{val}'")
            passed = False
        else:
            print(f"  [OK] '{expected}' matched.")

    # Verify Skills/Projects/Certificates list transformations
    skills = professional.get("skills", [])
    expected_skills = ["Python", "TypeScript", "React", "Docker", "FastAPI"]
    if skills != expected_skills:
        print(f"  [Mismatch] skills: Expected {expected_skills}, Got {skills}")
        passed = False
    else:
        print(f"  [OK] skills: {skills}")

    projects = professional.get("projects", [])
    expected_projects = ["Real-time face recognition system", "Scalable analytics dashboard"]
    if projects != expected_projects:
        print(f"  [Mismatch] projects: Expected {expected_projects}, Got {projects}")
        passed = False
    else:
        print(f"  [OK] projects: {projects}")

    # 2. Test Passport
    print("\n--- Test Case 2: Passport standardization ---")
    res2 = run_standardizer_test(TEST_CASES["passport"])
    if not res2:
        print("FAIL: Passport standardizer request failed.")
        return False
    
    passport_assertions = [
        (res2.get("personal_information", {}).get("name"), "John Doe"),
        (res2.get("personal_information", {}).get("dob"), "1995-12-05"),
        (res2.get("personal_information", {}).get("gender"), "Male"),
        (res2.get("personal_information", {}).get("nationality"), "American"),
        (res2.get("identification", {}).get("passport_number"), "Z1234567")
    ]
    for val, expected in passport_assertions:
        if val != expected:
            print(f"  [Mismatch] Expected '{expected}', Got '{val}'")
            passed = False
        else:
            print(f"  [OK] '{expected}' matched.")

    # 3. Test Invoice
    print("\n--- Test Case 3: Invoice standardization ---")
    res3 = run_standardizer_test(TEST_CASES["invoice"])
    if not res3:
        print("FAIL: Invoice standardizer request failed.")
        return False
    
    invoice_assertions = [
        (res3.get("professional", {}).get("company"), "Acme Corp"),
        (res3.get("contact_information", {}).get("phone"), "555-666-7777"),
        (res3.get("contact_information", {}).get("pincode"), "95101"),
        (res3.get("identification", {}).get("driving_license"), "DL1420110068991"),
        (res3.get("identification", {}).get("pan_number"), "ABCDE1234F")
    ]
    for val, expected in invoice_assertions:
        if val != expected:
            print(f"  [Mismatch] Expected '{expected}', Got '{val}'")
            passed = False
        else:
            print(f"  [OK] '{expected}' matched.")

    # 4. Test Admission Form
    print("\n--- Test Case 4: Admission Form standardization ---")
    res4 = run_standardizer_test(TEST_CASES["admission_form"])
    if not res4:
        print("FAIL: Admission Form standardizer request failed.")
        return False
    
    admission_assertions = [
        (res4.get("personal_information", {}).get("name"), "Alice Smith"),
        (res4.get("contact_information", {}).get("email"), "alice@gmail.com"),
        (res4.get("education", {}).get("degree"), "MCA"),
        (res4.get("education", {}).get("branch"), "Cloud Computing"),
        (res4.get("education", {}).get("cgpa"), "8.5"),
        (res4.get("education", {}).get("percentage"), "85.0")
    ]
    for val, expected in admission_assertions:
        if val != expected:
            print(f"  [Mismatch] Expected '{expected}', Got '{val}'")
            passed = False
        else:
            print(f"  [OK] '{expected}' matched.")

    # 5. Test Government ID
    print("\n--- Test Case 5: Government ID standardization ---")
    res5 = run_standardizer_test(TEST_CASES["government_id"])
    if not res5:
        print("FAIL: Government ID standardizer request failed.")
        return False
    
    gov_assertions = [
        (res5.get("identification", {}).get("aadhaar_number"), "1234 5678 9012"),
        (res5.get("personal_information", {}).get("name"), "Charlie Brown"),
        (res5.get("personal_information", {}).get("gender"), "Male"),
        (res5.get("personal_information", {}).get("age"), "30")
    ]
    for val, expected in gov_assertions:
        if val != expected:
            print(f"  [Mismatch] Expected '{expected}', Got '{val}'")
            passed = False
        else:
            print(f"  [OK] '{expected}' matched.")

    print("\n==================================================")
    if passed:
        print("SUCCESS: All tests passed!")
    else:
        print("FAIL: Some assertions failed.")
    print("==================================================")
    return passed

if __name__ == "__main__":
    test_all()
