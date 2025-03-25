from behave import given, when, then
from app.anomaly_detection import detect_anomalies

@given("a preprocessed dataset")
def step_given_preprocessed_dataset(context):
    context.dataset_path = "data/bank_transactions_data_2.csv"
    context.df = pd.read_csv(context.dataset_path)

@when("the anomaly detection model runs")
def step_when_run_anomaly_model(context):
    context.df_anomalies = detect_anomalies(context.df)

@then("it should identify anomalies and assign labels")
def step_then_verify_anomaly_detection(context):
    assert "Anomaly" in context.df_anomalies.columns
    assert set(context.df_anomalies["Anomaly"].unique()) == {"Anomaly", "Normal"}
