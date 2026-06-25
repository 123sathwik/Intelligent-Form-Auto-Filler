from pydantic import BaseModel, Field
from typing import List

class PersonalInformationSchema(BaseModel):
    name: str = ""
    father_name: str = ""
    mother_name: str = ""
    gender: str = ""
    dob: str = ""
    age: str = ""
    nationality: str = ""

class ContactInformationSchema(BaseModel):
    email: str = ""
    phone: str = ""
    address: str = ""
    city: str = ""
    state: str = ""
    country: str = ""
    pincode: str = ""

class EducationSchema(BaseModel):
    college: str = ""
    university: str = ""
    degree: str = ""
    branch: str = ""
    cgpa: str = ""
    percentage: str = ""

class ProfessionalSchema(BaseModel):
    company: str = ""
    experience: str = ""
    skills: List[str] = Field(default_factory=list)
    projects: List[str] = Field(default_factory=list)
    certificates: List[str] = Field(default_factory=list)

class IdentificationSchema(BaseModel):
    passport_number: str = ""
    visa_number: str = ""
    pan_number: str = ""
    aadhaar_number: str = ""
    driving_license: str = ""

class StandardizedDocumentSchema(BaseModel):
    personal_information: PersonalInformationSchema = Field(default_factory=PersonalInformationSchema)
    contact_information: ContactInformationSchema = Field(default_factory=ContactInformationSchema)
    education: EducationSchema = Field(default_factory=EducationSchema)
    professional: ProfessionalSchema = Field(default_factory=ProfessionalSchema)
    identification: IdentificationSchema = Field(default_factory=IdentificationSchema)
