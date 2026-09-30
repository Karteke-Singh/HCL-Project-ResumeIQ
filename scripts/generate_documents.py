"""
Generates realistic PDF and DOCX resume documents for all 15 synthetic candidates in Project P_101.
Outputs:
- data/sample/resumes/docx/C001.docx to C015.docx
- data/sample/resumes/pdf/C001.pdf to C015.pdf
"""

import json
from pathlib import Path
import docx
from docx.shared import Inches, Pt, RGBColor
from fpdf import FPDF
from fpdf.enums import XPos, YPos

BASE_DIR = Path(__file__).resolve().parent.parent
SAMPLE_DIR = BASE_DIR / "data" / "sample"
RESUMES_JSON_PATH = SAMPLE_DIR / "resumes.json"

DOCX_DIR = SAMPLE_DIR / "resumes" / "docx"
PDF_DIR = SAMPLE_DIR / "resumes" / "pdf"

DOCX_DIR.mkdir(parents=True, exist_ok=True)
PDF_DIR.mkdir(parents=True, exist_ok=True)


def create_docx_resume(candidate: dict, output_path: Path):
    doc = docx.Document()

    # Margins
    for section in doc.sections:
        section.top_margin = Inches(0.7)
        section.bottom_margin = Inches(0.7)
        section.left_margin = Inches(0.8)
        section.right_margin = Inches(0.8)

    cid = candidate["candidate_id"]
    name = candidate["name"]
    email = f"candidate.{cid.lower()}@synthetic-dataset.local"

    # Header
    header = doc.add_paragraph()
    run_name = header.add_run(f"{name} ({cid})")
    run_name.bold = True
    run_name.font.size = Pt(17)
    run_name.font.color.rgb = RGBColor(30, 41, 59)

    contact_p = doc.add_paragraph()
    run_contact = contact_p.add_run(f"Email: {email} | Location: Synthetic Region | Confidential Portfolio")
    run_contact.font.size = Pt(9.5)
    run_contact.font.italic = True
    run_contact.font.color.rgb = RGBColor(100, 116, 139)

    def add_section_header(title: str):
        p = doc.add_paragraph()
        run = p.add_run(title.upper())
        run.bold = True
        run.font.size = Pt(11.5)
        run.font.color.rgb = RGBColor(15, 23, 42)
        p.paragraph_format.space_before = Pt(8)
        p.paragraph_format.space_after = Pt(2)

    # 1. Professional Summary
    add_section_header("Professional Summary")
    p_summary = doc.add_paragraph(candidate["professional_summary"])
    p_summary.paragraph_format.space_after = Pt(6)

    # 2. Technical Skills
    add_section_header("Technical Skills")
    p_skills = doc.add_paragraph()
    run_skills = p_skills.add_run(", ".join(candidate["skills"]))
    run_skills.font.size = Pt(10)
    p_skills.paragraph_format.space_after = Pt(6)

    # 3. Professional Experience
    add_section_header("Professional Experience")
    work = candidate.get("work_experience", [])
    if not work:
        p_none = doc.add_paragraph("Entry-Level / Capstone Projects Only (0.0 Professional Experience Years)")
        p_none.paragraph_format.space_after = Pt(4)
    else:
        for item in work:
            p_job = doc.add_paragraph()
            r_title = p_job.add_run(f"{item['title']} - {item['company']}")
            r_title.bold = True
            r_title.font.size = Pt(10.5)

            p_dur = doc.add_paragraph()
            r_dur = p_dur.add_run(f"Duration: {item['duration']}")
            r_dur.font.italic = True
            r_dur.font.size = Pt(9.5)
            r_dur.font.color.rgb = RGBColor(100, 116, 139)

            for resp in item.get("responsibilities", []):
                p_bullet = doc.add_paragraph(resp, style="List Bullet")
                p_bullet.paragraph_format.space_after = Pt(1)

    p_tot = doc.add_paragraph(f"Total Professional Experience: {candidate['experience_years']} years")
    p_tot.paragraph_format.space_before = Pt(4)
    p_tot.paragraph_format.space_after = Pt(6)

    # 4. Technical Projects
    add_section_header("Key Technical Projects")
    for proj in candidate.get("projects", []):
        p_pname = doc.add_paragraph()
        r_pname = p_pname.add_run(proj["name"])
        r_pname.bold = True
        r_pname.font.size = Pt(10)

        p_pdesc = doc.add_paragraph(proj.get("description", ""))
        p_pdesc.paragraph_format.space_after = Pt(1)

        p_ptech = doc.add_paragraph()
        r_ptech = p_ptech.add_run(f"Technologies Used: {', '.join(proj.get('technologies', []))}")
        r_ptech.font.size = Pt(9)
        r_ptech.font.italic = True
        p_ptech.paragraph_format.space_after = Pt(4)

    # 5. Education
    add_section_header("Education")
    edu = candidate["education"]
    p_edu = doc.add_paragraph(f"{edu['degree']} in {edu['field_of_study']}")
    p_edu.runs[0].bold = True
    p_inst = doc.add_paragraph(f"{edu['institution']} | Graduation Year: {edu['graduation_year']}")
    p_inst.paragraph_format.space_after = Pt(6)

    # 6. Certifications
    add_section_header("Certifications")
    certs = candidate.get("certifications", [])
    if certs:
        for cert in certs:
            doc.add_paragraph(cert, style="List Bullet")
    else:
        doc.add_paragraph("None")

    doc.save(str(output_path))


