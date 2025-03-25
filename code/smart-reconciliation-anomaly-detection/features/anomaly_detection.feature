# BDD Test Cases using Behave
Feature: Anomaly Detection and Reporting System

  Scenario: Load and preprocess transaction data
    Given a transaction dataset is available
    When the system loads the dataset
    Then it should successfully preprocess the data

  Scenario: Generate real-time transactions
    Given the system needs to generate real-time transactions
    When the data generation function runs
    Then it should create a CSV file with synthetic transactions

  Scenario: Detect anomalies in transactions
    Given a preprocessed dataset
    When the anomaly detection model runs
    Then it should identify anomalies and assign labels

  Scenario: Generate explanations for detected anomalies
    Given an anomaly is detected
    When the system generates an explanation
    Then it should provide a meaningful anomaly reason

  Scenario: Display detected anomalies in the dashboard
    Given the system has identified anomalies
    When the user accesses the web dashboard
    Then they should see the anomalies displayed

  Scenario: Send an anomaly report via email
    Given anomalies have been detected
    When the report generation function runs
    Then an email should be sent with the report attachment

