import mlflow
import subprocess
import sys
import time
import os
import shutil

MLFLOW_URI = "http://localhost:5000"

def deploy_model(model_uri, port=6000):
    # 1. Setup Environment
    os.environ["MLFLOW_TRACKING_URI"] = MLFLOW_URI
    mlflow.set_tracking_uri(MLFLOW_URI)
    
    print(f"[DEPLOY] Target Model URI: {model_uri}")
    
    # 2. Clean up previous attempts
    os.system(f"fuser -k {port}/tcp 2>/dev/null || true")
    if os.path.exists("./local_model"):
        shutil.rmtree("./local_model")
    
    # 3. MANUALLY DOWNLOAD THE ARTIFACT
    # This uses the Python API which is more robust than the CLI for downloads
    print("[DEPLOY] Downloading model to local workspace...")
    try:
        local_path = mlflow.artifacts.download_artifacts(artifact_uri=model_uri, dst_path=".")
        # Usually downloads to a folder named 'model'
        print(f"[DEPLOY] Model downloaded to: {local_path}")
    except Exception as e:
        print(f"[DEPLOY ERROR] Failed to download: {e}")
        sys.exit(1)

    # 4. Start the server using the LOCAL path
    # Now MLflow doesn't need to 'download' anything; it just reads the folder
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
        sys.exit(1)
    deploy_model(sys.argv[1])
