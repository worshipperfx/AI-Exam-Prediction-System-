import pandas as pd
import os

questions_df = pd.read_csv(r"C:\Users\Marvellous\Desktop\Exam Prediction Rephrasing\test_exam_questions_dataset.csv")
embeddings_df = pd.read_csv(r"C:\Users\Marvellous\Desktop\Exam Prediction Rephrasing\question_embeddings.csv")

merged_df = pd.merge(embeddings_df, questions_df, on=["paper_code", "question_id"], how="inner")

output_path = (r"C:\Users\Marvellous\Desktop\Exam Prediction Rephrasing\merged_qn_to_embeddings.csv")
os.makedirs(os.path.dirname(output_path), exist_ok=True)

merged_df.to_csv(output_path, index=False)

print("Merged datasets successfully")