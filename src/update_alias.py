import mlflow
from mlflow.tracking import MlflowClient
import sys

MLFLOW_URI = "http://localhost:5000"
MODEL_NAME = "iris-classifier"

def update_alias(version, old_alias, new_alias):
    mlflow.set_tracking_uri(MLFLOW_URI)
    client = MlflowClient()
    client.set_registered_model_alias(MODEL_NAME, new_alias, version)
    try:
        client.delete_registered_model_alias(MODEL_NAME, old_alias)
    except Exception:
        pass
    print(f"[ALIAS] Updated version {version}: '{old_alias}' → '{new_alias}'")

if __name__ == "__main__":
    version = sys.argv[1]
    old_alias = sys.argv[2]
    new_alias = sys.argv[3]
    update_alias(version, old_alias, new_alias)
