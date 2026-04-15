import mlflow
from mlflow.tracking import MlflowClient
import subprocess
import sys
import time
import os
import shutil

MLFLOW_URI = "http://localhost:5000"

def deploy_model(model_uri, port=6000):
    os.environ["MLFLOW_TRACKING_URI"] = MLFLOW_URI
    mlflow.set_tracking_uri(MLFLOW_URI)

    print(f"[DEPLOY] Target Model URI: {model_uri}")

    # --- DIAGNOSTIC CHECK ---
    client = MlflowClient()
    run_id = model_uri.split("/")[1]
    try:
        artifacts = client.list_artifacts(run_id)
        print(f"[DEPLOY] Available artifacts in Run {run_id}: {[a.path for a in artifacts]}")
    except Exception as e:
        print(f"[DEPLOY WARNING] Could not list artifacts: {e}")

    # Clean up port and local directories
    os.system(f"fuser -k {port}/tcp 2>/dev/null || true")
    if os.path.exists("./local_model"):
        shutil.rmtree("./local_model")

    print("[DEPLOY] Downloading model to local workspace...")
    try:
        # Download strictly into a dedicated folder
        local_path = mlflow.artifacts.download_artifacts(artifact_uri=model_uri, dst_path="./local_model")
        print(f"[DEPLOY] Model downloaded successfully to: {local_path}")
    except Exception as e:
        print(f"[DEPLOY ERROR] Failed to download: {e}")
        sys.exit(1)

    current_env = os.environ.copy()
    current_env["MLFLOW_TRACKING_URI"] = MLFLOW_URI

    process = subprocess.Popen(
        [
            "mlflow", "models", "serve",
            "-m", local_path,
            "-p", str(port),
            "--no-conda"
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env=current_env
    )

    print("[DEPLOY] Waiting for server to initialize...")
    time.sleep(15)

    if process.poll() is None:
        print(f"[DEPLOY] SUCCESS: Model is live at http://localhost:{port}")
    else:
        stdout, stderr = process.communicate()
        print(f"[DEPLOY ERROR] Model failed to start:\n{stderr.decode()}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python deploy_model.py <model_uri>")
        sys.exit(1)
    deploy_model(sys.argv[1])
