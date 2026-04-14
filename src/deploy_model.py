import mlflow
import subprocess
import sys
import time
import os

MLFLOW_URI = "http://localhost:5000"

def deploy_model(model_uri, port=6000):
    # 1. Set environment for the current process
    os.environ["MLFLOW_TRACKING_URI"] = MLFLOW_URI
    mlflow.set_tracking_uri(MLFLOW_URI)
    
    print(f"[DEPLOY] Deploying model from: {model_uri}")
    
    # 2. Kill any old process on port 6000
    print(f"[DEPLOY] Cleaning up port {port}...")
    os.system(f"fuser -k {port}/tcp 2>/dev/null || true")
    time.sleep(2)

    # 3. Create a clean environment dictionary for the subprocess
    # This is how your MLflow version gets the Tracking URI
    current_env = os.environ.copy()
    current_env["MLFLOW_TRACKING_URI"] = MLFLOW_URI

    # 4. Start the server (WITHOUT the --tracking-uri flag)
    process = subprocess.Popen(
        [
            "mlflow", "models", "serve", 
            "-m", model_uri, 
            "-p", str(port), 
            "--no-conda"
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env=current_env
    )

    print("[DEPLOY] Waiting for server to initialize...")
    time.sleep(12) 

    if process.poll() is None:
        print(f"[DEPLOY] SUCCESS: Model is live at http://localhost:{port}")
        print(f"[DEPLOY] Inference endpoint: http://localhost:{port}/invocations")
    else:
        stdout, stderr = process.communicate()
        print(f"[DEPLOY ERROR] Model failed to start:\n{stderr.decode()}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python deploy_model.py <model_uri>")
        sys.exit(1)
    deploy_model(sys.argv[1])
