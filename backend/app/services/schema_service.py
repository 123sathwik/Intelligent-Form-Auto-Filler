import json
import logging
from pathlib import Path
from typing import Any

logger = logging.getLogger("autofiller-backend")

# All schemas are stored relative to this file's location
SCHEMAS_DIR = Path(__file__).parent.parent.parent / "schemas"

# Canonical mapping: form_type name -> JSON filename (without .json)
FORM_REGISTRY = {
    "Resume": "resume",
    "Passport": "passport",
    "Aadhaar": "aadhaar",
    "PAN Card": "pan_card",
    "Driving License": "driving_license",
    "Medical Report": "medical_report",
    "Invoice": "invoice",
    "Bank KYC": "bank_kyc",
    "Admission Form": "admission_form",
    "Insurance Claim": "insurance_claim",
    "Employee Registration": "employee_registration",
    "Student Registration": "student_registration",
    "Custom Form": "custom",
}

class SchemaService:
    """
    Loads JSON schema definitions from backend/schemas/ and performs
    entity-to-field auto-fill mapping.
    """

    @staticmethod
    def get_all() -> list:
        """Returns a list of all available form types with metadata."""
        result = []
        for form_type, filename in FORM_REGISTRY.items():
            schema_path = SCHEMAS_DIR / f"{filename}.json"
            entry = {
                "form_type": form_type,
                "filename": filename,
                "available": schema_path.exists()
            }
            if schema_path.exists():
                try:
                    with open(schema_path, "r", encoding="utf-8") as f:
                        data = json.load(f)
                    entry["icon"] = data.get("icon", "FileText")
                    entry["description"] = data.get("description", "")
                    entry["section_count"] = len(data.get("sections", []))
                    entry["field_count"] = sum(
                        len(s.get("fields", [])) for s in data.get("sections", [])
                    )
                except Exception as e:
                    logger.error(f"Error reading schema {filename}: {e}")
            result.append(entry)
        return result

    @staticmethod
    def get(form_type: str) -> dict | None:
        """
        Returns the full schema dict for a given form_type name.
        Returns None if not found.
        """
        filename = FORM_REGISTRY.get(form_type)
        if not filename:
            return None
        schema_path = SCHEMAS_DIR / f"{filename}.json"
        if not schema_path.exists():
            logger.error(f"Schema file not found: {schema_path}")
            return None
        try:
            with open(schema_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Error loading schema {filename}: {e}")
            return None

    @staticmethod
    def get_custom(custom_schema: dict) -> dict:
        """Validates and returns a user-defined custom schema dict."""
        return {
            "form_type": "Custom Form",
            "icon": "Puzzle",
            "description": custom_schema.get("description", "Custom user-defined form"),
            "sections": custom_schema.get("sections", [])
        }

    @staticmethod
    def autofill(schema: dict, entities: dict) -> dict:
        """
        Iterates through schema fields and matches entity_keys against
        extracted entities. Returns a flat dict:
        {
          "<section_id>.<field_id>": {
            "value": "...",
            "source": "auto" | "empty"
          }
        }
        """
        result = {}
        for section in schema.get("sections", []):
            section_id = section.get("id", "")
            for field in section.get("fields", []):
                field_id = field.get("id", "")
                entity_keys = field.get("entity_keys", [])
                key = f"{section_id}.{field_id}"

                matched_value = ""
                for ek in entity_keys:
                    val = entities.get(ek)
                    if val:
                        # Handle list values (skills, projects, certificates)
                        if isinstance(val, list):
                            matched_value = ", ".join(str(v) for v in val if v)
                        else:
                            matched_value = str(val).strip()
                        if matched_value:
                            break

                result[key] = {
                    "value": matched_value,
                    "source": "auto" if matched_value else "empty"
                }
        return result

    @staticmethod
    def build_form_data(schema: dict, autofill_map: dict) -> dict:
        """
        Converts the schema + autofill_map into the nested dict format
        consumed by the frontend DynamicForm component.
        {
          "section_id": { "field_id": "value", ... },
          ...
        }
        """
        form_data = {}
        for section in schema.get("sections", []):
            section_id = section.get("id", "")
            form_data[section_id] = {}
            for field in section.get("fields", []):
                field_id = field.get("id", "")
                key = f"{section_id}.{field_id}"
                entry = autofill_map.get(key, {"value": "", "source": "empty"})
                form_data[section_id][field_id] = entry["value"]
        return form_data
