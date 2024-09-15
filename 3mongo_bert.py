import pandas as pd
from pymongo import MongoClient
from transformers import AutoModelForSequenceClassification, AutoTokenizer
import re

# USE GOOGLE COLAB INSTEAD!!!

access_token = ("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")
chunk_size = 100

# Connect to MongoDB
client = MongoClient("mongodb+srv://starvevader:Aw255423@cluster0.lcwom3q.mongodb.net/?retryWrites=true&w=majority")
db = client["heatmap"]
collection = db["wsb_spacy"]

# Retrieve all documents from MongoDB collection
data = list(collection.find({}))
df = pd.DataFrame(data)

# Regular expression pattern for matching URLs
url_pattern = re.compile(r"https?://\S+")

# initialize finBERT model and tokenizer
model = AutoModelForSequenceClassification.from_pretrained("FourthBrain/bert_model_reddit_tsla", use_auth_token=access_token)
tokenizer = AutoTokenizer.from_pretrained("FourthBrain/bert_model_reddit_tsla")


# function to perform sentiment analysis and return sentiment score
def sentiment_analysis(title, post_body):
    text = title + " " + post_body
    text = text[:300] # truncate the input text to 512 tokens
    input_ids = tokenizer.encode(text, return_tensors="pt")
    sentiment_logits = model(input_ids)[0][0]
    positive_score = sentiment_logits[1]
    negative_score = sentiment_logits[0]
    return positive_score, negative_score

# process the data in smaller chunks

for i in range(0, len(df), chunk_size):
    df_chunk = df.iloc[i:i+chunk_size]
    df_chunk['title'].fillna("", inplace=True)
    df_chunk['post body'].fillna("", inplace=True)
    positive_scores, negative_scores = [], []
    for index, row in df_chunk.iterrows():
        positive, negative = sentiment_analysis(row["title"], row["post body"])
        positive_scores.append(positive.detach().numpy())
        negative_scores.append(negative.detach().numpy())
    df_chunk["Positive_Score"] = positive_scores
    df_chunk["Negative_Score"] = negative_scores
    for index, row in df_chunk.iterrows():
        collection.update_one({'_id': row['_id']}, {'$set': {'Positive_Score': row['Positive_Score'], 'Negative_Score': row['Negative_Score']}})
print ("export complete")