class ResumePDF(FPDF):
    def header(self):
        pass

    def footer(self):
        self.set_y(-12)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(150, 150, 150)
        self.cell(self.epw, 8, f"Page {self.page_no()}", align="C")


def create_pdf_resume(candidate: dict, output_path: Path):
    pdf = ResumePDF(orientation="P", unit="mm", format="A4")
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_margins(16, 16, 16)

    cid = candidate["candidate_id"]
    name = candidate["name"]
    email = f"candidate.{cid.lower()}@synthetic-dataset.local"

    # Header
    pdf.set_font("Helvetica", "B", 15)
    pdf.set_text_color(30, 41, 59)
    pdf.cell(pdf.epw, 7, f"{name} ({cid})", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    pdf.set_font("Helvetica", "I", 9)
    pdf.set_text_color(100, 116, 139)
    pdf.cell(pdf.epw, 5, f"Email: {email} | Region: Synthetic Evaluation Set", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(2)

    def print_section_title(title: str):
        pdf.set_font("Helvetica", "B", 10.5)
        pdf.set_text_color(15, 23, 42)
        pdf.set_fill_color(240, 244, 248)
        pdf.cell(pdf.epw, 6, f"  {title.upper()}", fill=True, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.ln(1.5)

    # 1. Professional Summary
    print_section_title("Professional Summary")
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(51, 65, 85)
    pdf.multi_cell(pdf.epw, 4.5, candidate["professional_summary"])
    pdf.ln(2.5)

    # 2. Technical Skills
    print_section_title("Technical Skills")
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(51, 65, 85)
    pdf.multi_cell(pdf.epw, 4.5, ", ".join(candidate["skills"]))
    pdf.ln(2.5)

    # 3. Professional Experience
    print_section_title("Professional Experience")
    work = candidate.get("work_experience", [])
    if not work:
        pdf.set_font("Helvetica", "I", 9)
        pdf.set_text_color(100, 116, 139)
        pdf.multi_cell(pdf.epw, 4.5, "Entry-Level / Capstone Projects Only (0.0 formal years in industry)")
        pdf.ln(2)
    else:
        for item in work:
            pdf.set_font("Helvetica", "B", 9)
            pdf.set_text_color(30, 41, 59)
            pdf.cell(pdf.epw, 4.5, f"{item['title']} - {item['company']}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

            pdf.set_font("Helvetica", "I", 8)
            pdf.set_text_color(100, 116, 139)
            pdf.cell(pdf.epw, 4.0, f"Duration: {item['duration']}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

            pdf.set_font("Helvetica", "", 8.5)
            pdf.set_text_color(51, 65, 85)
            for resp in item.get("responsibilities", []):
                pdf.multi_cell(pdf.epw, 4.0, f"- {resp}")
            pdf.ln(1.5)

    pdf.set_font("Helvetica", "B", 8.5)
    pdf.set_text_color(30, 41, 59)
    pdf.cell(pdf.epw, 4.5, f"Total Professional Experience: {candidate['experience_years']} years", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(2)

    # 4. Technical Projects
    print_section_title("Technical Projects")
    for proj in candidate.get("projects", []):
        pdf.set_font("Helvetica", "B", 9)
        pdf.set_text_color(30, 41, 59)
        pdf.cell(pdf.epw, 4.5, proj["name"], new_x=XPos.LMARGIN, new_y=YPos.NEXT)

        pdf.set_font("Helvetica", "", 8.5)
        pdf.set_text_color(51, 65, 85)
        pdf.multi_cell(pdf.epw, 4.0, proj.get("description", ""))

        pdf.set_font("Helvetica", "I", 8)
        pdf.set_text_color(100, 116, 139)
        pdf.cell(pdf.epw, 4.0, f"Technologies: {', '.join(proj.get('technologies', []))}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.ln(1.5)

    # 5. Education
    print_section_title("Education")
    edu = candidate["education"]
    pdf.set_font("Helvetica", "B", 9)
    pdf.set_text_color(30, 41, 59)
    pdf.cell(pdf.epw, 4.5, f"{edu['degree']} in {edu['field_of_study']}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    pdf.set_font("Helvetica", "", 8.5)
    pdf.set_text_color(51, 65, 85)
    pdf.cell(pdf.epw, 4.0, f"{edu['institution']} | Graduation Year: {edu['graduation_year']}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(2)

    # 6. Certifications
    print_section_title("Certifications")
    certs = candidate.get("certifications", [])
    pdf.set_font("Helvetica", "", 8.5)
    pdf.set_text_color(51, 65, 85)
    if certs:
        for cert in certs:
            pdf.cell(pdf.epw, 4.0, f"- {cert}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    else:
        pdf.cell(pdf.epw, 4.0, "None", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    pdf.output(str(output_path))


def main():
    with open(RESUMES_JSON_PATH, "r", encoding="utf-8") as f:
        candidates = json.load(f)

    print(f"Loaded {len(candidates)} candidates from {RESUMES_JSON_PATH}")
    for candidate in candidates:
        cid = candidate["candidate_id"]
        docx_file = DOCX_DIR / f"{cid}.docx"
        pdf_file = PDF_DIR / f"{cid}.pdf"

        create_docx_resume(candidate, docx_file)
        create_pdf_resume(candidate, pdf_file)
        print(f"  [OK] Generated {cid}.docx and {cid}.pdf")

    print(f"\n[SUCCESS] Successfully generated {len(candidates)} DOCX and {len(candidates)} PDF resumes.")


if __name__ == "__main__":
    main()
