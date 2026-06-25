import json
import sys
import logging
import urllib.request
import urllib.error
from pathlib import Path

# Add backend to python path to run training script first
sys.path.append(str(Path(__file__).parent.parent / "backend"))

from app.ml.model_trainer import ModelTrainer

API_URL = "http://localhost:8000/api/v1/map-fields"

TEST_DOMAINS = {
    "government_forms": {
        "labels": ["Aadhaar Card Number", "Permanent Account Number", "Driving License ID", "Date of Birth", "Sex Category"],
        "expected": {
            "Aadhaar Card Number": "aadhaar_number",
            "Permanent Account Number": "pan_number",
            "Driving License ID": "driving_license",
            "Date of Birth": "dob",
            "Sex Category": "gender"
        }
    },
    "resume_forms": {
        "labels": ["Candidate Full Name", "Key Skills", "Technical Projects", "Work Experience Years", "Academic Degree"],
        "expected": {
            "Candidate Full Name": "name",
            "Key Skills": "skills",
            "Technical Projects": "projects",
            "Work Experience Years": "experience",
            "Academic Degree": "degree"
        }
    },
    "admission_forms": {
        "labels": ["Student Name", "Grade Point Average", "Qualification Name", "Specialization Stream", "College Name"],
        "expected": {
            "Student Name": "name",
            "Grade Point Average": "cgpa",
            "Qualification Name": "degree",
            "Specialization Stream": "branch",
            "College Name": "college"
        }
    },
    "passport_forms": {
        "labels": ["Travel Document No", "Nation of Citizenship", "Full Name of Father", "Birthday"],
        "expected": {
            "Travel Document No": "passport_number",
            "Nation of Citizenship": "nationality",
            "Full Name of Father": "father_name",
            "Birthday": "dob"
        }
    },
    "visa_forms": {
        "labels": ["Visa Permit Number", "Mother's Full Name", "Age in Years", "Correspondence Address"],
        "expected": {
            "Visa Permit Number": "visa_number",
            "Mother's Full Name": "mother_name",
            "Age in Years": "age",
            "Correspondence Address": "address"
        }
    },
    "insurance_forms": {
        "labels": ["Customer Full Name", "Contact Mobile", "Electronic Mail ID", "Mailing Zip Code"],
        "expected": {
            "Customer Full Name": "name",
            "Contact Mobile": "phone",
            "Electronic Mail ID": "email",
            "Mailing Zip Code": "pincode"
        }
    },
    "job_application_forms": {
        "labels": ["Name of Employer", "Staff Name", "Telephone", "Province"],
        "expected": {
            "Name of Employer": "company",
            "Staff Name": "name",
            "Telephone": "phone",
            "Province": "state"
        }
    }
}

def run_mapping_test(labels):
    data = json.dumps({"labels": labels}).encode("utf-8")
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

def main():
    print("==================================================")
    print("1. Executing ML Training Pipeline & Accuracy Comparison")
    print("==================================================")
    
    # Configure logger to print to stdout for visibility
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
    
    results = ModelTrainer.train_and_evaluate()
    print(f"Training completed successfully!")
    print(f"  Random Forest Accuracy: {results['rf_accuracy']:.4f}")
    print(f"  XGBoost Accuracy:       {results['xgb_accuracy']:.4f}")
    print(f"  Saved Best Model:       {results['best_model_name']} ({results['best_accuracy']:.4f})")
    
    print("\n==================================================")
    print("2. Verifying Semantic Mapping API Mappings")
    print("==================================================")
    
    passed = True
    
    for domain_name, data in TEST_DOMAINS.items():
        print(f"\n--- Testing Domain: {domain_name.replace('_', ' ').title()} ---")
        labels = data["labels"]
        expected = data["expected"]
        
        response = run_mapping_test(labels)
        if not response or not response.get("success"):
            print(f"FAIL: Semantic mapping API failed for domain {domain_name}")
            passed = False
            continue
            
        mappings = response["mappings"]
        confidences = response["confidences"]
        
        for label in labels:
            pred = mappings.get(label)
            conf = confidences.get(label, 0.0)
            exp = expected[label]
            
            if pred != exp:
                print(f"  [Mismatch] Label '{label}': Expected '{exp}', Got '{pred}' (Conf: {conf:.2f})")
                passed = False
            else:
                print(f"  [OK] Label '{label}' -> '{pred}' (Conf: {conf:.2f})")

    print("\n==================================================")
    if passed:
        print("SUCCESS: All semantic mapping tests passed successfully!")
    else:
        print("FAIL: Some semantic assertions failed.")
    print("==================================================")
    
    sys.exit(0 if passed else 1)

if __name__ == "__main__":
    main()
