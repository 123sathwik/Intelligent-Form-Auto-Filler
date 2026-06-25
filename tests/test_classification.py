import sys
from pathlib import Path

# Add backend directory to path
backend_dir = Path("c:/Users/Admin/OneDrive/auto filler/backend")
sys.path.append(str(backend_dir))

from app.classification.classifier import DocumentClassifier

def run_tests():
    print("=" * 50)
    print("Testing Document Classification Module")
    print("=" * 50)

    # Trigger initial training / loading
    print("Initializing classifier resources...")
    model, encoder = DocumentClassifier.get_resources()
    print("Classifier loaded successfully.")

    test_cases = [
        (
            "Resume of Vamsi Krishna. Stanford B.Tech. Skills: Python, React, FastAPI. Experience: Software Engineer at Google.",
            "Resume"
        ),
        (
            "PASSPORT. REPUBLIC OF INDIA. Passport No: Z9918273. Surname: CONAN. Given Name: ARTHUR. Nationality: INDIAN. DOB: 22/05/1990.",
            "Passport"
        ),
        (
            "Unique Identification Authority of India. Aadhaar Card Number: 4433 2211 0099. Name: Priya Sharma. DOB: 1993. Address: Pune.",
            "Aadhaar"
        ),
        (
            "INCOME TAX DEPARTMENT. GOVERNMENT OF INDIA. PAN Number: ABCDE1234F. Name: Amit Singh. Father's Name: Harbhajan Singh.",
            "PAN Card"
        ),
        (
            "State of California. Driver License. DL No: CA991827. Name: Alice Smith. Class: C. Expiry: 12/05/2027.",
            "Driving License"
        ),
        (
            "Acme Corporation. TAX INVOICE. Invoice Number: INV-998822. Due Date: 25/07/2026. Subtotal: $450.00. Tax: $45.00. Total Due: $495.00.",
            "Invoice"
        ),
        (
            "Chase Bank. Account Statement. Period: June 2026. Account Holder: Vamsi Krishna. Ending Balance: $12,450.00.",
            "Bank Statement"
        ),
        (
            "City Health Care Clinic. Patient Medical Report. Patient Name: Vamsi Krishna. Diagnosis: Acute Bronchitis. Doctor: Dr. Arthur Conan.",
            "Medical Report"
        ),
        (
            "Attention Is All You Need. Abstract: We propose a new network architecture, the Transformer. Keywords: Deep Learning, NLP.",
            "Research Paper"
        ),
        (
            "Egg Inspection Quality Control Report. Batch Number: EGG-20260625. Total Eggs: 10000. Rejects: 100. Grade A Eggs: 9500.",
            "Egg AI Report"
        ),
        (
            "Certificate of Completion. This certifies that John Doe has successfully completed the Deep Learning Specialization course.",
            "Certificate"
        ),
        (
            "Meeting memo. Subject: Project roadmap. Date: 06/25/2026. Author: Lead Developer. Description: general update.",
            "Generic Document"
        )
    ]

    passed = 0
    for text, expected in test_cases:
        result = DocumentClassifier.classify(text)
        pred = result["document_type"]
        conf = result["confidence"]
        
        status = "PASSED" if pred == expected else "FAILED"
        print(f"[{status}] Expected: {expected:<18} -> Predicted: {pred:<18} (Confidence: {conf}%)")
        if pred == expected:
            passed += 1

    print("-" * 50)
    print(f"Results: {passed}/{len(test_cases)} tests passed.")
    print("=" * 50)

    if passed == len(test_cases):
        print("SUCCESS: All classifier tests passed!")
        sys.exit(0)
    else:
        print("ERROR: Some tests failed.")
        sys.exit(1)

if __name__ == "__main__":
    run_tests()
