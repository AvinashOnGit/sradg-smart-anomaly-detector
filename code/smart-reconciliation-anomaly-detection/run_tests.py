# Run BDD Test Cases
from behave import __main__

# Run all BDD test cases
def run_tests():
    feature_file = "features/anomaly_detection.feature"
    __main__.main([feature_file])

if __name__ == "__main__":
    run_tests()
