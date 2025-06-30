import os
import json
import pandas as pd
import re

input_folder = r"C:\Users\Marvellous\Desktop\Exam Prediction Rephrasing\output_test_files_qp"
output_csv_path = r"C:\Users\Marvellous\Desktop\Exam Prediction Rephrasing\test_exam_questions_dataset.csv"
os.makedirs(os.path.dirname(output_csv_path), exist_ok=True)

# Extract paper code from filename
def get_paper_code(filename):
    match = re.search(r'(\d{4})_.*_(\d{2})', filename)
    if match:
        return f"{match.group(1)}_{match.group(2)}"
    else:
        match = re.search(r'(\d{4})_.*_(\d{2})', filename.replace("qp", ""))
        return match.group(0) if match else "unknown"

all_data = []

for file in os.listdir(input_folder):
    if file.endswith(".json"):
        paper_code = get_paper_code(file)
        filepath = os.path.join(input_folder, file)

        with open(filepath, "r", encoding="utf-8") as f:
            try:
                questions = json.load(f)
            except json.JSONDecodeError:
                print(f"Skipped: {file} - invalid JSON")
                continue

        for q in questions:
            all_data.append({
                "paper_code": paper_code,
                "question_id": q.get("question", ""),
                "text": q.get("text", "").strip(),
                "marks": q.get("marks", None)
            })


df = pd.DataFrame(all_data)
print(df)
df.to_csv(output_csv_path, index=False, encoding="utf-8-sig")
print(f"Dataset created: {output_csv_path} with {len(df)} questions.")
