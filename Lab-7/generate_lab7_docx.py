"""
generate_lab7_docx.py
Generates a clean, minimal, human-written Lab 7 report:
- PES1UG25CS846_Siddu_Shirasagi_LAB7.docx
- SRN_NAME_LAB7.docx
"""

import os
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), fill_hex)
    tcPr.append(shd)

def set_cell_margins(cell, top=80, bottom=80, left=100, right=100):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def build_docx():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    screenshots_dir = os.path.join(base_dir, "screenshots")
    docx_paths = [
        os.path.join(base_dir, "PES1UG25CS846_Siddu_Shirasagi_LAB7.docx"),
        os.path.join(base_dir, "SRN_NAME_LAB7.docx")
    ]

    for docx_path in docx_paths:
        doc = Document()

        for section in doc.sections:
            section.top_margin = Inches(0.7)
            section.bottom_margin = Inches(0.7)
            section.left_margin = Inches(0.7)
            section.right_margin = Inches(0.7)

        # Header Title
        title_p = doc.add_paragraph()
        title_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run_title = title_p.add_run("PES UNIVERSITY")
        run_title.font.name = "Arial"
        run_title.font.size = Pt(16)
        run_title.font.bold = True
        run_title.font.color.rgb = RGBColor(17, 24, 39)

        dept_p = doc.add_paragraph()
        dept_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run_dept = dept_p.add_run("Department of Computer Science and Engineering\nSoftware Engineering Lab (UE23CS352A)\nLab 7: Fuzzing for Input Validation Bugs")
        run_dept.font.name = "Arial"
        run_dept.font.size = Pt(10.5)
        run_dept.font.color.rgb = RGBColor(75, 85, 99)

        # Student Details Table
        table = doc.add_table(rows=2, cols=2)
        table.alignment = WD_TABLE_ALIGNMENT.CENTER

        cells0 = table.rows[0].cells
        p0 = cells0[0].paragraphs[0]
        r = p0.add_run("Name: ")
        r.bold = True
        p0.add_run("Siddu Sanganna Shirasagi")

        p1 = cells0[1].paragraphs[0]
        r = p1.add_run("SRN: ")
        r.bold = True
        p1.add_run("PES1UG25CS846")

        cells1 = table.rows[1].cells
        p2 = cells1[0].paragraphs[0]
        r = p2.add_run("Problem / Roll: ")
        r.bold = True
        p2.add_run("61 (Credit Card Rewards)")

        p3 = cells1[1].paragraphs[0]
        r = p3.add_run("Repo: ")
        r.bold = True
        p3.add_run("sidducs/se-labs (Lab-7)")

        for row in table.rows:
            for cell in row.cells:
                set_cell_background(cell, "F3F4F6")
                set_cell_margins(cell, top=60, bottom=60, left=80, right=80)

        doc.add_paragraph()

        # Objective
        h1 = doc.add_heading(level=2)
        r = h1.add_run("Objective")
        r.font.name = "Arial"
        r.font.size = Pt(12)
        r.font.bold = True
        r.font.color.rgb = RGBColor(31, 41, 55)

        p = doc.add_paragraph()
        p.add_run("Use the Hypothesis library to perform property-based fuzz testing on credit_card_rewards_parser.py, identify input validation crashes, and harden the code using defensive programming.")

        # Screenshots
        h2 = doc.add_heading(level=2)
        r = h2.add_run("Execution Screenshots")
        r.font.name = "Arial"
        r.font.size = Pt(12)
        r.font.bold = True
        r.font.color.rgb = RGBColor(31, 41, 55)

        ss_list = [
            ("SS1: Running credit_card_rewards_parser.py (Buggy Module)", "SS1.png"),
            ("SS2: Running pytest test_credit_card_rewards_parser.py (Failing on Buggy Module)", "SS2.png"),
            ("SS3: Running credit_card_rewards_parser.py (Fixed Module)", "SS3.png"),
            ("SS4: Running pytest test_credit_card_rewards_parser.py (All Tests Passing)", "SS4.png")
        ]

        for label, fname in ss_list:
            lp = doc.add_paragraph()
            lrun = lp.add_run(label)
            lrun.bold = True
            lrun.font.size = Pt(10)
            lrun.font.color.rgb = RGBColor(17, 24, 39)

            img_path = os.path.join(screenshots_dir, fname)
            if os.path.exists(img_path):
                ip = doc.add_paragraph()
                ip.alignment = WD_ALIGN_PARAGRAPH.CENTER
                ip.add_run().add_picture(img_path, width=Inches(6.0))
            doc.add_paragraph()

        # Bug Analysis Table
        h3 = doc.add_heading(level=2)
        r = h3.add_run("Bugs Discovered by Hypothesis")
        r.font.name = "Arial"
        r.font.size = Pt(12)
        r.font.bold = True
        r.font.color.rgb = RGBColor(31, 41, 55)

        bug_table = doc.add_table(rows=4, cols=4)
        bug_table.alignment = WD_TABLE_ALIGNMENT.CENTER
        headers = ["Function", "Assumed Input", "Failing Input Found", "Error / Exception"]
        for i, h in enumerate(headers):
            cell = bug_table.rows[0].cells[i]
            cp = cell.paragraphs[0]
            cr = cp.add_run(h)
            cr.bold = True
            cr.font.size = Pt(9)
            set_cell_background(cell, "E5E7EB")

        table_data = [
            ("mask_card_number", "Always a string with card digits", "s = None", "AttributeError: 'NoneType' has no attribute 'replace'"),
            ("parse_transaction", "Always 'date,category,amount' with int amount", "s = None\ns = ''\ns = 'date,cat,abc'", "AttributeError (on None)\nIndexError: list index out of range (on '')\nValueError: invalid literal for int()"),
            ("parse_statement_total", "Always contains ':' followed by integer", "s = None\ns = ''\ns = ':'", "AttributeError (on None)\nIndexError: list index out of range\nValueError: invalid literal for int()")
        ]

        for r_idx, row_vals in enumerate(table_data, start=1):
            for c_idx, val in enumerate(row_vals):
                cell = bug_table.rows[r_idx].cells[c_idx]
                cp = cell.paragraphs[0]
                cr = cp.add_run(val)
                cr.font.size = Pt(8.5)
                set_cell_background(cell, "F9FAFB" if r_idx % 2 == 1 else "FFFFFF")

        for row in bug_table.rows:
            for cell in row.cells:
                set_cell_margins(cell, top=50, bottom=50, left=70, right=70)

        doc.add_paragraph()

        # Reflection Questions
        h4 = doc.add_heading(level=2)
        r = h4.add_run("Reflection Questions")
        r.font.name = "Arial"
        r.font.size = Pt(12)
        r.font.bold = True
        r.font.color.rgb = RGBColor(31, 41, 55)

        reflections = [
            (
                "1. What types of bugs does fuzz testing reveal that traditional unit testing usually misses?",
                "Traditional unit tests only check inputs the developer thought of beforehand (the happy path and a few expected edge cases). Fuzz testing generates hundreds of unexpected, malformed, and boundary inputs automatically (such as None, empty strings, missing separators, and bad data types). This easily reveals unhandled crashes like AttributeError, IndexError, and ValueError that manual tests tend to miss."
            ),
            (
                "2. What edge cases and malformed inputs did Hypothesis uncover in each of the three functions?",
                "• mask_card_number: Failed on s = None, causing an AttributeError because NoneType does not have a .replace() method.\n"
                "• parse_transaction: Failed on s = None (AttributeError on split), empty string s = '' (IndexError because parts has only 1 element), and non-integer amounts like 'abc' (ValueError on int()).\n"
                "• parse_statement_total: Failed on s = None (AttributeError), empty string or lines without a colon (IndexError on text.split(':')[1]), and strings like ':' with no number after the colon (ValueError)."
            ),
            (
                "3. How did you harden the functions against invalid inputs, and what are the trade-offs between defensive parsing vs crashing?",
                "I hardened the functions by adding isinstance(..., str) checks, checking list length and delimiter existence before indexing, and wrapping int() conversion in try-except blocks, returning None or '' when input is invalid.\n\n"
                "Trade-offs: Defensive parsing prevents unexpected crashes and keeps the service running even when users provide garbage input. However, returning fallback defaults like None can sometimes hide upstream bugs if the caller forgets to check the result. Raising exceptions makes bugs immediately obvious, but requires callers to add try-except blocks everywhere to prevent the program from crashing."
            )
        ]

        for q_text, a_text in reflections:
            qp = doc.add_paragraph()
            qrun = qp.add_run(q_text)
            qrun.bold = True
            qrun.font.size = Pt(10)
            qrun.font.color.rgb = RGBColor(17, 24, 39)

            ap = doc.add_paragraph()
            arun = ap.add_run(a_text)
            arun.font.size = Pt(9.5)
            arun.font.color.rgb = RGBColor(55, 65, 81)

        try:
            doc.save(docx_path)
            print(f"Generated: {docx_path}")
        except PermissionError:
            print(f"File locked by another process (e.g. Word): {docx_path}")

if __name__ == "__main__":
    build_docx()
