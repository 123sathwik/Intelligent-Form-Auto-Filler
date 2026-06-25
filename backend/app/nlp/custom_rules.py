import re

COMMON_SKILLS = [
    "Python", "Java", "C++", "C#", "Javascript", "TypeScript", "React", "Angular", "Vue",
    "FastAPI", "Django", "Flask", "SQL", "MySQL", "PostgreSQL", "MongoDB", "Docker",
    "Kubernetes", "AWS", "Azure", "GCP", "Machine Learning", "Deep Learning", "NLP",
    "Data Science", "HTML", "CSS", "Node.js", "Express", "Git", "GitHub", "Linux",
    "Tailwind", "Bootstrap", "C", "PHP", "Ruby", "Rails", "Go", "Rust", "Swift", "Kotlin"
]

COMMON_DEGREES = [
    "B.Tech", "M.Tech", "B.Sc", "M.Sc", "B.E", "M.E", "B.B.A", "M.B.A", "B.C.A", "M.C.A",
    "Ph.D", "B.Com", "M.Com", "B.A", "M.A", "B.S", "M.S", "Bachelor of Technology",
    "Master of Technology", "Bachelor of Engineering", "Master of Engineering",
    "Bachelor of Science", "Master of Science", "Master of Business Administration",
    "Bachelor of Computer Applications", "Master of Computer Applications"
]

COMMON_BRANCHES = [
    "Computer Science", "Information Technology", "Computer Engineering",
    "Electrical Engineering", "Electronics and Communication", "Mechanical Engineering",
    "Civil Engineering", "Data Science", "Artificial Intelligence", "Software Engineering",
    "Cyber Security", "Aerospace Engineering", "Chemical Engineering"
]

class CustomRulesExtractor:
    @staticmethod
    def extract(text: str) -> dict:
        """
        Extracts heuristic/vocabulary entities like Degree, Branch, CGPA,
        Percentage, Skills, DOB, Age, Gender, Nationality, lists.
        """
        entities = {}
        
        # 1. Degree
        degree_found = ""
        for deg in COMMON_DEGREES:
            if re.search(r'\b' + re.escape(deg) + r'\b', text, re.IGNORECASE):
                degree_found = deg
                break
        entities["degree"] = degree_found

        # 2. Branch
        branch_found = ""
        for branch in COMMON_BRANCHES:
            if re.search(r'\b' + re.escape(branch) + r'\b', text, re.IGNORECASE):
                branch_found = branch
                break
        entities["branch"] = branch_found

        # 3. CGPA
        cgpa_match = re.search(
            r'\b(?:cgpa|gpa)\s*(?:of|is|:)?\s*([1-9]\.\d{1,2}|10(?:\.0)?)\b|\b([1-9]\.\d{1,2}|10(?:\.0)?)\s*(?:cgpa|gpa)\b', 
            text, 
            re.IGNORECASE
        )
        if cgpa_match:
            entities["cgpa"] = cgpa_match.group(1) or cgpa_match.group(2) or ""
        else:
            entities["cgpa"] = ""

        # 4. Percentage
        pct_match = re.search(
            r'\b(\d{1,2}(?:\.\d{1,2})?)\s*%(?!\w)|\b(?:percentage|percent|marks)\s*(?:of|is|:)?\s*(\d{1,2}(?:\.\d{1,2})?)\s*%(?!\w)', 
            text, 
            re.IGNORECASE
        )
        if pct_match:
            entities["percentage"] = pct_match.group(1) or pct_match.group(2) or ""
        else:
            entities["percentage"] = ""

        # 5. Gender
        gender_match = re.search(r'\bgender\s*:\s*(male|female|other)\b|\b(male|female)\b', text, re.IGNORECASE)
        if gender_match:
            entities["gender"] = (gender_match.group(1) or gender_match.group(2) or "").capitalize()
        else:
            entities["gender"] = ""

        # 6. Nationality
        nat_match = re.search(
            r'\bnationality\s*:\s*([a-z]+)\b|\b(indian|american|british|canadian|australian)\b', 
            text, 
            re.IGNORECASE
        )
        if nat_match:
            entities["nationality"] = (nat_match.group(1) or nat_match.group(2) or "").capitalize()
        else:
            entities["nationality"] = ""

        # 7. Date of Birth
        dob_match = re.search(
            r'\b(?:dob|date of birth|birth date|d\.o\.b)\s*[:\-]?\s*([a-z0-9 \t/.,-]+)\b', 
            text, 
            re.IGNORECASE
        )
        if dob_match:
            entities["dob"] = dob_match.group(1).strip()
        else:
            entities["dob"] = ""

        # 8. Age
        age_match = re.search(r'\bage\s*(?:is|:)?\s*(\d{1,2})\b|\b(\d{1,2})\s*years?\s*old\b', text, re.IGNORECASE)
        if age_match:
            entities["age"] = age_match.group(1) or age_match.group(2) or ""
        else:
            entities["age"] = ""

        # 9. Skills (List)
        skills_found = []
        for skill in COMMON_SKILLS:
            pattern = r'\b' + re.escape(skill) + r'\b'
            if skill == "C++":
                pattern = r'\bC\+\+'
            if re.search(pattern, text, re.IGNORECASE):
                skills_found.append(skill)
        entities["skills"] = skills_found

        # 10. Father & Mother Names
        father_match = re.search(
            r'\bfather(?:[\'\"]s)?(?:\s*name\s*[:\-]?|\s*[:\-])\s*(?:mr\.?\s+)?([a-z. \t]+)\b', 
            text, 
            re.IGNORECASE
        )
        entities["father_name"] = father_match.group(1).strip().title() if father_match else ""

        mother_match = re.search(
            r'\bmother(?:[\'\"]s)?(?:\s*name\s*[:\-]?|\s*[:\-])\s*(?:mrs?\.?\s+)?([a-z. \t]+)\b', 
            text, 
            re.IGNORECASE
        )
        entities["mother_name"] = mother_match.group(1).strip().title() if mother_match else ""

        # 11. Lists of lines matching sections (Experience, Projects, Certificates)
        lines = text.splitlines()
        exp_lines = []
        proj_lines = []
        cert_lines = []

        for line in lines:
            trimmed = line.strip()
            # Filter line lengths to get only meaningful short lines/titles
            if len(trimmed) < 150:
                trimmed_lower = trimmed.lower()
                # Experience keywords
                if any(k in trimmed_lower for k in ["experience", "worked as", "developer at", "engineer at"]):
                    exp_lines.append(trimmed)
                # Project keywords
                if any(k in trimmed_lower for k in ["project", "developed", "built a"]):
                    proj_lines.append(trimmed)
                # Certificate keywords
                if any(k in trimmed_lower for k in ["certified", "certification", "credential"]):
                    cert_lines.append(trimmed)

        entities["experience"] = exp_lines[:5]
        entities["projects"] = proj_lines[:5]
        entities["certificates"] = cert_lines[:5]

        return entities
