from behave import given, when, then
import pandas as pd
from app.data_processing import load_and_preprocess_data

@given("a transaction dataset is available")
def step_given_dataset(context):
    context.dataset_path = "data/bank_transactions_data_2.csv"

@when("the system loads the dataset")
def step_when_load_dataset(context):
    context.df = load_and_preprocess_data(context.dataset_path)

@then("it should successfully preprocess the data")
def step_then_verify_preprocessing(context):
    assert not context.df.empty
    assert context.df.isnull().sum().sum() == 0
