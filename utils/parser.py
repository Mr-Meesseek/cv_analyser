import re

def parse_cv(text):
    """Parse the extracted text and structure it into JSON."""
    result = {
        "name": "",
        "email": "",
        "phone": "",
        "address": "",
        "social_media": [],
        "summary": "",
        "interests": [],
        "languages": [],
        "education": [],
        "pro_experience": [],
        "certifications": [],
        "skills": [],
        "projects": []
    }

    # Extract name
    name_match = re.search(r"(?i)(Ismail\s+Salem)", text)
    if name_match:
        result["name"] = name_match.group(0).strip()

    # Extract email
    email_match = re.search(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", text)
    if email_match:
        result["email"] = email_match.group(0)

    # Extract phone number
    phone_match = re.search(r"(\+?\d{1,3}[\s\-]?\d{2,3}[\s\-]?\d{3,4}[\s\-]?\d{3,4})", text)
    if phone_match:
        result["phone"] = phone_match.group(0).strip()

    # Extract address
    address_match = re.search(r"(?i)(Monastir,\s+[A-Za-z\s]+[\d]+)", text)
    if address_match:
        result["address"] = address_match.group(0).strip()

    # Extract social media
    social_media_matches = re.findall(r"(git\s+[^\s,]+|linkedin\s+[^\s,]+)", text, re.IGNORECASE)
    result["social_media"] = [sm.strip() for sm in social_media_matches]

    # Extract summary
    summary_match = re.search(r"summary\s*:\s*(.*?)\n\n", text, re.DOTALL | re.IGNORECASE)
    if summary_match:
        result["summary"] = summary_match.group(1).strip()

    # Extract interests
    interests_match = re.search(r"interests\s*(.*?)(?=\n[A-Z])", text, re.DOTALL | re.IGNORECASE)
    if interests_match:
        interests = interests_match.group(1).strip().split("\n")
        result["interests"] = [interest.strip() for interest in interests if interest.strip()]

    # Extract languages
    languages_match = re.search(r"languages and levels\s*(.*?)(?=\n[A-Z])", text, re.DOTALL | re.IGNORECASE)
    if languages_match:
        languages = languages_match.group(1).strip().split("\n")
        result["languages"] = [lang.strip() for lang in languages if lang.strip()]

    # Extract education
    education_matches = re.findall(r"(DEGREE IN [\w\s]+)\s+([\w\s]+)\s+(\d{2}/\d{4}\s*–\s*\d{2}/\d{4}|\d{4})\s+\|\s+([\w\s]+)", text, re.IGNORECASE)
    result["education"] = [f"{edu[0]} {edu[1]} {edu[2]} | {edu[3]}" for edu in education_matches]

    # Extract professional experience
    experience_matches = re.findall(r"([\w\s]+),\s+(\d{2}/\d{4}\s*–\s*(?:present|\d{2}/\d{4}))\s+\|\s+([\w\s]+)", text, re.IGNORECASE)
    result["pro_experience"] = [f"{exp[0]} {exp[1]} | {exp[2]}" for exp in experience_matches]

    # Extract certifications
    certifications_matches = re.findall(r"(Responsive web design|Introduction to Git|Introduction to SQL|Ui/Ux|Foundation of Probability in Python)\s+([\w\s]+)", text, re.IGNORECASE)
    result["certifications"] = [f"{cert[0]} {cert[1]}" for cert in certifications_matches]

    # Extract skills
    skills_match = re.search(r"skills\s*(.*?)(?=\n[A-Z])", text, re.DOTALL | re.IGNORECASE)
    if skills_match:
        skills = skills_match.group(1).strip().split("\n")
        result["skills"] = [skill.strip() for skill in skills if skill.strip()]

    # Extract projects
    projects_match = re.search(r"projects\s*(.*?)(?=\n[A-Z])", text, re.DOTALL | re.IGNORECASE)
    if projects_match:
        projects = projects_match.group(1).strip().split("\n")
        result["projects"] = [project.strip() for project in projects if project.strip()]

    return result