import random

class DocumentDatasetGenerator:
    @staticmethod
    def generate_raw_samples() -> list:
        """
        Generates a synthetic dataset of texts for training the document classifier.
        Returns a list of tuples: (text, label)
        """
        samples = []

        # Templates per document category
        templates = {
            "Resume": [
                "Vamsi Krishna. Email: abc@gmail.com, Phone: 9876543210. B.Tech Computer Science student at Stanford. Skills: Python, TypeScript, React, Docker, FastAPI. Work experience: Software Engineer at Google Ltd. Project: Face recognition system using OpenCV.",
                "Jane Smith. Contact: jane.smith@email.com. Education: MCA from MIT. Technical Skills: Java, AWS, Kubernetes, Node.js. Experience: 3 years as Full Stack Developer at Amazon. Certificate: AWS Certified Cloud Practitioner.",
                "Alex Jones. Resume. Phone: 111-222-3333. email: alex.j@gmail.com. Summary: Senior Data Scientist with 5 years experience in PyTorch and machine learning. Education: PhD in Statistics from Harvard. Projects: Recommendation Engine.",
                "Professional Resume of Sarah Connor. Email: sarah@skynet.com. Phone: 555-0199. Skills: C++, Systems Engineering, Security, Linux. Exp: Security Analyst at Cyberdyne Systems. B.S. in Electrical Engineering.",
                "Michael Scott. Contact details: michael@dundermifflin.com, 570-555-1212. Objective: Sales Manager with 15+ years experience. Education: B.A. from Penn State. Skills: Leadership, Negotiation, Relationship Building.",
            ],
            "Passport": [
                "PASSPORT. REPUBLIC OF INDIA. Type: P. Code: IND. Passport No: Z1234567. Surname: KRISHNA. Given Names: VAMSI. Nationality: INDIAN. Date of Birth: 12/08/2002. Gender: M. Place of Birth: HYDERABAD. Date of Issue: 20/06/2024. Date of Expiry: 19/06/2034. Authority: HYDERABAD.",
                "UNITED STATES OF AMERICA. PASSPORT. Passport No: 998877665. Surname: SMITH. Given Names: ALICE MAE. Nationality: USA. Date of Birth: 05 DEC 1995. Sex: F. Place of Birth: CALIFORNIA, USA. Date of Issue: 12 JAN 2021. Date of Expiry: 11 JAN 2031.",
                "PASSPORT / PASSEPORT. Republic of France. Passport Number: FRA8877112. Surname: DUPONT. Given Name: JEAN. Nationality: FRENCH. DOB: 18/02/1988. Gender: M. Date of Expiry: 25/08/2032. Place of Issue: PARIS.",
                "REPUBLIC OF GERMANY. PASSPORT. REISEPASS. Passport No: C8776529. Name: MUELLER. First Name: HANS. Nationality: DEUTSCH. DOB: 01.04.1990. Sex: M. Expiry: 30.06.2030.",
                "PASSPORT. Commonwealth of Australia. Document No: PA123456. Surname: JONES. Given Names: DAVID. Nationality: AUSTRALIAN. Date of Birth: 15/10/1985. Sex: M. Date of Expiry: 10/10/2035.",
            ],
            "Aadhaar": [
                "Government of India. Unique Identification Authority of India. Aadhaar Card. Aadhaar Number: 1234 5678 9012. Name: Vamsi Krishna. DOB: 12/08/2002. Gender: Male. Address: 104 Sunrise Apartments, Banjara Hills, Hyderabad, 500034. Father's Name: Ramakrishna Prasad. Mera Aadhaar, Meri Pehchan.",
                "Government of India. UIDAI. Aadhaar. Name: Rajesh Kumar. DOB: 15-05-1990. Male. Aadhaar No: 9876 5432 1098. Address: H.No 45, Sector 15, Noida, Uttar Pradesh, 201301.",
                "AADHAAR CARD. Government of India. Enrollment No: 100223/88921. Name: Priya Sharma. Year of Birth: 1993. Female. Aadhaar: 4433 2211 0099. Address: Flat 402, Royal Residency, Pune, Maharashtra - 411001.",
                "Government of India. Aadhaar. Name: Amit Singh. Date of Birth: 22/11/1980. Male. Aadhaar Number: 5566 7788 9900. Father's Name: Harbhajan Singh. Address: G.T. Road, Amritsar, Punjab - 143001.",
                "UNIQUE IDENTIFICATION AUTHORITY OF INDIA. Aadhaar Card. Aadhaar No: 1111 2222 3333. Name: Sunita Devi. DOB: 05/06/1975. Female. Address: Vill-Rampur, Post-Chanda, Varanasi, UP, 221001.",
            ],
            "PAN Card": [
                "INCOME TAX DEPARTMENT. GOVERNMENT OF INDIA. Permanent Account Number Card. PAN Card. PAN Number: ABCDE1234F. Name: Vamsi Krishna. Father's Name: Ramakrishna Prasad. Date of Birth: 12/08/2002. Card Type: Individual. Signature of Cardholder.",
                "INCOME TAX DEPT. Govt of India. PAN Card. Permanent Account Number: XYZWP9876A. Name: Rajesh Kumar. Father's Name: Sh. Satish Kumar. DOB: 15/05/1990. Category: Individual.",
                "GOVERNMENT OF INDIA. INCOME TAX DEPARTMENT. PAN CARD. Permanent Account Number: QWERT5544B. Cardholder: Priya Sharma. Father's Name: Vijay Sharma. Date of Birth: 25/07/1993.",
                "INCOME TAX DEPARTMENT. Govt of India. PAN: LKMJP1122C. Name: Amit Singh. Father's name: Harbhajan Singh. DOB: 22/11/1980. Status: Individual.",
                "INCOME TAX DEPARTMENT. Permanent Account Number: PLKJS9988D. Name: Sunita Devi. Father: Ramesh Chand. DOB: 05/06/1975.",
            ],
            "Driving License": [
                "STATE LICENSING AUTHORITY. Driving Licence. DL Number: DL1420110068991. Name: Vamsi Krishna. Father's Name: Ramakrishna Prasad. Address: 104 Sunrise Apartments, Banjara Hills, Hyderabad, Telangana, 500034. Licence Class: LMV, MCWG. Valid From: 20/06/2021. Valid To: 19/06/2041.",
                "UNION TERRITORY OF DELHI. Transport Department. Driving License. DL No: DL-042020004921. Name: Rajesh Kumar. Father's Name: Satish Kumar. DOB: 15/05/1990. Address: Sector 15, Dwarka, Delhi - 110075. Valid Upto: 14/05/2035.",
                "MAHARASHTRA STATE MOTOR VEHICLES DEPT. Driving Licence. License No: MH-12-20150022312. Name: Priya Sharma. DOB: 25/07/1993. Address: Royal Residency, Pune - 411001. Class: LMV. Issued: 10/10/2015. Expiry: 09/10/2035.",
                "STATE OF CALIFORNIA. DRIVER LICENSE. DL No: CA9928172. Name: Alice Smith. DOB: 12/05/1995. Address: 742 Evergreen Terrace, Los Angeles, CA 90001. Class: C. Date of Issue: 15/06/2022. Expiry Date: 12/05/2027.",
                "TRANSPORT DEPARTMENT. State of Punjab. Driving License. DL No: PB-02-199920042. Name: Amit Singh. Father: Harbhajan Singh. Address: Amritsar. Class: LMV, Trans. Valid: 22/11/2000 to 21/11/2020.",
            ],
            "Invoice": [
                "Acme Corporation. INVOICE. Invoice Number: INV-998822. Date: 25/06/2026. Due Date: 25/07/2026. PO Number: PO-10023. Vendor Details: Acme Corp, 123 Industrial Way, Silicon Valley, CA 94025, support@acme.com, Tax ID: TX-8877. Bill To: Customer Name: Vamsi Krishna, Address: 104 Sunrise Apts, Hyderabad. Items: Widget X - Qty 10 - Price $45.00 - Total $450.00. Subtotal: $450.00. Tax: $45.00. Total Amount: $495.00. Payment Status: Pending.",
                "Tech Solutions Inc. INVOICE. Inv No: TS-2026-004. Date: 12/05/2026. Bill To: Enterprise Corp, 500 Market St, San Francisco, CA. PO: PO-99881. Total Due: $10,500.00. Please send payments to billing@techsolutions.com.",
                "INVOICE / FACTURE. Global Delivery Services. Invoice Number: GDS-9908. Date: May 1, 2026. Due: May 31, 2026. Customer: Priya Sharma. Description: Shipping Fees. Subtotal: $120.00. Tax (15%): $18.00. Total Due: $138.00.",
                "TAX INVOICE. Supermart Retail Pvt Ltd. Invoice No: RET-5541. Date: 25/06/2026. Cashier: Rajesh K. Items: Groceries - $50.00, Household items - $35.00. CGPA/SGST: 18%. Total Invoice Amount: $100.30.",
                "Billing Statement & Invoice. Clean Water Co. Invoice Number: CW-9821. Date: 15/06/2026. Due Date: 30/06/2026. Account: ACT-8822. Services rendered: Water filtration maintenance. Total Balance: $75.00.",
            ],
            "Bank Statement": [
                "Chase Bank. Account Statement. Statement Period: June 1, 2026 - June 25, 2026. Bank Name: Chase Bank, New York. Account Number: 112233445566. Account Holder: Vamsi Krishna. Opening Balance: $10,500.00. Closing Balance: $12,450.00. Deposits: $2,500.00. Withdrawals: $550.00. Transaction Details: ATM Cash - $100, Direct Deposit - $2000, Store Purchase - $450.",
                "STATE BANK OF INDIA. Savings Bank Account Statement. Account No: 33442211001. Statement Period: 01/05/2026 to 31/05/2026. Account Holder: Rajesh Kumar. Branch: Dwarka, Delhi. Available Balance: INR 75,430.00. Summary: Dr Count: 5, Cr Count: 2.",
                "HDFC BANK. Current Account Statement. Statement Period: April 2026. Account Number: 501002231244. Name: Priya Sharma. Opening: INR 1,20,000. Closing: INR 1,45,000. Total Deposits: INR 45,000. Total Withdrawals: INR 20,000.",
                "Bank of America. Statement of Account. Account No: 4880998822. Period: 05/12/2025 to 05/01/2026. Name: Alice Smith. Beginning Balance: $5,230.15. Ending Balance: $4,820.50. Interest Earned: $0.12.",
                "WELLS FARGO BANK. Savings Account Statement. Period: June 2026. Account Holder: John Doe. Account: WF-99882. Opening Balance: $2,500.00. Closing Balance: $2,490.00. Monthly Service Fee: $10.00.",
            ],
            "Medical Report": [
                "City Health Care Clinic. Patient Medical Report. Patient Name: Vamsi Krishna. Patient ID: PAT-9988. Age: 24. Gender: Male. Date of Birth: 12/08/2002. Report Date: 25/06/2026. Doctor Name: Dr. Arthur Conan. Diagnosis: Acute Bronchitis. Symptoms: Persistent dry cough, mild fever, chest congestion. Recommendations: Bed rest for 3 days, cough syrup 10ml thrice daily, antibiotics. Tests Performed: Chest X-Ray (Normal), Blood Test.",
                "Mayo Medical Center. Lab & Clinical Report. Doctor: Dr. Elizabeth Blackwell. Patient: John Doe. Patient ID: 887-223. Age: 45. Gender: Male. Report Date: 12/05/2026. Diagnosis: Hypertension, Vitamin D Deficiency. Treatment: 5000 IU Vitamin D3 daily, Lisinopril 10mg.",
                "Apollo Hospitals. Health Checkup Report. Patient: Priya Sharma. Age: 33. Sex: Female. Ref Doctor: Dr. Nair. Symptoms: Fatigue and joint pain. Diagnosis: Rheumatoid Arthritis suspected. Recommended: RA Factor test, Physiotherapy.",
                "Diagnostic Laboratory Report. Quest Diagnostics. Patient Name: Alice Smith. Age: 31. Date: 15/06/2026. Tests: Complete Blood Count (CBC), Lipid Profile. Results: Cholesterol: 210 mg/dL (Borderline High), Hemoglobin: 13.5 g/dL (Normal).",
                "City Dental Care. Clinical Summary. Patient ID: DENT-441. Patient: Rajesh Kumar. Age: 36. Diagnosis: Dental Caries in lower left molar. Recommendations: Root Canal Treatment (RCT) and Crown placement.",
            ],
            "Research Paper": [
                "Deep Learning for Natural Language Processing. Authors: Vamsi Krishna, Arthur Conan. Publication Date: 12/05/2026. Journal/Conference: Journal of Artificial Intelligence Research. Abstract: This research paper proposes an advanced semantic mapping framework using Sentence Transformers and deep learning. We analyze tabular entity patterns and demonstrate state-of-the-art results on form matching. Keywords: Machine Learning, NLP, Embedding, Sentence Transformers, Text Extraction. DOI: 10.1109/JAIR.2026.100223.",
                "Attention Is All You Need. Authors: Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit. Abstract: We propose a new simple network architecture, the Transformer, based solely on attention mechanisms, dispensing with recurrence and convolutions entirely. Conference: NeurIPS 2017. DOI: 10.5555/3295222.3295349.",
                "Generative Adversarial Nets. Authors: Ian Goodfellow, Jean Pouget-Abadie, Yoshua Bengio. Journal: arXiv. Abstract: We propose a new framework for estimating generative models via an adversarial process, in which we simultaneously train two models: a generative model and a discriminative model.",
                "ResNet: Deep Residual Learning for Image Recognition. Authors: Kaiming He, Xiangyu Zhang, Shaoqing Ren, Jian Sun. Conference: CVPR 2016. Abstract: We present a residual learning framework to ease the training of networks that are substantially deeper than those previously used. DOI: 10.1109/CVPR.2016.90.",
                "BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding. Authors: Jacob Devlin, Ming-Wei Chang, Kenton Lee, Kristina Toutanova. Abstract: We introduce a new language representation model called BERT, which stands for Bidirectional Encoder Representations from Transformers. Keywords: NLP, Pre-training, Transformers.",
            ],
            "Egg AI Report": [
                "Egg Inspection Quality Control Report. Batch Number: EGG-20260625. Inspection Date: 25/06/2026. Total Eggs: 10000. Grade A Eggs: 9500. Grade B Eggs: 400. Rejects: 100. Temperature: 22C. Humidity: 55%. Inspector Name: Inspector John Doe. Quality Grade: PASS. Comments: High-yield batch with minimal shell abnormalities. Reject count is within acceptable threshold.",
                "Poultry Tech AI. Egg Quality Analysis Report. Batch: BATCH-8872. Date: 12/05/2026. Inspector: Rajesh Kumar. Total Count: 5000. Grade A: 4800. Grade B: 150. Reject Count: 50. Temperature: 21.5 C. Humidity: 50%. Status: Approved.",
                "Egg Processing Facility Report. Quality Grade Inspection. Batch: EP-998822. Date: 22/04/2026. Inspector: Sunita Devi. Temperature: 20C. Humidity: 58%. Total Checked: 12000. Grade A Count: 11200. Grade B Count: 600. Rejects: 200.",
                "AI Egg Grading & Sorting Log. Automated Inspector: EGG-BOT-v2. Batch Number: AUTO-9911. Date: 15/06/2026. Total sorted eggs: 25000. Premium Grade A: 24200. Standard Grade B: 600. Rejects/Broken: 200. Temp: 19C. Humidity: 52%.",
                "EGG QUALITY REPORT. Batch Ref: EGG-9921. Date: May 10, 2026. Total Eggs Scanned: 8000. Grade A: 7600. Grade B: 300. Rejects: 100. Ambient Temp: 23C. Humidity: 60%. Lead Inspector: Alice Smith.",
            ],
            "Certificate": [
                "Certificate of Achievement. AWS Certified Solutions Architect. Recipient Name: Vamsi Krishna. Issuing Organization: Amazon Web Services (AWS). Issue Date: 25/06/2026. Credential ID: AWS-CSA-998822. Course/Achievement: Successfully completed all criteria and examinations for the Solutions Architect certification.",
                "Stanford University. CERTIFICATE OF COMPLETION. This is to certify that John Doe has successfully completed the Course: Deep Learning Specialization. Issued on 12/05/2026. Credential ID: STFD-DL-8829.",
                "Docker Certified Associate. Certificate of Excellence. Awarded to: Priya Sharma. Issued by: Docker Inc. Date of Issue: 15/01/2026. Credential ID: DCA-9988223.",
                "CERTIFICATE OF PARTICIPATION. International Conference on Machine Learning (ICML). Recipient: Amit Singh. For attending the workshop on Generative AI. Date: 18/06/2026. Organization: ICML Board.",
                "Google Cloud Certified. Professional Data Engineer Certificate. This certifies that Rajesh Kumar has met the requirements for Google Cloud Professional Data Engineer. Credential ID: GCP-PDE-4412. Issued: 10/11/2025.",
            ],
            "Generic Document": [
                "Intelligent Form Auto-Filler Test PDF. This is a test PDF file to verify PyMuPDF and pdfplumber extraction. Subject: Project update and general guidelines. Date: 06/25/2026. Author: Developer. Description: System validation and regression testing.",
                "General Meeting Notes. Date: May 15, 2026. Author: Alice Smith. Topic: Team coordination and roadmap discussion. Description: Aligning resources for the next phase of the project.",
                "MEMORANDUM. To: All Employees. From: Management. Date: 01/06/2026. Subject: Office Policy Updates. Description: General announcement regarding office work hours and holiday calendar.",
                "Project Alpha Status Update. Summary: We have completed the research phase and are transitioning to implementation. Key milestones achieved: system design finalized, database schemas created.",
                "General Article: The History of Computing. Author: Charles Babbage. Publication Date: 10/10/2025. Description: Overview of the analytical engine and early computation concepts.",
            ]
        }

        # Let's generate a larger set by slightly modifying templates or adding noise
        for label, texts in templates.items():
            for text in texts:
                # Add sample directly
                samples.append((text, label))
                
                # Create 3 minor variations per template to expand the dataset
                for i in range(3):
                    noise_words = ["IMPORTANT", "VERIFIED", "AUTO", "SYSTEM", "DRAFT", "CONFIDENTIAL"]
                    prefix = random.choice(noise_words) + " - " if random.random() > 0.5 else ""
                    suffix = " [Verified at " + str(random.randint(10, 23)) + ":00]" if random.random() > 0.5 else ""
                    samples.append((prefix + text + suffix, label))

        # Shuffle dataset
        random.shuffle(samples)
        return samples
