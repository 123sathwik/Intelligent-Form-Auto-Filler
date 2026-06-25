from typing import Any
from app.standardizer.field_mapper import FieldMapper
from app.standardizer.normalizer import Normalizer
from app.classification.schemas import SCHEMA_MAP

def set_nested_value(d: dict, path: str, value: Any):
    """Dynamically sets a nested dictionary value using a dot-separated path."""
    keys = path.split('.')
    current = d
    for key in keys[:-1]:
        if key not in current:
            current[key] = {}
        current = current[key]
    current[keys[-1]] = value

class Standardizer:
    @staticmethod
    def standardize(data: dict, document_type: str = "Generic Document") -> dict:
        """
        Translates raw/flat/nested extracted entity data into the intermediate standardized JSON format.
        Determines target schema dynamically based on document_type.
        """
        # 1. Handle nested 'entities' dictionary if it was forwarded from the NLP pipeline
        source = data.get("entities") if "entities" in data and isinstance(data["entities"], dict) else data
        
        # 2. Get the correct target schema class
        schema_class = SCHEMA_MAP.get(document_type, SCHEMA_MAP["Generic Document"])
        
        # 3. Create default template dictionary using Pydantic defaults
        schema_dict = schema_class().model_dump()
        
        # 4. Clean keys and normalize values
        for key, val in source.items():
            if val is None:
                continue
            path = FieldMapper.map_key_to_schema_path(key, document_type)
            if not path:
                continue
            
            # Apply specific normalizations depending on the target schema field
            # Check ends with field names to support dynamic schema paths (e.g. personal_information.dob, patient_details.dob)
            path_lower = path.lower()
            if path_lower.endswith(".name") or path_lower.endswith(".father_name") or path_lower.endswith(".mother_name") or path_lower.endswith(".father_or_spouse_name") or path_lower.endswith(".surname") or path_lower.endswith(".given_names") or path_lower.endswith(".account_holder"):
                normalized_val = Normalizer.normalize_name(val)
            elif path_lower.endswith(".gender") or path_lower.endswith(".sex"):
                normalized_val = Normalizer.normalize_gender(val)
            elif path_lower.endswith(".dob") or path_lower.endswith(".date_of_birth") or path_lower.endswith(".date") or path_lower.endswith(".invoice_date") or path_lower.endswith(".due_date") or path_lower.endswith(".issue_date") or path_lower.endswith(".date_of_issue") or path_lower.endswith(".date_of_expiry") or path_lower.endswith(".expiry_date") or path_lower.endswith(".inspection_date"):
                normalized_val = Normalizer.normalize_date(val)
            elif path_lower.endswith(".age"):
                normalized_val = Normalizer.normalize_age(val)
            elif path_lower.endswith(".cgpa") or path_lower.endswith(".gpa"):
                normalized_val = Normalizer.normalize_cgpa(val)
            elif path_lower.endswith(".percentage"):
                normalized_val = Normalizer.normalize_percentage(val)
            elif path_lower.endswith(".skills") or path_lower.endswith(".projects") or path_lower.endswith(".certificates") or path_lower.endswith(".keywords"):
                normalized_val = Normalizer.normalize_list(val)
            elif path_lower.endswith(".experience"):
                normalized_val = Normalizer.normalize_experience(val)
            else:
                # Basic string fields: strip and stringify
                normalized_val = str(val).strip()
                
            set_nested_value(schema_dict, path, normalized_val)
            
        # 5. Instantiate and dump the Pydantic schema to ensure final validation and defaults
        standardized_model = schema_class(**schema_dict)
        return standardized_model.model_dump()
