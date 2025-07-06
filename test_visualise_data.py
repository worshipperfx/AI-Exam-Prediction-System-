import pandas as pd
import matplotlib.pyplot as plt


df = pd.read_csv("C:/Users/Marvellous/Desktop/Exam Prediction Rephrasing/topic_only.csv")

if 'Topic' not in df.columns:
    raise Exception("Run BERTopic first to generate 'topic' column.")

topic_counts = df['Topic'].value_counts().sort_index()

plt.figure(figsize=(10, 6))
topic_counts.plot(kind='bar', color='skyblue', edgecolor='black')
plt.title("Number of Questions per Topic")
plt.xlabel("Topic Number")
plt.ylabel("Question Count")
plt.xticks(rotation=0)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()
