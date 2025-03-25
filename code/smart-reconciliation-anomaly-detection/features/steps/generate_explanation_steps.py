from behave import given, when, then
from app.anomaly_detection import generate_anomaly_explanation

@given("an anomaly is detected")
def step_given_anomaly_detected(context):
    context.anomaly_data = {
        "TransactionAmount": 1200,
        "TransactionType": 1,
        "Channel": 2,
        "Location": 45,
        "CustomerAge": 60,
        "TransactionDuration": 300,
        "LoginAttempts": 5
    }

@when("the system generates an explanation")
def step_when_generate_explanation(context):
    context.explanation = generate_anomaly_explanation(context.anomaly_data)

@then("it should provide a meaningful anomaly reason")
def step_then_verify_explanation(context):
    assert isinstance(context.explanation, str)
    assert len(context.explanation) > 0
