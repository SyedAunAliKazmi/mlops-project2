import mlflow
import mlflow.sklearn
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import sys

MLFLOW_URI = "http://localhost:5000"
THRESHOLD = 0.99

def test_model(model_uri):
    mlflow.set_tracking_uri(MLFLOW_URI)
    print(f"[TEST] Loading model from: {model_uri}")
    model = mlflow.sklearn.load_model(model_uri)

    iris = load_iris()
    X, y = iris.data, iris.target
    _, X_test, _, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    accuracy = accuracy_score(y_test, model.predict(X_test))
    print(f"[TEST] Accuracy: {accuracy}")
    print(f"[TEST] Threshold: {THRESHOLD}")

    if accuracy >= THRESHOLD:
        print("[TEST] PASSED")
        sys.exit(0)
    else:
        print("[TEST] FAILED - accuracy below threshold")
        sys.exit(1)

if __name__ == "__main__":
    model_uri = sys.argv[1]
    test_model(model_uri)
