from datetime import timedelta

import pandas as pd
from faker import Faker
import random

from sklearn.preprocessing import StandardScaler

fake = Faker()

# Load sample data from provided CSV
def load_sample_data(file_path):
    df = load_and_preprocess_data(file_path)
    return df


# Generate real-time simulated data matching the schema of bank_transactions_data_2.csv
def generate_real_time_data(num_records=100):
    fake = Faker()
    data = []
    for _ in range(num_records):
        record = {
            "TransactionID": fake.uuid4(),
            "AccountID": f"AC{random.randint(10000, 99999)}",
            "TransactionAmount": round(random.uniform(10.0, 1000.0), 2),
            "TransactionDate": str(fake.date_time_this_decade()),
            "TransactionType": random.choice(['Debit', 'Credit']),
            "Location": random.choice(['San Diego', 'Houston', 'Mesa', 'Raleigh', 'Atlanta']),
            "DeviceID": f"D{random.randint(100, 999)}",
            "IP Address": fake.ipv4(),
            "MerchantID": f"M{random.randint(1, 100)}",
            "Channel": random.choice(['ATM', 'Online']),
            "CustomerAge": random.randint(18, 75),
            "CustomerOccupation": random.choice(['Doctor', 'Engineer', 'Student', 'Lawyer']),
            "TransactionDuration": random.randint(10, 200),
            "LoginAttempts": random.randint(1, 5),
            "AccountBalance": round(random.uniform(500.0, 15000.0), 2),
            "PreviousTransactionDate": str(fake.date_time_this_year()),
        }
        data.append(record)

    df_real_time = pd.DataFrame(data)
    df_real_time.to_csv('data/real_time_data.csv', index=False)
    return df_real_time

# Function to generate synthetic transaction data
def generate_synthetic_data(output_path, num_records=1000):
    data = []
    transaction_types = ["Purchase", "Withdrawal", "Transfer", "Deposit"]
    channels = ["Online", "ATM", "Mobile", "Branch"]

    for _ in range(num_records):
        transaction_date = fake.date_time_between(start_date="-1y", end_date="now")
        previous_transaction_date = transaction_date - timedelta(days=random.randint(1, 60))

        record = {
            "TransactionID": fake.uuid4(),
            "AccountID": fake.uuid4(),
            "TransactionAmount": round(random.uniform(10, 1000), 2),
            "TransactionDate": transaction_date.strftime("%Y-%m-%d %H:%M:%S"),
            "TransactionType": random.choice(range(len(transaction_types))),
            "Location": random.randint(0, 50),
            "DeviceID": fake.uuid4(),
            "IP Address": fake.ipv4(),
            "MerchantID": f"M{random.randint(1, 1000):03d}",
            "Channel": random.choice(range(len(channels))),
            "CustomerAge": random.randint(18, 70),
            "CustomerOccupation": fake.job(),
            "TransactionDuration": random.randint(10, 600),
            "LoginAttempts": random.randint(1, 5),
            "AccountBalance": round(random.uniform(1000, 10000), 2),
            "PreviousTransactionDate": previous_transaction_date.strftime("%Y-%m-%d %H:%M:%S"),
        }
        data.append(record)

    # Convert to DataFrame and save as CSV
    df = pd.DataFrame(data)
    df.to_csv(output_path, index=False)
    print(f"Synthetic transaction data generated and saved to {output_path}")

def load_and_preprocess_data(dataset_path):
    # Load the dataset into a DataFrame
    df = pd.read_csv(dataset_path)

    # Drop unnecessary or sensitive columns if they exist
    columns_to_drop = ["TransactionID", "AccountID", "DeviceID", "IP Address", "MerchantID"]
    for col in columns_to_drop:
        if col in df.columns:
            df.drop(columns=[col], inplace=True)

    # Convert categorical columns to numerical representations
    categorical_cols = ["TransactionType", "Channel", "Location", "CustomerOccupation"]
    for col in categorical_cols:
        if col in df.columns:
            df[col] = pd.Categorical(df[col]).codes

    # Handle missing or null values if any
    df.fillna(0, inplace=True)

    # Normalize numeric columns using StandardScaler
    scaler = StandardScaler()
    numeric_cols = ["TransactionAmount", "TransactionDuration", "LoginAttempts", "AccountBalance"]
    df[numeric_cols] = scaler.fit_transform(df[numeric_cols])

    print("Data successfully loaded and preprocessed.")
    return df
