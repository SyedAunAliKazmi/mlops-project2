import mlflow
import mlflow.sklearn
from mlflow.tracking import MlflowClient
import subprocess
import sys
import time
import os
import signal

MLFLOW_URI = "http://localhost:5000"
MODEL_NAME = "iris-classifier"

# CRITICAL FIX: Force the environment variable so the subprocess can see it
os.environ["MLFLOW_TRACKING_URI"] = MLFLOW_URI

def deploy_model(model_uri, port=6000):
    mlflow.set_tracking_uri(MLFLOW_URI)
    print(f"[DEPLOY] Deploying model from: {model_uri}")
    print(f"[DEPLOY] Starting MLflow model server on port {port}...")

    # Kill any existing process on the port
    os.system(f"fuser -k {port}/tcp 2>/dev/null || true")
    time.sleep(2)

    # Start MLflow model serving in background
    # Because we set os.environ above, this command now knows exactly where to find the model
    process = subprocess.Popen(
        ["mlflow", "models", "serve",
         "-m", model_uri,
         "-p", str(port),
         "--no-conda"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    # Wait for server to start
    time.sleep(8)

    if process.poll() is None:
        print(f"[DEPLOY] Model successfully deployed at http://localhost:{port}")
        print(f"[DEPLOY] Inference endpoint: http://localhost:{port}/invocations")
        # Save PID for cleanup
        with open("deploy_pid.txt", "w") as f:
            f.write(str(process.pid))
    else:
        stdout, stderr = process.communicate()
        print(f"[DEPLOY ERROR] {stderr.decode()}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Error: Please provide a model URI")
        sys.exit(1)
        
    model_uri = sys.argv[1]
    deploy_model(model_uri)
