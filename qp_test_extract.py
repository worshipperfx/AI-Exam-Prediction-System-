import pdfplumber
import re
import os
import json

input_folder = r"C:\Users\Marvellous\Desktop\Exam Prediction Rephrasing\test_files_qp"
output_folder = r"C:\Users\Marvellous\Desktop\Exam Prediction Rephrasing\output_test_files_qp"
os.makedirs(output_folder, exist_ok=True)

num_pattern = re.compile(r'^(\d+)(?=\s|\(|$)')
letter_pattern = re.compile(r'^\(([a-zA-Z])\)')
roman_pattern = re.compile(r'^\(([ivxIVX]+)\)')
marks_pattern = re.compile(r'\[(\d+)\]')
junk_pattern = re.compile(r'(© UCLES|Turn over|Cambridge|Page \d+|^\*+|^\s*$|^\d{2}_0478|^\*{2,})')
dotted_line = re.compile(r'\.{5,}')

def extract_paper_code(filename):
    match = re.search(r'(0478).*?_qp_(\d{2})', filename)
    if match:
        return f"{match.group(1)}_{match.group(2)}"
    return "unknown_code"

def extract_questions(pdf_path, paper_code):
    with pdfplumber.open(pdf_path) as pdf:
        lines = []
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                for line in text.split('\n'):
                    line = line.strip()
                    line = dotted_line.sub('', line).strip()
                    if (
                        junk_pattern.search(line)
                        or line.startswith("_")
                        or not line
                    ):
                        continue
                    lines.append(line)

    questions = []
    current_question_id = ""
    current_text = []
    last_num = ""
    last_letter = ""
    last_roman = ""
    prev_question_id = ""
    pending_mark = None

    i = 0
    while i < len(lines):
        line = lines[i].strip()

        if re.match(r'^\d{3,} ', line):
            current_text.append(line)
            i += 1
            continue

        if num_pattern.match(line) and len(line.split()) < 4:
            i += 1
            continue

        if re.fullmatch(r'\[\d+\]', line):
            pending_mark = int(line.strip("[]"))
            i += 1
            if i < len(lines) and re.match(r'^\((?:[a-zA-Z]|[ivxIVX]+)\)', lines[i]):
                if current_question_id and current_text:
                    joined = " ".join(current_text).strip()
                    questions.append({
                        "paper_code": paper_code,
                        "question": current_question_id,
                        "text": joined,
                        "marks": pending_mark
                    })
                    current_text = []
                    pending_mark = None
                continue
            if current_question_id and current_text:
                joined = " ".join(current_text).strip()
                questions.append({
                    "paper_code": paper_code,
                    "question": current_question_id,
                    "text": joined,
                    "marks": pending_mark
                })
                current_text = []
                pending_mark = None
            continue

        num_match = num_pattern.match(line)
        letter_match = letter_pattern.match(line)
        roman_match = roman_pattern.match(line)
        started_new = False

        if num_match and len(line.split()) > 3:
            last_num = num_match.group(1)
            last_letter = ""
            last_roman = ""
            current_question_id = last_num
            started_new = True

        elif letter_match:
            last_letter = f"({letter_match.group(1)})"
            last_roman = ""
            if last_num:
                current_question_id = last_num + last_letter
                started_new = True

        elif roman_match:
            last_roman = f"({roman_match.group(1)})"
            if last_num and last_letter:
                current_question_id = last_num + last_letter + last_roman
                started_new = True
            elif last_num:
                current_question_id = last_num + last_roman
                started_new = True
            elif last_letter:
                current_question_id = last_letter + last_roman
                started_new = True
            else:
                current_question_id = last_roman
                started_new = True

        if started_new and current_text:
            joined = " ".join(current_text).strip()
            mark_inline = marks_pattern.search(joined)
            if mark_inline:
                mark = int(mark_inline.group().strip("[]"))
                clean_text = marks_pattern.sub("", joined).strip()
                questions.append({
                    "paper_code": paper_code,
                    "question": prev_question_id,
                    "text": clean_text,
                    "marks": mark
                })
                current_text = []
            else:
                current_text = []

        elif started_new and not current_text:
            current_text = [line]
            prev_question_id = current_question_id
            i += 1
            continue

        current_text.append(line)
        prev_question_id = current_question_id

        inline_mark = marks_pattern.search(line)
        if inline_mark:
            mark = int(inline_mark.group().strip("[]"))
            joined = " ".join(current_text).strip()
            clean_text = marks_pattern.sub("", joined).strip()
            questions.append({
                "paper_code": paper_code,
                "question": current_question_id,
                "text": clean_text,
                "marks": mark
            })
            current_text = []

        i += 1

    return questions

for filename in os.listdir(input_folder):
    if filename.lower().endswith(".pdf"):
        pdf_path = os.path.join(input_folder, filename)
        paper_code = extract_paper_code(filename)
        data = extract_questions(pdf_path, paper_code)
        output_path = os.path.join(output_folder, filename.replace(".pdf", ".json"))

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        print(f"Extracted {len(data)} questions → {output_path}")
