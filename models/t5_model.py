from transformers import T5Tokenizer, T5ForConditionalGeneration
class T5Model:
    def __init__(self, model_name="t5-base"):
        self.tokenizer = T5Tokenizer.from_pretrained(model_name)
        self.model = T5ForConditionalGeneration.from_pretrained(model_name)

    def generate_structured_data(self, text, section_name):
        # Define prompts based on the section name
        if section_name == "EDUCATION":
            prompt = (
                f"Extract the education details from the following CV section. "
                f"List all degrees, institutions, and dates:\n\n"
                f"Input:\n{text}\n\n"
                f"Output format:\n"
                f"Education:\n- Degree: [Degree Name], Institution: [Institution Name], Dates: [Start-End]\n"
            )
        elif section_name == "PROFESSIONAL EXPERIENCE":
            prompt = (
                f"Extract the professional experience details from the following CV section. "
                f"List all job titles, companies, and dates:\n\n"
                f"Input:\n{text}\n\n"
                f"Output format:\n"
                f"Experience:\n- Job Title: [Job Title], Company: [Company Name], Dates: [Start-End]\n"
            )
        elif section_name == "CERTIFICATES":
            prompt = (
                f"Extract the certificates from the following CV section. "
                f"List all certificates and their dates:\n\n"
                f"Input:\n{text}\n\n"
                f"Output format:\n"
                f"Certifications:\n- Certificate: [Certificate Name], Date: [Date]\n"
            )
        elif section_name == "SKILLS":
            prompt = (
                f"Extract the skills from the following CV section. "
                f"List all skills:\n\n"
                f"Input:\n{text}\n\n"
                f"Output format:\n"
                f"Skills:\n- [Skill 1]\n- [Skill 2]\n"
            )
        else:
            # Default prompt for unrecognized sections
            prompt = (
                f"Extract the following fields from the CV section and organize them into categories:\n\n"
                f"Input:\n{text}\n\n"
                f"Output format:\n"
                f"Fields:\n- [Field 1]\n- [Field 2]\n"
            )

        # Tokenize the prompt and generate output
        inputs = self.tokenizer(prompt, return_tensors="pt", max_length=1024, truncation=True)
        outputs = self.model.generate(inputs.input_ids, max_length=1024, num_beams=4, early_stopping=True)
        result = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return result

    def split_cv_into_sections(self, cv_text):
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

    def process_cv(self, cv_text):
        sections = self.split_cv_into_sections(cv_text)
        structured_data = {}
        for section_name, section_text in sections.items():
            structured_data[section_name] = self.generate_structured_data(section_text, section_name)
        return structured_data