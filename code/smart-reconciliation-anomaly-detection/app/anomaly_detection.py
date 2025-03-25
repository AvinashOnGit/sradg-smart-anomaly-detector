from sklearn.ensemble import IsolationForest
import pandas as pd
from transformers import AutoModelForCausalLM, AutoTokenizer, T5Tokenizer, T5ForConditionalGeneration
import torch

model_name = "google/flan-t5-small"
tokenizer = T5Tokenizer.from_pretrained(model_name)
model = T5ForConditionalGeneration.from_pretrained(model_name)

# Updated function to generate anomaly explanations using GPT-J

def generate_anomaly_explanation(anomaly_data):
    # Extract relevant fields for explanation
    relevant_data = {
        "TransactionAmount": anomaly_data['TransactionAmount'],
        "TransactionType": anomaly_data['TransactionType'],
        "Channel": anomaly_data['Channel'],
        "Location": anomaly_data['Location'],
        "CustomerAge": anomaly_data['CustomerAge'],
        "TransactionDuration": anomaly_data['TransactionDuration'],
        "LoginAttempts": anomaly_data['LoginAttempts'],
    }

    # Simplified and focused prompt
    prompt = (
        f"Explain why the following transaction is considered an anomaly:\n"
        f"Amount: {relevant_data['TransactionAmount']}, "
        f"Type: {relevant_data['TransactionType']}, "
        f"Channel: {relevant_data['Channel']}, "
        f"Location: {relevant_data['Location']}, "
        f"Age: {relevant_data['CustomerAge']}, "
        f"Duration: {relevant_data['TransactionDuration']} seconds, "
        f"Login Attempts: {relevant_data['LoginAttempts']}."
    )

    # Encode the prompt for flan-t5
    inputs = tokenizer(
        prompt,
        return_tensors="pt",
        padding=True,
        truncation=True,
        max_length=512
    )

    # Generate explanation with a short length and beam search
    outputs = model.generate(
        inputs["input_ids"],
        max_length=50,  # Ensure a concise response
        num_return_sequences=1,
        num_beams=3,  # Beam search for better results
        early_stopping=True
    )

    # Decode and format the output
    explanation = tokenizer.decode(outputs[0], skip_special_tokens=True).strip()

    # Handle cases where no valid explanation is generated
    if not explanation or explanation == prompt.strip():
        return "No meaningful explanation generated. Check the model or prompt."

    return explanation

# Updated anomaly detection function
def detect_anomalies(df):
    # Encode categorical columns
    df['TransactionType'] = pd.Categorical(df['TransactionType']).codes
    df['Channel'] = pd.Categorical(df['Channel']).codes
    df['Location'] = pd.Categorical(df['Location']).codes

    # Features for anomaly detection
    X = df[['TransactionAmount', 'TransactionType', 'Channel', 'Location', 'TransactionDuration', 'LoginAttempts']].values

    # Isolation Forest model
    model = IsolationForest(contamination=0.05, random_state=42)
    model.fit(X)

    # Predict anomalies: -1 means anomaly, 1 means normal
    df['Anomaly'] = model.predict(X)
    df['Anomaly'] = df['Anomaly'].apply(lambda x: 'Anomaly' if x == -1 else 'Normal')
    df['Explanation'] = ''
    count=0
    for idx, row in df[df['Anomaly'] == 'Anomaly'].iterrows():
        anomaly_data = row.to_dict()
        count+=1
        explanation = generate_anomaly_explanation(anomaly_data)
        df.loc[idx, 'Explanation'] = explanation
        print('Count : {} , LLM explanation : {}'.format(str(count),explanation))


    return df
