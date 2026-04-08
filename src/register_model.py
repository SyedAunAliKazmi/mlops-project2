import mlflow
from mlflow.tracking import MlflowClient
import sys

MLFLOW_URI = "http://localhost:5000"
MODEL_NAME = "iris-classifier"

def register_model(run_id, alias):
    mlflow.set_tracking_uri(MLFLOW_URI)
    client = MlflowClient()

    model_uri = f"runs:/{run_id}/model"
    result = mlflow.register_model(model_uri, MODEL_NAME)
    version = result.version

    client.set_registered_model_alias(MODEL_NAME, alias, version)
    print(f"[REGISTER] Model version {version} registered with alias '{alias}'")

    with open("model_version.txt", "w") as f:
        f.write(str(version))

if __name__ == "__main__":
    run_id = sys.argv[1]
    alias = sys.argv[2]
    register_model(run_id, alias)
