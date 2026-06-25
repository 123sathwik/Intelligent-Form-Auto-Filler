from pydantic import BaseModel, Field
from typing import List

# ==========================================
# 1. Resume Schema
# ==========================================
class ResumePersonal(BaseModel):
    name: str = ""
    dob: str = ""
    gender: str = ""
    nationality: str = ""

class ResumeContact(BaseModel):
    email: str = ""
    phone: str = ""
    address: str = ""

class ResumeEducation(BaseModel):
    college: str = ""
    degree: str = ""
    branch: str = ""
    cgpa: str = ""

class ResumeProfessional(BaseModel):
    company: str = ""
    experience: str = ""
    skills: List[str] = Field(default_factory=list)
    projects: List[str] = Field(default_factory=list)
    certificates: List[str] = Field(default_factory=list)

class ResumeSchema(BaseModel):
    personal_information: ResumePersonal = Field(default_factory=ResumePersonal)
    contact_information: ResumeContact = Field(default_factory=ResumeContact)
    education: ResumeEducation = Field(default_factory=ResumeEducation)
    professional: ResumeProfessional = Field(default_factory=ResumeProfessional)


# ==========================================
# 2. Passport Schema
# ==========================================
class PassportDetails(BaseModel):
    passport_number: str = ""
    country_code: str = ""
    surname: str = ""
    given_names: str = ""
    nationality: str = ""
    dob: str = ""
    gender: str = ""
    place_of_birth: str = ""
    place_of_issue: str = ""
    date_of_issue: str = ""
    date_of_expiry: str = ""

class PassportSchema(BaseModel):
    passport_details: PassportDetails = Field(default_factory=PassportDetails)


# ==========================================
# 3. Aadhaar Schema
# ==========================================
class AadhaarDetails(BaseModel):
    aadhaar_number: str = ""
    name: str = ""
    dob: str = ""
    gender: str = ""
    address: str = ""
    father_or_spouse_name: str = ""

class AadhaarSchema(BaseModel):
    aadhaar_details: AadhaarDetails = Field(default_factory=AadhaarDetails)


# ==========================================
# 4. PAN Card Schema
# ==========================================
class PanDetails(BaseModel):
    pan_number: str = ""
    name: str = ""
    father_name: str = ""
    dob: str = ""
    card_type: str = ""

class PanCardSchema(BaseModel):
    pan_details: PanDetails = Field(default_factory=PanDetails)


# ==========================================
# 5. Driving License Schema
# ==========================================
class DrivingLicenseDetails(BaseModel):
    driving_license_number: str = ""
    name: str = ""
    father_or_spouse_name: str = ""
    dob: str = ""
    address: str = ""
    license_class: str = ""
    date_of_issue: str = ""
    date_of_expiry: str = ""

class DrivingLicenseSchema(BaseModel):
    license_details: DrivingLicenseDetails = Field(default_factory=DrivingLicenseDetails)


# ==========================================
# 6. Invoice Schema
# ==========================================
class InvoiceDetails(BaseModel):
    invoice_number: str = ""
    invoice_date: str = ""
    due_date: str = ""
    po_number: str = ""

class VendorDetails(BaseModel):
    vendor_name: str = ""
    vendor_address: str = ""
    vendor_email: str = ""
    vendor_phone: str = ""
    tax_id: str = ""

class CustomerDetails(BaseModel):
    customer_name: str = ""
    customer_address: str = ""
    customer_email: str = ""
    customer_phone: str = ""

class PaymentDetails(BaseModel):
    subtotal: str = ""
    tax_amount: str = ""
    total_amount: str = ""
    payment_status: str = ""

class InvoiceSchema(BaseModel):
    invoice_details: InvoiceDetails = Field(default_factory=InvoiceDetails)
    vendor_details: VendorDetails = Field(default_factory=VendorDetails)
    customer_details: CustomerDetails = Field(default_factory=CustomerDetails)
    payment_details: PaymentDetails = Field(default_factory=PaymentDetails)


# ==========================================
# 7. Bank Statement Schema
# ==========================================
class BankDetails(BaseModel):
    bank_name: str = ""
    account_number: str = ""
    account_holder: str = ""
    statement_period: str = ""
    opening_balance: str = ""
    closing_balance: str = ""

class BankStatementSchema(BaseModel):
    bank_details: BankDetails = Field(default_factory=BankDetails)


# ==========================================
# 8. Medical Report Schema
# ==========================================
class PatientDetails(BaseModel):
    patient_name: str = ""
    age: str = ""
    gender: str = ""
    dob: str = ""
    patient_id: str = ""

class ClinicalDetails(BaseModel):
    report_date: str = ""
    doctor_name: str = ""
    diagnosis: str = ""
    symptoms: str = ""
    recommendations: str = ""
    tests_performed: str = ""

class MedicalReportSchema(BaseModel):
    patient_details: PatientDetails = Field(default_factory=PatientDetails)
    clinical_details: ClinicalDetails = Field(default_factory=ClinicalDetails)


# ==========================================
# 9. Research Paper Schema
# ==========================================
class PaperDetails(BaseModel):
    title: str = ""
    authors: str = ""
    abstract: str = ""
    publication_date: str = ""
    journal_or_conference: str = ""
    keywords: str = ""
    doi: str = ""

class ResearchPaperSchema(BaseModel):
    paper_details: PaperDetails = Field(default_factory=PaperDetails)


# ==========================================
# 10. Egg AI Report Schema
# ==========================================
class EggDetails(BaseModel):
    batch_number: str = ""
    inspection_date: str = ""
    total_eggs: str = ""
    grade_a_count: str = ""
    grade_b_count: str = ""
    reject_count: str = ""
    temperature: str = ""
    humidity: str = ""
    inspector_name: str = ""

class EggAiReportSchema(BaseModel):
    egg_details: EggDetails = Field(default_factory=EggDetails)


# ==========================================
# 11. Certificate Schema
# ==========================================
class CertificateDetails(BaseModel):
    title: str = ""
    recipient_name: str = ""
    issuing_organization: str = ""
    issue_date: str = ""
    credential_id: str = ""
    course_or_achievement: str = ""

class CertificateSchema(BaseModel):
    certificate_details: CertificateDetails = Field(default_factory=CertificateDetails)


# ==========================================
# 12. Generic Document Schema
# ==========================================
class DocumentDetails(BaseModel):
    title: str = ""
    date: str = ""
    author: str = ""
    description: str = ""
    content_summary: str = ""

class GenericDocumentSchema(BaseModel):
    document_details: DocumentDetails = Field(default_factory=DocumentDetails)


# Registry mapping document type to its pydantic model schema
SCHEMA_MAP = {
    "Resume": ResumeSchema,
    "Passport": PassportSchema,
    "Aadhaar": AadhaarSchema,
    "PAN Card": PanCardSchema,
    "Driving License": DrivingLicenseSchema,
    "Invoice": InvoiceSchema,
    "Bank Statement": BankStatementSchema,
    "Medical Report": MedicalReportSchema,
    "Research Paper": ResearchPaperSchema,
    "Egg AI Report": EggAiReportSchema,
    "Certificate": CertificateSchema,
    "Generic Document": GenericDocumentSchema
}
