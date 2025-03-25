from behave import given, when, then
import requests

@given("the system has identified anomalies")
def step_given_anomalies_identified(context):
    context.dashboard_url = "http://127.0.0.1:5000/"

@when("the user accesses the web dashboard")
def step_when_access_dashboard(context):
    context.response = requests.get(context.dashboard_url)

@then("they should see the anomalies displayed")
def step_then_verify_dashboard_display(context):
    assert context.response.status_code == 200
    assert "Anomaly Detection Report" in context.response.text
