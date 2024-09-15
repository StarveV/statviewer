import pandas as pd
from transformers import AutoModelForSequenceClassification, AutoTokenizer
import re
access_token =  ("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")

chunk_size = 100

# load the data from .xlsx file
df = pd.read_csv("/content/spacy_change23.csv")
processed_chunks = []

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
    positive_scores, neutral_scores, negative_scores = [], [], []
    for index, row in df_chunk.iterrows():
        positive, negative = sentiment_analysis(row["title"], row["post body"])
        positive_scores.append(positive.detach().numpy())
        negative_scores.append(negative.detach().numpy())
    df_chunk["Positive_Score"] = positive_scores
    df_chunk["Negative_Score"] = negative_scores
    processed_chunks.append(df_chunk)

# concatenate the processed chunks into a single dataframe
df = pd.concat(processed_chunks)

# export the results to a new .xlsx file
df.to_csv("finbert13.csv", index=False)
print ("export complete")
