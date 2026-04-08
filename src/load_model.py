import mlflow
from mlflow.tracking import MlflowClient
import sys

MLFLOW_URI = "http://localhost:5000"
MODEL_NAME = "iris-classifier"

def load_model_by_alias(alias):
    mlflow.set_tracking_uri(MLFLOW_URI)
    client = MlflowClient()

    model_version = client.get_model_version_by_alias(MODEL_NAME, alias)
    run_id = model_version.run_id
    version = model_version.version

    print(f"[LOAD] Loaded model version {version} with alias '{alias}'")
    print(f"[LOAD] Run ID: {run_id}")

    with open("run_id.txt", "w") as f:
        f.write(run_id)
    with open("model_version.txt", "w") as f:
        f.write(str(version))

if __name__ == "__main__":
    alias = sys.argv[1]
    load_model_by_alias(alias)
