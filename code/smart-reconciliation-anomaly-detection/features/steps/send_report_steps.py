from behave import given, when, then
from app.email_notification import send_email_with_attachment
import os

@given("anomalies have been detected")
def step_given_anomalies_detected(context):
    context.report_path = "anomaly_report.txt"
    with open(context.report_path, "w") as file:
        file.write("Sample anomaly report for testing.")

@when("the report generation function runs")
def step_when_send_report(context):
    context.email_result = send_email_with_attachment(
        subject="Anomaly Detection Report",
        body="Please find the attached anomaly detection report.",
        recipient_email="target_group@example.com",
        file_path=context.report_path
    )

@then("an email should be sent with the report attachment")
def step_then_verify_email_sent(context):
    assert context.email_result is True
    os.remove(context.report_path)  # Clean up after the test
