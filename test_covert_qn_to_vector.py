import pandas as pd
from sentence_transformers import SentenceTransformer
import os 

csv_path = r"C:\Users\Marvellous\Desktop\Exam Prediction Rephrasing\test_exam_questions_dataset.csv"
df = pd.read_csv(csv_path)

# Transfomer Model
model = SentenceTransformer('all-MiniLM-L6-v2')

embeddings = model.encode(df['text'].tolist(), show_progress_bar=True)

embeddings_df = pd.DataFrame(embeddings)
embeddings_df["paper_code"] = df["paper_code"]
embeddings_df["question_id"] = df["question_id"]

os.makedirs(os.path.dirname(csv_path), exist_ok=True)
output_path = r'C:\Users\Marvellous\Desktop\Exam Prediction Rephrasing\question_embeddings.csv'
embeddings_df.to_csv(output_path, index =False)