from bertopic import BERTopic
from sentence_transformers import SentenceTransformer
import pandas as pd

merged_df = pd.read_csv(r"C:\Users\Marvellous\Desktop\Exam Prediction Rephrasing\merged_qn_to_embeddings.csv")
texts = merged_df['text'].tolist()
vectors = merged_df.loc[:, merged_df.columns.str.isnumeric()].values

topic_model = BERTopic()
topics, probs = topic_model.fit_transform(texts, vectors)

merged_df['topic'] = topics
print(topic_model.get_topic_info())

topic_info_csv = topic_model.get_topic_info()
topic_info_csv.to_csv(r"C:\Users\Marvellous\Desktop\Exam Prediction Rephrasing\topic_only.csv", index=False)
merged_df.to_csv(r"C:\Users\Marvellous\Desktop\Exam Prediction Rephrasing\merged_with_topics.csv", index=False)


print("Saved both topic CSV files")
