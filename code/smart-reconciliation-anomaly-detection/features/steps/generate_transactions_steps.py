from behave import given, when, then
from app.data_processing import generate_synthetic_data
import os

@given("the system needs to generate real-time transactions")
def step_given_generate_data(context):
    context.output_path = "data/generated_transactions.csv"

@when("the data generation function runs")
def step_when_generate_data(context):
    generate_synthetic_data(context.output_path)

@then("it should create a CSV file with synthetic transactions")
def step_then_verify_csv_creation(context):
    assert os.path.exists(context.output_path)
    os.remove(context.output_path)  # Clean up after the test
