def split_cv_into_sections(cv_text):
    sections = {}
    current_section = None
    for line in cv_text.splitlines():
        line = line.strip()
        if not line:
            continue
        if line.upper() in ["EDUCATION", "PROFESSIONAL EXPERIENCE", "CERTIFICATES", "SKILLS"]:
            current_section = line.upper()
            sections[current_section] = []
        elif current_section:
            sections[current_section].append(line)
    for section in sections:
        sections[section] = "\n".join(sections[section])
    return sections

def process_cv(cv_text, t5_model):
    sections = split_cv_into_sections(cv_text)
    structured_data = {}
    for section_name, section_text in sections.items():
        structured_data[section_name] = t5_model.generate_structured_data(section_text)
    return structured_data

def combine_results(structured_data):
    combined = {}
    for section, data in structured_data.items():
        combined[section] = data
    return combined